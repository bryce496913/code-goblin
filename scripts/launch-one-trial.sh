#!/usr/bin/env bash
# Owner terminal only, after explicit approval and a separate STOP reset.
set -eu
if [[ $# -ne 1 || $1 != --approved-one-run ]]; then
    echo "Usage after owner approval: $0 --approved-one-run" >&2
    exit 2
fi
script_dir=$(cd "$(dirname "$0")" && pwd)
if [[ -e /etc/code-goblin/STOP || -L /etc/code-goblin/STOP ]]; then
    echo 'REFUSED: STOP is present.' >&2
    exit 1
fi
test -r /etc/code-goblin && test -x /etc/code-goblin
stage=$(mktemp -d)
cleanup() {
    if ! sudo -n touch /etc/code-goblin/STOP; then
        echo 'Re-arm STOP immediately from the owner terminal.' >&2
    fi
    rm -f -- "$stage"/*.py
    rmdir -- "$stage"
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
chmod 0755 "$stage"
install -m 0644 "$script_dir"/{supervised-trial,trial-fixture,supervisor-dry-run}.py "$stage"
uid=$(id -u code-goblin)
gid=$(id -g code-goblin)
# Root-owned atomic claim persists across exits, failures and reboots.
sudo mkdir -m 0700 /var/lib/code-goblin-supervised-trial.claim
sudo systemd-run --unit=code-goblin-supervised-trial --wait --pipe --collect \
    -p User=code-goblin -p Group=code-goblin -p NoNewPrivileges=yes \
    -p ProtectHome=yes -p ProtectSystem=strict -p PrivateDevices=yes -p LimitCORE=0 \
    -p 'RestrictAddressFamilies=AF_UNIX AF_INET AF_INET6' \
    -p KillMode=control-group -p CPUQuota=100% -p MemoryMax=768M -p MemorySwapMax=0 \
    -p RuntimeMaxSec=300 -p TimeoutStopSec=5 \
    -p StateDirectory=code-goblin-supervised-trial -p StateDirectoryMode=0700 \
    -p "TemporaryFileSystem=/mnt:size=100M,mode=0700,uid=$uid,gid=$gid" \
    /usr/bin/python3 -B "$stage/supervised-trial.py" \
    --scratch /mnt --logs /var/lib/code-goblin-supervised-trial
