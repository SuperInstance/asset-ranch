#!/usr/bin/env bash
# LOCAL lane wrapper — free, unlimited. See docs/LANES.md.
set -euo pipefail
if [ $# -lt 2 ]; then echo "usage: gen-local.sh <output.png> <prompt> [extra gen-local.py args...]"; exit 1; fi
OUT="$1"; shift
exec python3 "$(dirname "$0")/gen-local.py" --out "$OUT" "$@"
