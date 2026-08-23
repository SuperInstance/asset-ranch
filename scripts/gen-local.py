#!/usr/bin/env python3
"""LOCAL lane: SDXL-Turbo via diffusers on the RTX 4050. Free, unlimited.

Usage: gen-local.py --prompt "..." --out file.png [--neg "..."] [--steps 4] [--seed N] [--size 1024x1024]
"""
import argparse, os, time

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--neg", default="photorealistic, photographic, noise, grain, gritty, "
        "thin spindly parts, cinematic depth of field, harsh shadows, text, watermark, "
        "cluttered background, complex shading, subsurface scattering")
    ap.add_argument("--out", required=True)
    ap.add_argument("--steps", type=int, default=4)
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--size", default="1024x1024")
    args = ap.parse_args()

    import torch
    from diffusers import AutoPipelineForText2Image

    w, h = (int(x) for x in args.size.lower().split("x"))
    model = os.path.expanduser("~/models/sdxl-turbo")
    kwargs = dict(torch_dtype=torch.float16)
    try:
        pipe = AutoPipelineForText2Image.from_pretrained(model, variant="fp16", **kwargs)
    except ValueError as e:
        if "variant" not in str(e):
            raise
        print("[local] no fp16 variant on disk — loading default weights", flush=True)
        pipe = AutoPipelineForText2Image.from_pretrained(model, **kwargs)
    try:
        pipe.to("cuda")
    except torch.cuda.OutOfMemoryError:
        print("[local] CUDA OOM at load — falling back to sequential CPU offload", flush=True)
        del pipe
        pipe = AutoPipelineForText2Image.from_pretrained(model, torch_dtype=torch.float16)
        pipe.enable_sequential_cpu_offload()
    pipe.set_progress_bar_config(disable=True)

    gen = torch.Generator("cuda" if torch.cuda.is_available() else "cpu")
    if args.seed is not None:
        gen = gen.manual_seed(args.seed)

    t0 = time.time()
    img = pipe(prompt=args.prompt, negative_prompt=args.neg, num_inference_steps=args.steps,
               guidance_scale=0.0, width=w, height=h, generator=gen).images[0]
    dt = time.time() - t0
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    img.save(args.out)
    print(f"[local] wrote {args.out} ({dt:.1f}s, steps={args.steps}, size={w}x{h})")

if __name__ == "__main__":
    main()
