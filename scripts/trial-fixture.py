#!/usr/bin/env python3
"""Exercise a fixed local trial task with no model calls or external effects."""

import argparse
from pathlib import Path
import os
import selectors
import shutil
import subprocess
import sys
import time

MIB = 1024**2
LOG_LIMIT = 5 * MIB
SCRATCH_LIMIT = 100 * MIB
RETENTION_SECONDS = 7 * 86400
WORKER_SECONDS = 90
SESSION_SECONDS = 300
RAM_FLOOR = 1280 * MIB
DISK_FLOOR = 12_000_000_000


def preflight(backing: Path) -> None:
    available = next(
        int(line.split()[1]) * 1024
        for line in Path("/proc/meminfo").read_text().splitlines()
        if line.startswith("MemAvailable:")
    )
    if available < RAM_FLOOR:
        raise ValueError("available RAM below 1.25 GiB")
    if shutil.disk_usage(backing).free < DISK_FLOOR:
        raise ValueError("backing filesystem has less than 12 GB free")


def expire_logs(directory: Path, now: float) -> None:
    for path in directory.glob("trial-*.log"):
        if not path.is_symlink() and path.is_file():
            if path.stat().st_mtime <= now - RETENTION_SECONDS:
                path.unlink()


def verify_scratch_volume(scratch: Path) -> None:
    stat = os.statvfs(scratch)
    if not scratch.is_mount() or stat.f_blocks * stat.f_frsize > SCRATCH_LIMIT:
        raise ValueError("scratch needs a dedicated volume capped at 100 MiB")


def run_fixture(scratch: Path, log, deadline: float) -> None:
    # The only task checks its own write permissions and removes its own marker.
    program = (
        "from pathlib import Path; "
        "p=Path('fixture-marker'); "
        "f=p.open('x'); f.write('CODE_GOBLIN_FIXTURE\\n'); f.close(); "
        "assert p.read_text() == 'CODE_GOBLIN_FIXTURE\\n'; p.unlink(); "
        "print('FIXTURE_MARKER_VERIFIED')"
    )
    limit = min(time.monotonic() + WORKER_SECONDS, deadline)
    with subprocess.Popen(
        [sys.executable, "-I", "-c", program],
        cwd=scratch,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env={},
    ) as worker:
        try:
            copy_log(worker.stdout, log, limit)
            if worker.wait(timeout=max(0, limit - time.monotonic())):
                raise ValueError("fixed marker task failed")
        finally:
            if worker.poll() is None:
                worker.kill()
                worker.wait()


def copy_log(source, sink, deadline: float) -> None:
    stored = 0
    with selectors.DefaultSelector() as selector:
        selector.register(source, selectors.EVENT_READ)
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0 or not selector.select(remaining):
                raise TimeoutError("fixture exceeded its deadline")
            chunk = os.read(source.fileno(), min(65536, LOG_LIMIT - stored + 1))
            if not chunk:
                return
            allowed = min(len(chunk), LOG_LIMIT - stored)
            sink.write(chunk[:allowed])
            stored += allowed
            if allowed != len(chunk):
                raise ValueError("combined fixture log exceeds 5 MiB")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scratch", type=Path, required=True)
    parser.add_argument("--logs", type=Path, required=True)
    args = parser.parse_args()
    deadline = time.monotonic() + SESSION_SECONDS
    try:
        preflight(args.scratch.parent)
        verify_scratch_volume(args.scratch)
        if args.logs.resolve().is_relative_to(args.scratch.resolve()):
            raise ValueError("logs must be outside the capped scratch volume")
        args.logs.mkdir(mode=0o700, exist_ok=True)
        expire_logs(args.logs, time.time())
        # The one-run claim survives expiration of the captured log.
        with (args.logs / "fixture.claim").open("x") as claim:
            claim.write(f"{os.getpid()}\n")
        with (args.logs / "trial-fixture.log").open("xb") as log:
            run_fixture(args.scratch, log, deadline)
    except (OSError, ValueError, TimeoutError, subprocess.TimeoutExpired) as error:
        print(f"REFUSED: {error}", file=sys.stderr)
        return 1
    print(f"PASS fixed marker task as UID {os.getuid()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
