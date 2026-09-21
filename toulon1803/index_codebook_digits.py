#!/usr/bin/env python3
"""Build a rough digit-location index for the handwritten 1803 codebook."""

from __future__ import annotations

import json
from pathlib import Path

import easyocr


HERE = Path(__file__).resolve().parent
SCANS = HERE / "key1035"
OUTPUT = HERE / "codebook_digit_index.json"


def main() -> None:
    reader = easyocr.Reader(["en"], gpu=False)
    indexed: dict[str, list[dict[str, object]]] = {}
    for page in range(3, 19):
        path = SCANS / f"IMG_R1035_I45339_P{page}.jpg"
        print(f"OCR page {page}...", flush=True)
        found = reader.readtext(
            str(path),
            detail=1,
            paragraph=False,
            canvas_size=4096,
            mag_ratio=1.0,
            allowlist="0123456789",
        )
        indexed[str(page)] = [
            {
                "box": [[float(x), float(y)] for x, y in box],
                "text": text,
                "confidence": float(confidence),
            }
            for box, text, confidence in found
        ]
        OUTPUT.write_text(
            json.dumps(indexed, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"Page {page}: {len(found)} detections", flush=True)


if __name__ == "__main__":
    main()
