#!/usr/bin/env bash
set -eu

if [[ $# != 1 || "$1" != /* || -e "$1" ]]; then
    echo "Usage: $0 /absolute/path/to/new-playtest.pck" >&2
    exit 2
fi
output=$1
project=$(cd "$(dirname "$0")/.." && pwd)
scratch=$(mktemp -d)
trap 'rm -rf -- "$scratch"' EXIT
mkdir "$scratch/game"
cp "$project/project.godot" "$project/export_presets.cfg" "$project/icon.svg" "$project/icon.svg.import" "$scratch/game/"
cp -R "$project/scenes" "$project/scripts" "$project/tests" "$scratch/game/"
export XDG_CONFIG_HOME="$scratch/config" XDG_DATA_HOME="$scratch/data" XDG_CACHE_HOME="$scratch/cache"

run_check() {
    local limit=$1
    shift
    local status=0
    timeout "$limit" godot --headless "$@" > "$scratch/check.log" 2>&1 || status=$?
    cat "$scratch/check.log"
    [[ $status == 0 ]] && ! grep -Eq 'ERROR:|SCRIPT ERROR:' "$scratch/check.log"
}

run_check 45s --path "$scratch/game" --editor --import
run_check 15s --path "$scratch/game" --quit-after 5
run_check 15s --path "$scratch/game" --script tests/repair_shop_smoke.gd
run_check 30s --path "$scratch/game" --export-pack Linux "$scratch/playtest.pck"
test -s "$scratch/playtest.pck"
run_check 15s --main-pack "$scratch/playtest.pck" --quit-after 5
run_check 15s --main-pack "$scratch/playtest.pck" --script res://tests/repair_shop_smoke.gd
(set -o noclobber; cat "$scratch/playtest.pck" > "$output")
