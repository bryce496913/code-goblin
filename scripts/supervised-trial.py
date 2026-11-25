#!/usr/bin/env python3
"""Run the fixed supervised marker trial or its offline protocol fixture."""

import argparse
import json
import os
from pathlib import Path
import selectors
import subprocess
import time

# The existing fixed fixture owns the resource policy.
from importlib import import_module

limits = import_module("trial-fixture")
gate = import_module("supervisor-dry-run")

MARKER = "CODE_GOBLIN_TRIAL_OK"
CLI = "/opt/code-goblin/codex-0.172.0/node_modules/.bin/codex"
TOKEN_LIMITS = {"input_tokens": 50000, "output_tokens": 1000}
FIXTURE = '''
import json
import sys

print("private fixture diagnostic", file=sys.stderr)
for event in (
    {"type": "turn.started"},
    {"type": "item.completed", "item": {"type": "agent_message",
                                        "text": "CODE_GOBLIN_TRIAL_OK"}},
    {"type": "turn.completed", "usage": {"input_tokens": 7, "output_tokens": 2,
                                        "extra": "private fixture field"}},
):
    print(json.dumps(event))
'''


def read_evidence(worker: subprocess.Popen, deadline: float) -> dict:
    started = completed = 0
    marker = False
    usage = {}
    pending = bytearray()
    received = 0
    with selectors.DefaultSelector() as selector:
        selector.register(worker.stdout, selectors.EVENT_READ, True)
        selector.register(worker.stderr, selectors.EVENT_READ, False)
        while selector.get_map():
            remaining = deadline - time.monotonic()
            if remaining <= 0 or not (ready := selector.select(remaining)):
                raise TimeoutError
            for key, _ in ready:
                chunk = os.read(key.fd, min(65536, limits.LOG_LIMIT - received + 1))
                if not chunk:
                    selector.unregister(key.fileobj)
                    continue
                received += len(chunk)
                if received > limits.LOG_LIMIT:
                    raise ValueError("output cap exceeded")
                if not key.data:
                    continue  # Count raw stderr in the cap and discard it.
                pending.extend(chunk)
                while (end := pending.find(b"\n")) >= 0:
                    line = bytes(pending[:end])
                    del pending[:end + 1]
                    event = json.loads(line)
                    kind = event.get("type")
                    if kind == "turn.started":
                        started += 1
                        if started > 1:
                            raise ValueError("multiple turns reported")
                    if kind == "item.completed":
                        item = event.get("item", {})
                        if item.get("type") == "agent_message":
                            marker = item.get("text", "").strip() == MARKER
                        elif item.get("type") not in {"reasoning", "plan"}:
                            raise ValueError("unexpected completed item")
                    if kind == "turn.completed":
                        completed += 1
                        reported = event.get("usage", {})
                        usage = {key: reported[key] for key in TOKEN_LIMITS
                                 if type(reported.get(key)) is int and reported[key] >= 0}

    if pending or (started, completed) != (1, 1) or not marker or usage.keys() != TOKEN_LIMITS.keys():
        raise ValueError("incomplete trial evidence")
    return {"marker_verified": True, "usage": usage,
            "usage_within_review_thresholds": all(usage[key] <= cap for key, cap in TOKEN_LIMITS.items())}


def worker_command(fixture: bool) -> list[str]:
    if fixture:
        return ["/usr/bin/python3", "-I", "-c", FIXTURE]
    return [CLI, "--ask-for-approval", "never", "exec", "--ignore-user-config",
            "--disable", "plugins", "--disable", "apps", "--disable", "shell_tool", "--sandbox", "read-only",
            "--skip-git-repo-check", "--ephemeral", "--json", "-m", "gpt-6.2-sol",
            "-c", 'model_reasoning_effort="low"', "-c", 'web_search="disabled"',
            f"Reply with exactly {MARKER}. Do not call any tools."]


def run(scratch: Path, logs: Path, fixture: bool) -> None:
    session_deadline = time.monotonic() + limits.SESSION_SECONDS
    limits.preflight(scratch.parent)
    limits.verify_scratch_volume(scratch)
    if logs.resolve().is_relative_to(scratch.resolve()):
        raise ValueError("logs must be outside scratch")
    if not fixture and gate.stop_reason(Path("/etc/code-goblin")):
        raise ValueError("real STOP gate refused")
    limits.expire_logs(logs, time.time())
    mode = "fixture" if fixture else "live"
    with (logs / f"{mode}.claim").open("x") as claim:
        claim.write(f"{os.getpid()}\n")
        claim.flush()
        os.fsync(claim.fileno())
    report = logs / f"trial-{mode}.log"
    with report.open("x") as log:
        json.dump({"state": "started", "mode": mode}, log)
        log.write("\n")
        log.flush()
        os.fsync(log.fileno())
        if not fixture and gate.stop_reason(Path("/etc/code-goblin")):
            raise ValueError("real STOP gate refused before dispatch")
        env = {"PATH": "/usr/local/bin:/usr/bin:/bin", "HOME": str(scratch),
               "CODEX_HOME": str(scratch / ".codex")}
        if not fixture:
            auth_dir = scratch / ".codex"
            auth_dir.mkdir(mode=0o700)
            auth = Path("/var/lib/code-goblin/.codex/auth.json")
            if not auth.is_file() or not os.access(auth, os.R_OK):
                raise ValueError("dedicated file-backed Codex login unavailable")
            (auth_dir / "auth.json").symlink_to(auth)
        deadline = min(time.monotonic() + limits.WORKER_SECONDS, session_deadline)
        with subprocess.Popen(worker_command(fixture), cwd=scratch, env=env,
                              stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE) as worker:
            try:
                evidence = read_evidence(worker, deadline)
                if worker.wait(timeout=max(0, deadline - time.monotonic())) != 0:
                    raise ValueError("worker exited unsuccessfully")
            finally:
                if worker.poll() is None:
                    worker.kill()
                    worker.wait()
        with (scratch / "trial-marker.txt").open("x") as marker:
            marker.write(MARKER + "\n")
        json.dump({"state": "completed", **evidence}, log)
        log.write("\n")
        log.flush()
        os.fsync(log.fileno())
    print(f"PASS {mode} trial protocol as UID {os.getuid()}")
    print(json.dumps(evidence))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", action="store_true")
    parser.add_argument("--scratch", type=Path, required=True)
    parser.add_argument("--logs", type=Path, required=True)
    args = parser.parse_args()
    try:
        run(args.scratch, args.logs, args.fixture)
    except (OSError, ValueError, TypeError, AttributeError, TimeoutError,
            subprocess.TimeoutExpired) as error:
        # No exception details from child output enter persistent logs.
        print(f"REFUSED OR FAILED: {type(error).__name__}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
