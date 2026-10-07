"""Contact sheets + an index page for everything in renders/."""
import glob, json, os
from PIL import Image, ImageDraw
os.makedirs("renders/sheets", exist_ok=True)
for kind, (tw, th) in {"busts": (192, 256), "frames": (192, 256), "vistas": (448, 192)}.items():
    files = [f for f in sorted(glob.glob(f"renders/{kind}/*.png")) if os.path.basename(f).count(".") == 1]
    if not files: continue
    cols = 3 if kind == "vistas" else 6; rows = (len(files) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw, rows * (th + 18)), (12, 12, 12)); dr = ImageDraw.Draw(sheet)
    for i, f in enumerate(files):
        im = Image.open(f).convert("RGB"); im.thumbnail((tw, th)); x, y = (i % cols) * tw, (i // cols) * (th + 18)
        sheet.paste(im, (x, y)); dr.text((x + 4, y + th + 3), os.path.basename(f)[:-4], fill=(200, 190, 170))
    sheet.save(f"renders/sheets/{kind}.jpg", quality=88)
rows = []
for j in sorted(glob.glob("renders/*/*.json")):
    m = json.load(open(j)); rows.append(f"| {m['kind']} | {m['id']} | {m['seed']} | {m['seconds']}s | ![]({os.path.relpath(j[:-5] + '.png', 'renders')}) |")
open("renders/README.md", "w").write("# Renders\n\nFLUX.1-schnell (Apache-2.0) via stable-diffusion.cpp on GitHub-hosted runners.\n\n![busts](sheets/busts.jpg)\n\n![vistas](sheets/vistas.jpg)\n\n| kind | id | seed | time | image |\n|---|---|---|---|---|\n" + "\n".join(rows) + "\n")
