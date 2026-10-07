"""Render the items of one shard with stable-diffusion.cpp + FLUX.1-schnell (Apache-2.0). Writes PNG + JSON metadata to out/."""
import json, os, subprocess, sys, time
ITEMS = [s for s in os.environ["ITEMS"].split(",") if s]
VARIANTS = int(os.environ.get("VARIANTS", "2")); STEPS = os.environ.get("STEPS", "4")
SIZE = {"busts": (768, 1024), "vistas": (1344, 576)}
SD = os.environ.get("SD_BIN", "./sd/sd-cli"); M = os.environ.get("MODELS", "models")
os.makedirs("out", exist_ok=True)
for it in ITEMS:
    kind, key = it.split(":", 1); d = json.load(open(f"prompts/{kind}.json")); e = d["items"][key]
    prompt = e["line"] + " " + d["style"]; w, h = SIZE[kind]
    for v in range(VARIANTS):
        seed = e["seed"] + v * 1000; name = f"out/{kind}-{key}-s{seed}"
        cmd = [SD, "--diffusion-model", f"{M}/flux.gguf", "--vae", f"{M}/ae.safetensors", "--clip_l", f"{M}/clip_l.safetensors",
               "--t5xxl", f"{M}/t5.gguf", "-p", prompt, "--cfg-scale", "1.0", "--sampling-method", "euler", "--steps", STEPS,
               "-W", str(w), "-H", str(h), "--seed", str(seed), "--vae-tiling", "-o", name + ".png"]
        t = time.time(); print(f"::group::{kind}/{key} seed {seed} ({w}x{h})", flush=True)
        r = subprocess.run(cmd); dt = round(time.time() - t)
        print("::endgroup::", flush=True)
        if r.returncode != 0 or not os.path.exists(name + ".png"):
            print(f"::error::{kind}/{key} seed {seed} failed (exit {r.returncode})"); continue
        json.dump({"kind": kind, "id": key, "seed": seed, "steps": int(STEPS), "size": [w, h], "seconds": dt, "prompt": prompt,
                   "model": "FLUX.1-schnell Q4_K_S GGUF (Apache-2.0)", "runner": os.environ.get("RUNNER_OS", "") + "/" + os.environ.get("RUNNER_ARCH", "")},
                  open(name + ".json", "w"), indent=1)
        print(f"{kind}/{key} seed {seed}: {dt}s", flush=True)
