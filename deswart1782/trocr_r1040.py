import sys
from pathlib import Path

import cv2
import numpy as np
import torch
from PIL import Image
from transformers import TrOCRProcessor, VisionEncoderDecoderModel


MODEL = "Riksarkivet/trocr-base-handwritten-hist-swe-2"
sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def line_centers(gray):
    # Ignore margins and headings. Connected ink in the central 80% gives a
    # stable row projection for these uniformly ruled cipher lines.
    h, w = gray.shape
    roi = gray[int(h * .25):int(h * .96), int(w * .12):int(w * .90)]
    ink = (roi < 175).sum(axis=1).astype(float)
    ink = np.convolve(ink, np.ones(17), mode="same")
    threshold = max(np.percentile(ink, 70), ink.max() * .17)
    peaks = []
    active = np.where(ink > threshold)[0]
    if len(active):
        groups = np.split(active, np.where(np.diff(active) > 1)[0] + 1)
        for group in groups:
            if len(group) >= 4:
                segment = ink[group]
                peaks.append(int(h * .25) + int(group[np.argmax(segment)]))
    # Merge components belonging to the same handwriting line.
    merged = []
    for y in peaks:
        if not merged or y - merged[-1] > 60:
            merged.append(y)
        elif ink[y - int(h * .25)] > ink[merged[-1] - int(h * .25)]:
            merged[-1] = y
    return merged


def main(path):
    src = cv2.imread(str(path))
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    centers = line_centers(gray)
    print("centers", centers, flush=True)
    processor = TrOCRProcessor.from_pretrained(MODEL, use_fast=False)
    model = VisionEncoderDecoderModel.from_pretrained(MODEL)
    model.eval()
    for number, cy in enumerate(centers, 1):
        crop = gray[max(0, cy - 60):min(gray.shape[0], cy + 65), int(gray.shape[1] * .11):int(gray.shape[1] * .92)]
        crop = cv2.normalize(crop, None, 0, 255, cv2.NORM_MINMAX)
        pixels = processor(images=Image.fromarray(crop).convert("RGB"), return_tensors="pt").pixel_values
        with torch.inference_mode():
            ids = model.generate(pixels, max_new_tokens=220)
        print(f"{number:02d}: {processor.batch_decode(ids, skip_special_tokens=True)[0]}", flush=True)


if __name__ == "__main__":
    main(Path(sys.argv[1]).resolve())
