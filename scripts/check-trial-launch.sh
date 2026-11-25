#!/usr/bin/env bash
# Offline owner-terminal check using the proposed service identity and envelope.
set -eu
test -f /etc/code-goblin/STOP
script_dir=$(cd "$(dirname "$0")" && pwd)
stage=$(mktemp -d)
trap 'rm -f -- "$stage"/*.py; rmdir -- "$stage"' EXIT
chmod 0755 "$stage"
install -m 0644 "$script_dir"/{supervised-trial,trial-fixture,supervisor-dry-run}.py "$stage"
uid=$(id -u code-goblin)
gid=$(id -g code-goblin)
sudo systemd-run --unit=code-goblin-trial-fixture --wait --pipe --collect \
    -p User=code-goblin -p Group=code-goblin -p NoNewPrivileges=yes \
    -p PrivateNetwork=yes -p ProtectHome=yes -p ProtectSystem=strict \
    -p 'ReadWritePaths=/run/code-goblin-trial-fixture' \
    -p KillMode=control-group -p CPUQuota=100% -p MemoryMax=768M -p MemorySwapMax=0 \
    -p RuntimeMaxSec=300 -p TimeoutStopSec=5 \
    -p RuntimeDirectory=code-goblin-trial-fixture -p RuntimeDirectoryMode=0700 \
    -p "TemporaryFileSystem=/mnt:size=100M,mode=0700,uid=$uid,gid=$gid" \
    /usr/bin/python3 -B "$stage/supervised-trial.py" --fixture \
    --scratch /mnt --logs /run/code-goblin-trial-fixture
test -f /etc/code-goblin/STOP
if sudo -H -u code-goblin -- /usr/bin/test -r /var/lib/code-goblin/.codex/auth.json; then
    echo 'PASS dedicated file-backed login is readable by the studio account'
else
    echo 'BLOCKED dedicated file-backed login is unavailable'
    exit 1
fi
