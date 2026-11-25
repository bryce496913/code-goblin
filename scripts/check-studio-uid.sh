#!/usr/bin/env bash
# Owner-terminal diagnostic. Runs a fixed offline fixture as the studio UID.
set -eu

test -f /etc/code-goblin/STOP
id -u code-goblin >/dev/null
script_dir=$(cd "$(dirname "$0")" && pwd)
stage=$(mktemp -d)
trap 'rm -f -- "$stage/trial-fixture.py"; rmdir -- "$stage"' EXIT
chmod 0755 "$stage"
install -m 0644 "$script_dir/trial-fixture.py" "$stage/trial-fixture.py"
uid=$(id -u code-goblin)
gid=$(id -g code-goblin)

sudo systemd-run --wait --pipe --collect \
    --property=User=code-goblin \
    --property=Group=code-goblin \
    --property=NoNewPrivileges=yes \
    --property=PrivateNetwork=yes \
    --property=ProtectHome=yes \
    --property=KillMode=control-group \
    --property=CPUQuota=100% \
    --property=MemoryMax=768M \
    --property=MemorySwapMax=0 \
    --property=RuntimeMaxSec=300 \
    --property=RuntimeDirectory=code-goblin-trial-fixture \
    --property=RuntimeDirectoryMode=0700 \
    "--property=TemporaryFileSystem=/mnt:size=100M,mode=0700,uid=$uid,gid=$gid" \
    /usr/bin/python3 "$stage/trial-fixture.py" \
    --scratch /mnt --logs /run/code-goblin-trial-fixture

test -f /etc/code-goblin/STOP
sudo -H -u code-goblin -- /usr/local/bin/codex --version
if sudo -H -u code-goblin -- /usr/local/bin/codex login status; then
    echo "Studio account reports a CLI login."
else
    echo "Studio CLI login still needs separate verification."
fi
