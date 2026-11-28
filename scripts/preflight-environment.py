#!/usr/bin/env python3
"""Check or prepare the local, supervised Code Goblin environment."""

import argparse
from importlib import import_module
import os
from pathlib import Path
import shutil
import stat
import subprocess
import tempfile

REPO = Path(__file__).resolve().parents[1]
PRIVATE_DIRS = ("config", "tmp", "logs", "generated-assets", "cache", "state")
REQUIRED = ("bash", "git", "gh", "godot", "obs", "node", "npm")
OPTIONAL = ("vainfo", "gst-launch-1.0", "gst-discoverer-1.0", "ffmpeg", "jq", "smartctl")


def runtime_directory(root: Path, setup: bool) -> None:
    if root.is_symlink() or root.resolve().is_relative_to(REPO):
        raise ValueError("runtime root must be a real directory outside this checkout")
    for directory in (root, *(root / name for name in PRIVATE_DIRS)):
        if directory.is_symlink():
            raise ValueError(f"refusing a symlink at {directory.name}")
        if setup:
            directory.mkdir(mode=0o700, parents=True, exist_ok=True)
        info = directory.stat()
        if not directory.is_dir() or info.st_uid != os.getuid():
            raise ValueError(f"{directory.name} must be a directory owned by the current user")
        if setup and stat.S_IMODE(info.st_mode) != 0o700:
            directory.chmod(0o700)
        if stat.S_IMODE(directory.stat().st_mode) != 0o700:
            raise ValueError(f"{directory.name} permissions must be 0700")


def command(args: list[str], *, env: dict | None = None, cwd: Path = REPO) -> str:
    result = subprocess.run(args, cwd=cwd, env=env, capture_output=True, text=True, timeout=15)
    if result.returncode:
        raise ValueError(f"{Path(args[0]).name} exited {result.returncode}")
    return result.stdout.strip()


def godot_smoke(godot: str, root: Path) -> None:
    with tempfile.TemporaryDirectory(prefix="godot-check-", dir=root / "tmp") as temp:
        scratch = Path(temp)
        (scratch / "project.godot").write_text("config_version=5\n")
        (scratch / "verify.gd").write_text(
            'extends SceneTree\n\n'
            'func _initialize() -> void:\n'
            '\tprint("CODE_GOBLIN_GDSCRIPT_OK")\n'
            '\tquit(0)\n'
        )
        env = os.environ | {"XDG_CONFIG_HOME": str(scratch / "config"),
                            "XDG_CACHE_HOME": str(scratch / "cache"),
                            "XDG_DATA_HOME": str(scratch / "data")}
        out = command([godot, "--headless", "--path", temp, "--script", "verify.gd"], env=env)
        if "CODE_GOBLIN_GDSCRIPT_OK" not in out.splitlines():
            raise ValueError("Godot did not emit the expected GDScript marker")


def asset_smoke(root: Path) -> None:
    import sys

    from PIL import Image

    with tempfile.TemporaryDirectory(prefix="asset-check-", dir=root / "tmp") as temp:
        source = Path(temp) / "source.png"
        output = Path(temp) / "prepared.png"
        canvas = Image.new("RGBA", (3, 3))
        canvas.putpixel((1, 1), (163, 230, 53, 255))
        canvas.save(source)
        command([sys.executable, str(REPO / "studio/asset-generation/prepare_png.py"),
                 str(source), str(output), "--size", "6", "6", "--palette", "a3e635"])
        with Image.open(output) as result:
            if (result.mode, result.size, result.getchannel("A").getbbox()) != (
                "RGBA", (6, 6), (2, 2, 4, 4)
            ):
                raise ValueError("prepared PNG has unexpected dimensions or alpha")


def temperature_warning() -> None:
    for path in Path("/sys/class/thermal").glob("thermal_zone*"):
        try:
            if (path / "type").read_text().strip() != "pch_wildcat_point":
                continue
            current = int((path / "temp").read_text())
            trip = int((path / "trip_point_0_temp").read_text())
        except (OSError, ValueError):
            continue
        if current >= trip - 1000:
            print(f"WARN chipset sensor {current / 1000:.1f}°C near {trip / 1000:.1f}°C trip; verify before sustained load")


def main() -> int:
    state_home = Path(os.environ.get("XDG_STATE_HOME") or Path.home() / ".local/state")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=state_home / "code-goblin/runtime")
    parser.add_argument("--setup", action="store_true", help="create or repair private directories")
    parser.add_argument("--online", action="store_true", help="read the configured GitHub main ref")
    parser.add_argument("--godot-smoke", action="store_true", help="execute a disposable GDScript")
    parser.add_argument("--asset-smoke", action="store_true", help="prepare a disposable RGBA PNG")
    args = parser.parse_args()
    root = args.root.expanduser().absolute()
    errors = []
    tools = {}
    os.umask(0o077)
    try:
        runtime_directory(root, args.setup)
        print("PASS private runtime directories")
    except (OSError, ValueError) as error:
        errors.append(f"private runtime: {error}")

    pinned = Path.home() / ".local/share/code-goblin/codex/node_modules/.bin/codex"
    for name in (*REQUIRED, "codex"):
        candidate = str(pinned) if name == "codex" and os.access(pinned, os.X_OK) else shutil.which(name)
        if not candidate:
            errors.append(f"missing required tool: {name}")
            continue
        tools[name] = candidate
        try:
            version = command([candidate, "--version"]).splitlines()[0]
            print(f"PASS {name}: {version}")
        except (OSError, ValueError, IndexError, subprocess.TimeoutExpired) as error:
            errors.append(f"{name}: {error}")
    try:
        pillow = import_module("PIL.Image")
        print(f"PASS Pillow: {pillow.__version__}")
    except ImportError:
        errors.append("missing required Python package: Pillow")
    if codex := tools.get("codex"):
        try:
            help_text = command([codex, "exec", "--help"])
            if not all(flag in help_text for flag in ("--json", "resume", "--sandbox")):
                raise ValueError("installed Codex lacks the expected exec options")
            print("PASS Codex exec interface (help only)")
        except (OSError, ValueError, subprocess.TimeoutExpired) as error:
            errors.append(f"Codex exec: {error}")
    for name in OPTIONAL:
        if not shutil.which(name):
            print(f"OPTIONAL missing: {name}")

    if args.online and "git" in tools:
        try:
            out = command([tools["git"], "ls-remote", "--exit-code", "origin", "refs/heads/main"],
                          env=os.environ | {"GIT_TERMINAL_PROMPT": "0"})
            print(f"PASS GitHub main: {out.split()[0]}")
        except (OSError, ValueError, IndexError, subprocess.TimeoutExpired) as error:
            errors.append(f"GitHub: {error}")
    if not any(error.startswith("private runtime:") for error in errors):
        if args.godot_smoke and "godot" in tools:
            try:
                godot_smoke(tools["godot"], root)
                print("PASS Godot headless GDScript")
            except (OSError, ValueError, subprocess.TimeoutExpired) as error:
                errors.append(f"Godot smoke: {error}")
        if args.asset_smoke:
            try:
                asset_smoke(root)
                print("PASS RGBA asset preparation")
            except (ImportError, OSError, ValueError, subprocess.TimeoutExpired) as error:
                errors.append(f"asset smoke: {error}")
    temperature_warning()
    for error in errors:
        print(f"FAIL {error}")
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
