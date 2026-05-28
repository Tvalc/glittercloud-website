from PIL import Image, ImageFilter
from pathlib import Path

root = Path(r"c:\Users\19415\Desktop\Cursor\glittercloud-website\assets\gc")

leaf = Image.open(root / "LeaflyBanner.webp").convert("RGB")
conv = Image.open(root / "ConvoyBanner.jpg").convert("RGB")
W, H = 1600, 900
leaf = leaf.resize((W, H), Image.Resampling.LANCZOS)
conv = conv.resize((W, H), Image.Resampling.LANCZOS)
mask = Image.new("L", (W, H), 0)
mp = mask.load()
for x in range(W):
    if x < int(W * 0.35):
        v = 255
    elif x > int(W * 0.65):
        v = 0
    else:
        t = (x - W * 0.35) / (W * 0.30)
        v = int(255 * (1 - t))
    for y in range(H):
        mp[x, y] = v
blend = Image.composite(leaf, conv, mask)
blend = blend.filter(ImageFilter.UnsharpMask(radius=1.2, percent=120, threshold=3))
blend.save(root / "leafly-convoy-blend.png", optimize=True)

# Founder: Shrapnel + Makko only — two equal panels
founder_imgs = [
    Image.open(root / "ShrapnelBanner.jpg").convert("RGB"),
    Image.open(root / "MakkoBanner.png").convert("RGB"),
]
canvas_w, canvas_h = 1800, 1200
cell_w = canvas_w // 2
canvas = Image.new("RGB", (canvas_w, canvas_h), (10, 10, 10))
for i, img in enumerate(founder_imgs):
    panel = img.resize((cell_w, canvas_h), Image.Resampling.LANCZOS)
    canvas.paste(panel, (i * cell_w, 0))

v = Image.new("L", canvas.size, 0)
vp = v.load()
cx, cy = canvas.size[0] // 2, canvas.size[1] // 2
maxd = (cx ** 2 + cy ** 2) ** 0.5
for x in range(canvas.size[0]):
    for y in range(canvas.size[1]):
        d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
        val = max(0, min(100, int((d / maxd) * 120) - 20))
        vp[x, y] = val
shade = Image.new("RGB", canvas.size, (0, 0, 0))
canvas = Image.composite(shade, canvas, v)
canvas = canvas.filter(ImageFilter.UnsharpMask(radius=1.0, percent=130, threshold=2))
canvas.save(root / "founder-collage.png", optimize=True)

print("generated")
