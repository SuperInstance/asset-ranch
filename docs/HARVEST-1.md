# HARVEST 1 — Scrapcraft Prop Icons

**Date:** 2026-08-23 · **Campaign:** scrapcraft · **Class:** prop-icon
**Assets:** 10 generated → **8 approved / 2 rejected** · All at 1024×1024 PNG

Recovered mid-harvest after the first session died (it had produced 4 un-cataloged
CF assets; prompts were reconstructed post-hoc and flagged in the manifest).

## Targets

| Asset | Lane used | Verdict |
|---|---|---|
| engine-block.png | cloud-free | approved |
| gear-cluster.png | cloud-free | approved |
| crane-hook.png | cloud-free | approved |
| cat-sticker.png | cloud-free | approved |
| scrap-crate.png | cloud-free | approved |
| oil-drum.png | cloud-free | approved |
| wheel-stack.png | cloud-free (retry) | approved |
| toolbox-cf.png | cloud-free (retry) | approved |
| wheel-stack.local.png | local | **rejected** |
| toolbox.png | local | **rejected** |

## Per-lane results

### CLOUD-FREE — Cloudflare Workers AI `@cf/black-forest-labs/flux-1-schnell`
- **Output:** 8/8 usable. Every asset QC-passed: near-perfect solid backgrounds
  (edge-color spread 1–12/255), strong contrast (162–247), style suffix followed.
- **Speed:** ~2–5 s per image (4 steps). **Cost:** $0 (free Workers AI quota).
- **Auth:** wrangler OAuth fallback (no token env needed); auth never hardcoded.
- **Verdict: the workhorse.** Prompt-faithful, obeys "solid flat background"
  directive, free, fast. Default lane for prop-icon harvests.

### LOCAL — SDXL-Turbo via diffusers (RTX 4050, `~/models/sdxl-turbo`)
- **Output:** 0/2 usable as-is. Both images saturated and chunky (good) but the
  background is busy/textured (edge spread 116–129) — **SDXL-Turbo ignores the
  "solid flat background" directive**, failing the clean-cutout criterion.
- **Speed:** ~82–101 s per image + ~18 s model load per invocation. **Cost:** $0.
- **Bug fixed this session:** `variant="fp16"` crashed (no fp16 files on disk) —
  gen-local.py now falls back to default weights automatically.
- **Note:** SDXL's CLIP encoder truncates prompts at 77 tokens — the global style
  suffix partially drops off. Shorter prompts needed for this lane.
- **Verdict: prototype lane only.** Fine for iterating silhouettes/ideas; final
  harvest assets should come from cloud-free unless we add background-removal
  post-processing (e.g. rembg) for local outputs.

### RESERVED — DeepInfra FLUX-2-max
- **Not used.** Campaign-only, requires Casey's `--nod`. $0 spent.

## Review gate

- `tests/test_catalog.py`: 3/3 pass.
- Flow exercised end-to-end: generate → `catalog.py add` (full provenance in
  `assets/scrapcraft/prop-icon/manifest.json`: prompt, model, lane, seed, date,
  verdict, note) → `catalog.py review` → verdicts recorded.

### Final pass — dual-signal review (2026-08-23, finisher lane)

The first session had no usable vision model (GLM-5V-Turbo not on the Z.ai
plan; MMX vision token plan exhausted). The finisher closed that gap with a
**dual-signal gate**: pixel solidity + local VLM style check.

- **Pixel solidity** (`scripts/qc-solidity.py`, ring sample 3px inside edges):
  approved set stddev **0.4–3.3** (SOLID); rejected locals **23.6–29.7**
  (TEXTURED). Clean separation — the background criterion is settled by pixels.
- **Vision** (local `gemma3:4b` via Ollama, free): all 8 approved assets pass
  style / silhouette-at-64px / cleanliness. The 2 rejected locals pass style
  but fail the background criterion.
- **Calibration note:** small local VLMs (gemma3:4b, llava:7b) over-praise
  background solidity — they called the two textured backgrounds "flat". So the
  VLM is authoritative for *style/silhouette*, the pixel metric for
  *background*; an asset must pass both signals.
- **Outcome: verdicts unchanged** — 8 approved / 2 rejected, now with
  per-asset evidence recorded in the manifest `note` fields.
- Casey's eyeball pass still welcome before assets ship into a game repo.

## Provenance policy

- Prior-lane assets (engine-block, gear-cluster, crane-hook, cat-sticker) were
  generated before the session died un-cataloged; prompts in the manifest are
  **reconstructions**, flagged in each entry's `note` field. Seeds unknown.
- All new assets carry exact prompt + seed (local) or exact prompt (CF lane,
  schnell REST returns no seed).
