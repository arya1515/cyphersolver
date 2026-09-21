"""Rotate DECODE R1944 scans for close reading and comparison with R2034."""

from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "bordeaux" / "decode"
OUTPUT = Path(__file__).resolve().parent


records = {
    1944: range(13409, 13411),
    1945: range(13411, 13415),
    1946: range(13415, 13419),
}

for record, image_ids in records.items():
    for page, image_id in enumerate(image_ids, 1):
        source = SOURCE / f"IMG_R{record}_I{image_id}_P{page}.png"
        image = Image.open(source)
        upright = image.rotate(-90, expand=True)
        gray = ImageOps.grayscale(upright)
        enhanced = ImageEnhance.Contrast(gray).enhance(1.8)
        enhanced.save(OUTPUT / f"R{record}_P{page}_upright.png")


# Line crops for exact transcription of the R1946 known-plaintext ciphertext.
line_bands = {
    4: [(2420 + 310 * i, 2420 + 310 * (i + 1)) for i in range(7)],
    1: [(790 + 315 * i, 790 + 315 * (i + 1)) for i in range(13)],
}
for page, bands in line_bands.items():
    image = Image.open(OUTPUT / f"R1946_P{page}_upright.png")
    for line, (top, bottom) in enumerate(bands, 1):
        crop = image.crop((350, top, image.width - 150, bottom))
        crop.save(OUTPUT / f"R1946_P{page}_L{line:02d}.png")


# Line crops for the longer R1945 known-plaintext pair.  The first cipher
# sheet has eight lines; the continuation has eleven full lines and a short
# final line.
r1945_line_bands = {
    2: [(2320 + 315 * i, 2320 + 315 * (i + 1)) for i in range(8)],
    3: [(760 + 345 * i, 760 + 345 * (i + 1)) for i in range(12)],
}
for page, bands in r1945_line_bands.items():
    image = Image.open(OUTPUT / f"R1945_P{page}_upright.png")
    for line, (top, bottom) in enumerate(bands, 1):
        crop = image.crop((350, top, image.width - 150, bottom))
        crop.save(OUTPUT / f"R1945_P{page}_L{line:02d}.png")
