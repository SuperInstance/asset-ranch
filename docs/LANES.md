# THE THREE LANES — policy + setup

Spending doctrine: burn free lanes freely; the reserved lane costs real money
and stays behind an explicit gate.

---

## Lane A — LOCAL (free, unlimited)

**Runtime:** SDXL-Turbo (diffusers pipeline) on the local RTX 4050.
**Model:** `~/models/sdxl-turbo` (full diffusers layout — verified present).
**Stack:** python3 + torch 2.13 cu130 + diffusers 0.39 (verified installed).

- Script: `scripts/gen-local.py` (+ `scripts/gen-local.sh` wrapper)
- Turbo = 1–4 steps, no CFG; expect ~20–60 s/image on the 4050.
- Turbo leans photoreal — the style suffix + negative prompt do the steering;
  expect to re-roll more often than on flux-schnell.
- VRAM note: 6 GB class GPU → the script runs fp16 with sequential CPU
  offload fallback if OOM.

## Lane B — CLOUD-FREE (Cloudflare Workers AI)

**Model:** `@cf/black-forest-labs/flux-1-schnell` — better prompt fidelity
than turbo, still free quota. Verified working 2026-08-23.

- Script: `scripts/gen-cf.sh`
- Auth (in order of preference, never hardcoded):
  1. `CLOUDFLARE_API_TOKEN` + `CLOUDFLARE_ACCOUNT_ID` env vars
     (token needs *Workers AI: Edit*). Create at
     dash.cloudflare.com → My Profile → API Tokens.
  2. Fallback: wrangler OAuth token from `~/.config/.wrangler/config/default.toml`
     (works with the currently-logged-in account; account id auto-detected
     via `wrangler whoami`). This is what the first harvest used.
- Output is JPEG bytes base64-wrapped in JSON; script unwraps to a real file.

## Lane C — RESERVED (DeepInfra FLUX-2-max)

**Cost: real money. Campaign-grade only, with Casey's explicit nod.**

- Script: `scripts/gen-deepinfra.sh` — refuses to run without the literal
  `--nod` flag and prints a reminder of what it costs.
- Known gotcha: FLUX-2-max rejects width > 1440 → always pass explicit
  `--size 1280x720` style sizes, never bare aspect ratios.
- Auth: `DEEPINFRA_API_KEY` env (exists in the fleet environment; never committed).

---

## Policy

- Default routing: iterate LOCAL → polish with CLOUD-FREE → RESERVED only for
  campaign hero assets after free lanes plateau.
- Every generation, any lane, goes through `scripts/catalog.py` and starts
  at verdict `pending`. No pending asset enters a game repo.
