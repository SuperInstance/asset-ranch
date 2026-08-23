#!/usr/bin/env python3
"""Catalog + review gate for generated assets.

manifest.json lives at assets/<campaign>/<class>/manifest.json. Each entry:
  id, file, prompt, model, lane, seed, date, verdict (pending|approved|rejected), note

Commands:
  add    --dir assets/c/prop --file x.png --prompt "..." --model m --lane L [--seed N]
  review <id> --dir assets/c/prop --verdict approve|reject [--note "..."]
  status [--dir assets/c/prop] [--pending-only]
"""
import argparse, datetime, json, os, sys, uuid

VERDICTS = ("pending", "approved", "rejected")

def manifest_path(d):
    return os.path.join(d, "manifest.json")

def load(d):
    p = manifest_path(d)
    if os.path.exists(p):
        with open(p) as f:
            return json.load(f)
    return {"assets": []}

def save(d, m):
    os.makedirs(d, exist_ok=True)
    with open(manifest_path(d), "w") as f:
        json.dump(m, f, indent=2)

def cmd_add(a):
    d = a.dir
    if not os.path.exists(os.path.join(d, a.file)):
        sys.exit(f"file not found: {os.path.join(d, a.file)}")
    m = load(d)
    entry = {
        "id": uuid.uuid4().hex[:12],
        "file": a.file,
        "prompt": a.prompt,
        "model": a.model,
        "lane": a.lane,
        "seed": a.seed,
        "date": datetime.date.today().isoformat(),
        "verdict": "pending",
        "note": "",
    }
    m["assets"].append(entry)
    save(d, m)
    print(entry["id"])

def cmd_review(a):
    m = load(a.dir)
    for e in m["assets"]:
        if e["id"] == a.id:
            verdict = a.verdict.lower()
            if verdict in ("approve", "approved"):
                verdict = "approved"
            elif verdict in ("reject", "rejected"):
                verdict = "rejected"
            elif verdict == "pending":
                verdict = "pending"
            else:
                sys.exit(f"verdict must be one of {VERDICTS} (or approve/reject)")
            if e["verdict"] != "pending" and verdict != e["verdict"]:
                sys.exit(f"already reviewed as {e['verdict']}; refusing to flip without --force")
            e["verdict"] = verdict
            e["note"] = a.note or e["note"]
            save(a.dir, m)
            print(f"{e['id']}: {e['verdict']}")
            return
    sys.exit(f"id not found: {a.id}")

def cmd_status(a):
    dirs = [a.dir] if a.dir else []
    if not dirs:
        root = "assets"
        for camp in sorted(os.listdir(root)) if os.path.isdir(root) else []:
            for cls in sorted(os.listdir(os.path.join(root, camp))):
                p = os.path.join(root, camp, cls)
                if os.path.exists(manifest_path(p)):
                    dirs.append(p)
    for d in dirs:
        m = load(d)
        for e in m["assets"]:
            if a.pending_only and e["verdict"] != "pending":
                continue
            print(f"{e['id']}  {e['verdict']:9} {e['lane']:11} {e['file']}")

def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("add")
    p.add_argument("--dir", required=True)
    p.add_argument("--file", required=True)
    p.add_argument("--prompt", required=True)
    p.add_argument("--model", required=True)
    p.add_argument("--lane", required=True, choices=["local", "cloud-free", "reserved"])
    p.add_argument("--seed", type=int, default=None)
    p.set_defaults(fn=cmd_add)
    p = sub.add_parser("review")
    p.add_argument("id")
    p.add_argument("--dir", required=True)
    p.add_argument("--verdict", required=True)
    p.add_argument("--note", default="")
    p.add_argument("--force", action="store_true")
    p.set_defaults(fn=cmd_review)
    p = sub.add_parser("status")
    p.add_argument("--dir")
    p.add_argument("--pending-only", action="store_true")
    p.set_defaults(fn=cmd_status)
    a = ap.parse_args()
    a.fn(a)

if __name__ == "__main__":
    main()
