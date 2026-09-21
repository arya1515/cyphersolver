"""Crop a source image for close visual inspection."""

from pathlib import Path
import sys

from PIL import Image, ImageEnhance


source = Path(sys.argv[1])
box = tuple(map(int, sys.argv[2:6]))
destination = Path(sys.argv[6])
crop = Image.open(source).convert("RGB").crop(box)
crop = ImageEnhance.Contrast(crop).enhance(1.2)
crop.save(destination, quality=96)
print(destination)
