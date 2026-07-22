"""
Redact donor-name text baked into HDF well photos.

Approach: heavy Gaussian blur + downsample/upsample pixelation over specific
rectangles. Redaction is baked into the output JPG so the source pixels no
longer contain the text.

Coordinates are estimates from a first look at the images — expect to iterate.
Run:  python3 scripts/redact_names.py
Outputs land in photos/ so the site can serve them at photos/<id>.jpg.
"""
from pathlib import Path
from PIL import Image, ImageFilter

REPO = Path(__file__).resolve().parent.parent
PHOTOS = REPO / "photos"
PHOTOS.mkdir(exist_ok=True)


def redact_region(im: Image.Image, box: tuple[int, int, int, int]) -> None:
    """Blur + pixelate the given (x0, y0, x1, y1) region in-place."""
    x0, y0, x1, y1 = box
    region = im.crop(box)
    # Pixelate: downsample then upsample with nearest-neighbor
    w, h = region.size
    small = region.resize((max(1, w // 40), max(1, h // 40)), Image.BILINEAR)
    pixelated = small.resize((w, h), Image.NEAREST)
    # Then a heavy blur so pixel edges disappear
    blurred = pixelated.filter(ImageFilter.GaussianBlur(radius=18))
    im.paste(blurred, box)


# Coordinates for the two 4000x2252 frames. Format: (x0, y0, x1, y1).
# Coords picked from a coordinate-grid overlay on the source (scripts/grid_debug.py).
# Banner region — covers "Sadaqah Jariah for / Usama Khan And / Mohammad Asmat Khan"
# but leaves "WATER For Tomorrow" and "AFGHANISTAN 2025" visible.
BANNER_BOX_IMG1 = (800, 720, 1550, 1030)
BANNER_BOX_IMG2 = (50, 1050, 920, 1390)
# Commemorative plaque on the well body — cover the entire plaque text area.
PLAQUE_BOX_IMG1 = (1830, 1240, 2680, 1780)
PLAQUE_BOX_IMG2 = (1780, 1490, 2480, 1980)

jobs = [
    ("AfghanistanWell.jpg", "AFG-001.jpg", [BANNER_BOX_IMG1, PLAQUE_BOX_IMG1]),
    ("AfghanistanWell-People.jpg", "AFG-001-crowd.jpg", [BANNER_BOX_IMG2, PLAQUE_BOX_IMG2]),
]

for src_name, out_name, boxes in jobs:
    im = Image.open(REPO / src_name).convert("RGB")
    for b in boxes:
        redact_region(im, b)
    out_path = PHOTOS / out_name
    im.save(out_path, "JPEG", quality=88, optimize=True)
    print(f"wrote {out_path.relative_to(REPO)}  ({out_path.stat().st_size // 1024} KB)")
