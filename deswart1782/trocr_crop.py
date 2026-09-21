import argparse
from pathlib import Path

import cv2
import torch
from PIL import Image
from transformers import TrOCRProcessor, VisionEncoderDecoderModel

MODEL = "Riksarkivet/trocr-base-handwritten-hist-swe-2"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("image")
    ap.add_argument("x", type=int)
    ap.add_argument("y", type=int)
    ap.add_argument("w", type=int)
    ap.add_argument("h", type=int)
    args = ap.parse_args()

    processor = TrOCRProcessor.from_pretrained(MODEL, use_fast=False)
    model = VisionEncoderDecoderModel.from_pretrained(MODEL)
    model.eval()
    src = cv2.imread(str(Path(args.image)))
    crop = src[args.y:args.y + args.h, args.x:args.x + args.w]
    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    gray = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)
    image = Image.fromarray(gray).convert("RGB")
    pixels = processor(images=image, return_tensors="pt").pixel_values
    with torch.inference_mode():
        ids = model.generate(pixels, max_new_tokens=64, num_beams=5)
    print(processor.batch_decode(ids, skip_special_tokens=True)[0])


if __name__ == "__main__":
    main()
