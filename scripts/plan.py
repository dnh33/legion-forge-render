"""Build the job matrix: split the selected prompt items into N shards (one model download per shard)."""
import json, os, sys
sel = os.environ.get("SET", "all"); only = [s.strip() for s in os.environ.get("ONLY", "").split(",") if s.strip()]
shards = max(1, int(os.environ.get("SHARDS", "12")))
items = []
for kind in (["busts", "vistas"] if sel == "all" else [sel]):  # frames = style-frame exploration set
    d = json.load(open(f"prompts/{kind}.json"))
    for k in d["items"]:
        if not only or k in only:
            for v in range(max(1, int(os.environ.get("VARIANTS", "1")))): items.append(f"{kind}:{k}:{v}")  # one job slot per image
if not items: sys.exit("No items match SET/ONLY")
shards = min(shards, len(items))
groups = [items[i::shards] for i in range(shards)]
out = json.dumps({"include": [{"shard": i, "items": ",".join(g)} for i, g in enumerate(groups)]})
print(out)
with open(os.environ["GITHUB_OUTPUT"], "a") as f: f.write(f"matrix={out}\n")
