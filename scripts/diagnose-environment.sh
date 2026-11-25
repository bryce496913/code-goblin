#!/usr/bin/env bash
# Read-only inventory. Print no environment variables, credentials, or home paths.
set -eu

for tool in git gh codex obs; do
    if command -v "$tool" >/dev/null; then
        printf '%s: found\n' "$tool"
    else
        printf '%s: missing\n' "$tool"
    fi
done

if command -v godot4 >/dev/null || command -v godot >/dev/null; then
    printf 'Godot: found\n'
else
    printf 'Godot: missing\n'
fi

printf 'Kernel: %s\n' "$(uname -sr)"
getconf _NPROCESSORS_ONLN | awk '{print "Online CPUs: " $1}'
awk '/^MemTotal:/ {print "Physical memory: " $2 " " $3}' /proc/meminfo
df -Pk . | awk 'NR == 2 {print "Available disk (KiB): " $4}'
