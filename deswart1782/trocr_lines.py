from pathlib import Path

import cv2
import torch
from PIL import Image
from transformers import TrOCRProcessor, VisionEncoderDecoderModel

ROOT = Path(__file__).resolve().parent
MODEL = "Riksarkivet/trocr-base-handwritten-hist-swe-2"


def main():
    processor = TrOCRProcessor.from_pretrained(MODEL, use_fast=False)
    model = VisionEncoderDecoderModel.from_pretrained(MODEL)
    model.eval()
    src = cv2.imread(str(ROOT / "R2045_p1_upright.png"))
    # Baselines of the decipherment paragraph, measured on the 3648x5472 scan.
    centers = [1070, 1250, 1430, 1610, 1790, 1970, 2150, 2330,
               2510, 2690, 2870, 3050, 3230, 3410, 3590]
    for n, cy in enumerate(centers, 1):
        crop = src[max(0, cy - 105):cy + 105, 780:3500]
        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
        gray = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)
        image = Image.fromarray(gray).convert("RGB")
        pixels = processor(images=image, return_tensors="pt").pixel_values
        with torch.inference_mode():
            ids = model.generate(pixels, max_new_tokens=160)
        text = processor.batch_decode(ids, skip_special_tokens=True)[0]
        print(f"{n:02d}: {text}")


if __name__ == "__main__":
    main()
