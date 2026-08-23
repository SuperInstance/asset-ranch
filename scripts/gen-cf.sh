#!/usr/bin/env bash
# CLOUD-FREE lane: Cloudflare Workers AI flux-1-schnell. Free quota.
# usage: gen-cf.sh <output.png> <prompt>
# Auth: CLOUDFLARE_API_TOKEN (+ CLOUDFLARE_ACCOUNT_ID) env, else wrangler
# OAuth fallback. Never hardcode tokens.
set -euo pipefail
OUT="${1:?usage: gen-cf.sh <output.png> <prompt> [negative]}"; shift
PROMPT="${1:?usage: gen-cf.sh <output.png> <prompt> [negative]}"
NEG="${2:-photorealistic, photographic, noise, grain, gritty, thin spindly parts, harsh shadows, text, watermark, cluttered background, complex shading}"
STYLESUFFIX="chunky beveled-block low-poly 3D render, toylike proportions, saturated punchy colors, smooth plastic material, flat lighting, clean silhouette, isometric 3/4 view, solid flat background, game asset"
# flux-1-schnell endpoint rejects a negative_prompt field; fold into prompt.
NEGTEXT=". Avoid: photographic realism, noise, gritty texture, spindly thin detail, harsh shadows, text, cluttered backgrounds"

acct() {
  if [ -n "${CLOUDFLARE_ACCOUNT_ID:-}" ]; then echo "$CLOUDFLARE_ACCOUNT_ID"; return; fi
  wrangler whoami 2>/dev/null | grep -oP '\b[0-9a-f]{32}\b' | head -1
}

tok() {
  if [ -n "${CLOUDFLARE_API_TOKEN:-}" ]; then echo "$CLOUDFLARE_API_TOKEN"; return; fi
  grep -oP 'oauth_token = "\K[^"]+' ~/.config/.wrangler/config/default.toml
}

ACCOUNT="$(acct)"; TOKEN="$(tok)"
[ -n "$ACCOUNT" ] && [ -n "$TOKEN" ] || { echo "no cloudflare auth found" >&2; exit 1; }

URL="https://api.cloudflare.com/client/v4/accounts/$ACCOUNT/ai/run/@cf/black-forest-labs/flux-1-schnell"
REQ=$(jq -nc --arg p "$PROMPT. $STYLESUFFIX$NEGTEXT" '{prompt:$p, steps:4}')
for attempt in 1 2 3; do
  CODE=$(curl -s -o /tmp/cf-resp.json -w '%{http_code}' -X POST "$URL" \
    -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' -d "$REQ") || true
  if [ "$CODE" = 429 ]; then echo "429 rate-limited, waiting 60s (attempt $attempt)"; sleep 60; continue; fi
  break
done
if [ "$CODE" != 200 ]; then echo "cloudflare error HTTP $CODE" >&2; head -c 300 /tmp/cf-resp.json >&2; exit 1; fi
mkdir -p "$(dirname "$OUT")"
jq -r '.result.image' /tmp/cf-resp.json | base64 -d > "$OUT"
echo "[cf] wrote $OUT (flux-1-schnell, 4 steps)"
