"""Draw a coordinate grid + labeled rulers on a source image so we can pick
precise redaction rectangles. Output goes to /tmp so it doesn't pollute repo."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

REPO = Path(__file__).resolve().parent.parent

for src in ["AfghanistanWell.jpg", "AfghanistanWell-People.jpg"]:
    im = Image.open(REPO / src).convert("RGB")
    W, H = im.size
    draw = ImageDraw.Draw(im, "RGBA")
    step = 200
    for x in range(0, W, step):
        draw.line([(x, 0), (x, H)], fill=(255, 0, 255, 180), width=2)
        draw.text((x + 4, 4), str(x), fill=(255, 0, 255, 255))
    for y in range(0, H, step):
        draw.line([(0, y), (W, y)], fill=(0, 255, 255, 180), width=2)
        draw.text((4, y + 2), str(y), fill=(0, 255, 255, 255))
    out = Path("/tmp") / f"grid-{src}"
    im.save(out, "JPEG", quality=70)
    print(out)
