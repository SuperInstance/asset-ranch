#!/usr/bin/env bash
# RESERVED lane: DeepInfra FLUX-2-max. REAL MONEY. Campaign-only.
# Refuses to run without the explicit --nod flag (Casey's approval token).
# Gotcha: width must be <= 1440 — always pass explicit --size, never bare aspect.
set -euo pipefail
NOD=0; shift_ok=0
ARGS=()
for a in "$@"; do
  if [ "$shift_ok" = 0 ] && [ "$a" = "--nod" ]; then NOD=1; continue; fi
  ARGS+=("$a")
done
OUT="${ARGS[0]:?usage: gen-deepinfra.sh --nod <output.png> <prompt> [--size 1280x1024]}"
PROMPT="${ARGS[1]:?usage: gen-deepinfra.sh --nod <output.png> <prompt>}"
SIZE="1280x1024"
for a in "${ARGS[@]:2}"; do [ "$a" = "--size" ] && continue; case "$a" in *x*) SIZE="$a";; esac; done

if [ "$NOD" != 1 ]; then
  echo "REFUSED: DeepInfra FLUX-2-max costs real money." >&2
  echo "Re-run with --nod only when Casey has approved this campaign spend." >&2
  exit 2
fi
: "${DEEPINFRA_API_KEY:?DEEPINFRA_API_KEY env not set}"

W="${SIZE%x*}"; H="${SIZE#*x}"
[ "$W" -le 1440 ] || { echo "width $W > 1440 — FLUX-2-max rejects it"; exit 1; }

REQ=$(jq -nc --arg p "$PROMPT" --argjson w "$W" --argjson h "$H" \
  '{prompt:$p, width:$w, height:$h}')
for attempt in 1 2 3; do
  CODE=$(curl -s -o /tmp/di-resp.json -w '%{http_code}' -X POST \
    "https://api.deepinfra.com/v1/inference/black-forest-labs/FLUX-2-max" \
    -H "Authorization: Bearer $DEEPINFRA_API_KEY" -H 'Content-Type: application/json' -d "$REQ") || true
  if [ "$CODE" = 429 ]; then echo "429, waiting 60s (attempt $attempt)"; sleep 60; continue; fi
  break
done
[ "$CODE" = 200 ] || { echo "deepinfra error HTTP $CODE"; head -c 300 /tmp/di-resp.json; exit 1; }
mkdir -p "$(dirname "$OUT")"
jq -r '.images[0]' /tmp/di-resp.json | base64 -d > "$OUT" 2>/dev/null || cp /tmp/di-resp.json "$OUT"
echo "[deepinfra] wrote $OUT (FLUX-2-max, $SIZE) — money spent"
