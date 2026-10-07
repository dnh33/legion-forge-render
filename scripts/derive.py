"""Derive animation layers from each render: cut-out (rembg, u2net), depth map (Depth-Anything V2 Small, Apache-2.0)
and a glow mask (optics, candles, coals). Writes <name>.cut.png, <name>.depth.png, <name>.glow.png next to <name>.png.
Busts get all three; vistas get depth only (for parallax). Skips files that already have their layers."""
import glob, os, sys
import numpy as np
from PIL import Image, ImageFilter
root = sys.argv[1] if len(sys.argv) > 1 else "renders"
files = [f for f in sorted(glob.glob(f"{root}/**/*.png", recursive=True)) if f.count(".") == 1 and "/sheets/" not in f]
todo = [f for f in files if not os.path.exists(f[:-4] + ".depth.png")]
if not todo: print("nothing to derive"); sys.exit(0)
from transformers import pipeline
depth = pipeline("depth-estimation", model="depth-anything/Depth-Anything-V2-Small-hf", device="cpu")
from rembg import remove, new_session
seg = new_session("u2net")
for f in todo:
    im = Image.open(f).convert("RGB"); base = f[:-4]; bust = os.path.basename(f).startswith(("busts-", "frames-"))
    d = depth(im)["depth"].resize(im.size, Image.BICUBIC)
    a = np.asarray(d).astype(np.float32); a = (a - a.min()) / max(1e-6, a.max() - a.min())
    Image.fromarray((a * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.5)).save(base + ".depth.png")
    if bust:
        remove(im, session=seg, post_process_mask=True).save(base + ".cut.png")
        hsv = np.asarray(im.convert("HSV")).astype(np.float32) / 255.0
        rgb = np.asarray(im).astype(np.float32) / 255.0
        v, s = hsv[..., 2], hsv[..., 1]
        lum = rgb @ np.array([.2126, .7152, .0722])
        local = np.asarray(Image.fromarray((lum * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(24))).astype(np.float32) / 255.0
        glow = np.clip((v - .72) / .2, 0, 1) * np.clip((s - .25) / .4, 0, 1) * np.clip((lum - local - .12) / .25, 0, 1)
        g = Image.fromarray((glow * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(3))
        g.save(base + ".glow.png")
    print("derived", f, flush=True)
