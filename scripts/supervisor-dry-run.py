#!/usr/bin/env python3
"""Check the real STOP gate or dispatch one fixed worker against a test gate."""

import argparse
from datetime import datetime, timezone
import fcntl
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
from uuid import uuid4


# The hold fixture inherits the lock in both processes. If the supervisor is
# killed, the lock remains held until the bounded fixture group has exited.
HOLD_WORKER = '''
import signal
import subprocess
import sys

child = subprocess.Popen(
    [sys.executable, "-I", "-c", "import time; time.sleep(3)"],
    pass_fds=(int(sys.argv[1]),),
)

# Let the child receive group SIGTERM while this process stays to reap it.
signal.signal(signal.SIGTERM, signal.SIG_IGN)
print(f"FIXTURE_CHILD_PID={child.pid}", flush=True)
if child.wait() != 0:
    sys.exit(1)
print("FIXTURE_WORKER_RAN", flush=True)
'''

FINAL_STATES = {"completed", "failed", "timed_out", "interrupted", "refused"}


def stop_reason(directory: Path) -> str | None:
    try:
        directory_fd = os.open(directory, os.O_RDONLY | os.O_DIRECTORY)
    except OSError:
        return "STOP directory unavailable"

    try:
        os.stat("STOP", dir_fd=directory_fd, follow_symlinks=False)
    except FileNotFoundError:
        return None
    except OSError:
        return "STOP status unavailable"
    finally:
        os.close(directory_fd)

    # Presence alone is sufficient. The latch contents have no meaning.
    return "STOP is present"


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def save_checkpoint(path: Path, checkpoint: dict) -> None:
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", dir=path.parent, prefix=".checkpoint-", delete=False
    ) as output:
        temporary = Path(output.name)
        try:
            json.dump(checkpoint, output)
            output.write("\n")
            output.flush()
            os.fsync(output.fileno())
            os.replace(temporary, path)
            directory_fd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
            try:
                os.fsync(directory_fd)
            finally:
                os.close(directory_fd)
        finally:
            temporary.unlink(missing_ok=True)


def stop_worker_group(worker: subprocess.Popen) -> None:
    try:
        os.killpg(worker.pid, signal.SIGTERM)
    except ProcessLookupError:
        pass

    try:
        worker.wait(timeout=1)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(worker.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        worker.wait()


def run_fixture(directory: Path, deadline: float, hold: bool) -> int:
    lock_fd = os.open(
        directory / "supervisor.lock", os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600
    )
    try:
        try:
            fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            print("REFUSED: another invocation owns the fixture lock")
            return 1

        path = directory / "checkpoint.json"
        try:
            previous = json.loads(path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            previous = None
        else:
            if (
                not isinstance(previous, dict)
                or previous.get("task") != "fixture"
                or not isinstance(previous.get("owner"), str)
                or not isinstance(previous.get("state"), str)
                or previous["state"] not in FINAL_STATES | {"running"}
            ):
                print("REFUSED: invalid fixture checkpoint")
                return 1
            if previous["state"] == "running":
                previous.update(state="interrupted", finished_at=timestamp())
                save_checkpoint(path, previous)
                print("RECONCILED: interrupted fixture was not dispatched again")
                return 1

            print(f"REFUSED: fixture already recorded as {previous['state']}")
            return 1

        record = {
            "task": "fixture",
            "owner": uuid4().hex,
            "supervisor_pid": os.getpid(),
            "state": "running",
            "started_at": timestamp(),
            "deadline_seconds": deadline,
        }
        save_checkpoint(path, record)

        reason = stop_reason(directory)
        if reason is not None:
            record.update(state="refused", finished_at=timestamp(), reason=reason)
            save_checkpoint(path, record)
            print(f"REFUSED: {reason}")
            return 1

        program = HOLD_WORKER if hold else "print('FIXTURE_WORKER_RAN')"
        worker = subprocess.Popen(
            [sys.executable, "-I", "-c", program, str(lock_fd)],
            env={},
            start_new_session=True,
            pass_fds=(lock_fd,),
        )
        try:
            rc = worker.wait(timeout=deadline)
        except subprocess.TimeoutExpired:
            stop_worker_group(worker)
            record.update(state="timed_out", finished_at=timestamp())
            save_checkpoint(path, record)
            print("TIMED OUT: fixture process group stopped")
            return 124
        except BaseException:
            stop_worker_group(worker)
            raise

        record.update(
            state="completed" if rc == 0 else "failed",
            finished_at=timestamp(),
            worker_exit_code=rc,
        )
        save_checkpoint(path, record)
        return 0 if rc == 0 else 1
    finally:
        os.close(lock_fd)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check-real", action="store_true", help="inspect the real gate only")
    mode.add_argument("--fixture-dir", type=Path, help="use a temporary STOP directory")
    parser.add_argument("--deadline-seconds", type=float, default=5)
    parser.add_argument("--hold-fixture", action="store_true", help="run the bounded child fixture")
    args = parser.parse_args()
    if not 0 < args.deadline_seconds <= 10:
        parser.error("--deadline-seconds must be greater than 0 and at most 10")

    directory = Path("/etc/code-goblin") if args.check_real else args.fixture_dir
    reason = stop_reason(directory)
    if reason is not None:
        print(f"REFUSED: {reason}")
        return 1

    if args.check_real:
        print("CLEAR: real gate was checked without dispatch")
        return 0

    try:
        return run_fixture(directory, args.deadline_seconds, args.hold_fixture)
    except (OSError, ValueError) as error:
        print(f"REFUSED: fixture state or execution unavailable ({type(error).__name__})")
        return 1


if __name__ == "__main__":
    sys.exit(main())
