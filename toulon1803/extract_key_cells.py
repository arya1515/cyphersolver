#!/usr/bin/env python3
"""Extract the R1035 manuscript cell corresponding to each R2034 code group."""

from __future__ import annotations

import csv
import re
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFont
from scipy.signal import find_peaks


HERE = Path(__file__).resolve().parent
SCANS = HERE / "oterleek_codes" / "Scans" / "Codebook"
CODEBOOK = HERE / "oterleek_codes" / "Codebook" / "Nomenclator.csv"
TRANSCRIPTION = HERE / "transcription.txt"
MARKER_ORDER = {"~": 0, '"': 1, "^": 2, "": 3, ":": 4, "+": 5, "=": 6}


def load_known() -> dict[str, str]:
    with CODEBOOK.open(encoding="utf-8", newline="") as handle:
        return {row[0].strip(): row[1] for row in csv.reader(handle) if len(row) >= 2}


def tokens_through_end_marker() -> list[str]:
    tokens: list[str] = []
    for raw in TRANSCRIPTION.read_text(encoding="utf-8").splitlines():
        if not raw.strip() or raw.startswith("#"):
            continue
        for token in raw.split():
            tokens.append(token)
            if token.rstrip("-") == "763~":
                return tokens
    return tokens


def token_lines_through_end_marker() -> list[list[str]]:
    result: list[list[str]] = []
    for raw in TRANSCRIPTION.read_text(encoding="utf-8").splitlines():
        if not raw.strip() or raw.startswith("#"):
            continue
        line: list[str] = []
        for token in raw.split():
            line.append(token.rstrip("-"))
            if token.rstrip("-") == "763~":
                result.append(line)
                return result
        result.append(line)
    return result


def parse_code(token: str) -> tuple[int, str]:
    base = token.rstrip("-")
    match = re.fullmatch(r"(\d+)([~\"^:+=]?)", base)
    if not match:
        raise ValueError(token)
    return int(match.group(1)), match.group(2)


def red_mask(image: Image.Image) -> np.ndarray:
    rgb = np.asarray(image.convert("RGB")).astype(np.int16)
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    return (r - g > 15) & (r - b > 12) & (r > 70) & (g < 210)


def row_grid(mask: np.ndarray) -> np.ndarray:
    projection = mask[:, 200:2800].sum(axis=1)
    peaks, _ = find_peaks(projection, distance=30, prominence=70)
    candidates = np.array([int(y) for y in peaks if projection[y] > 250])
    top_candidates = [y for y in candidates if 50 < y < 350]
    if not top_candidates:
        raise RuntimeError("horizontal table grid not detected")
    top = float(min(top_candidates))
    gaps = np.diff(candidates)
    row_height = float(np.median(gaps[(gaps > 38) & (gaps < 68)]))
    predicted = top + np.arange(72) * row_height

    # Iteratively assign observed red rules to their nearest expected grid index,
    # then fit a quadratic to accommodate the page's gentle camera distortion.
    for _ in range(4):
        assignments: dict[int, int] = {}
        for y in candidates:
            index = int(np.argmin(np.abs(predicted - y)))
            if abs(predicted[index] - y) > row_height * .4:
                continue
            old = assignments.get(index)
            if old is None or projection[y] > projection[old]:
                assignments[index] = int(y)
        indexes = np.array(sorted(assignments))
        observed = np.array([assignments[i] for i in indexes])
        if len(indexes) < 38:
            raise RuntimeError("horizontal table grid fit failed")
        coefficients = np.polyfit(indexes, observed, 2)
        predicted = np.polyval(coefficients, np.arange(72))
    return predicted


def column_lines(mask: np.ndarray, y: float, row_height: float) -> list[int]:
    """Return alternating outer/divider grid lines for the five wide columns."""
    center = int(y)
    radius = max(80, int(row_height * 2.2))
    band = mask[max(0, center - radius):min(mask.shape[0], center + radius)]
    projection = band.sum(axis=0)
    peaks, _ = find_peaks(projection, distance=30, prominence=20)
    strong = [int(x) for x in peaks if 150 < x < 2900 and projection[x] > band.shape[0] * .40]

    # A valid run has alternating wide word cells and narrow number cells.
    best: tuple[float, list[int]] | None = None
    for start in range(max(1, len(strong) - 10)):
        run = strong[start:start + 11]
        if len(run) != 11:
            continue
        gaps = np.diff(run)
        wide, narrow = gaps[0::2], gaps[1::2]
        if not (280 < np.median(wide) < 450 and 60 < np.median(narrow) < 150):
            continue
        score = float(np.std(wide) + np.std(narrow))
        if best is None or score < best[0]:
            best = (score, run)
    if best is None:
        raise RuntimeError(f"vertical table grid not detected: {strong}")
    return best[1]


def locate(token: str) -> tuple[int, int, int]:
    number, marker = parse_code(token)
    # Each alphabet carries 999 numbered entries (1..999), not a 000/1000
    # slot.  Treating the sections as 1000 wide drifts one cell at every
    # marker transition and produces plausible-looking but wrong neighbours.
    global_number = MARKER_ORDER[marker] * 999 + number
    position = global_number - 37
    if position < 0:
        raise ValueError(f"code precedes photographed table: {token}")
    page, offset = divmod(position, 385)
    macro_column, local = divmod(offset, 77)
    return page, macro_column, local


def extract_cell(token: str) -> Image.Image:
    page, macro, local = locate(token)
    image = Image.open(SCANS / f"IMG_{4078 + page}.jpg").convert("RGB")
    mask = red_mask(image)
    rows = row_grid(mask)
    row_height = float(np.median(np.diff(rows)))
    top = float(rows[0])

    if local < 12:
        half = local // 6
        row = local % 6
    else:
        row = local - 6
    y0, y1 = float(rows[row]), float(rows[row + 1])
    # Use a nearby full-width row to recover the stable outer/divider lines.
    grid_y = max(y0 + row_height / 2, top + 8.5 * row_height)
    lines = column_lines(mask, grid_y, row_height)
    macro_left, word_right, macro_right = lines[macro * 2:macro * 2 + 3]
    macro_width = macro_right - macro_left
    if local < 12:
        half_width = macro_width / 2
        x0 = macro_left + half * half_width
        x1 = x0 + half_width
    else:
        x0, x1 = macro_left, macro_right

    pad_x, pad_y = macro_width * 0.02, row_height * 0.13
    box = (
        max(0, int(x0 - pad_x)), max(0, int(y0 - pad_y)),
        min(image.width, int(x1 + pad_x)), min(image.height, int(y1 + pad_y)),
    )
    crop = image.crop(box)
    crop = ImageEnhance.Contrast(crop).enhance(1.25)
    crop = ImageEnhance.Sharpness(crop).enhance(1.5)
    crop.thumbnail((620, 105))
    return crop


def extract_context(token: str) -> Image.Image:
    page, macro, local = locate(token)
    image = Image.open(SCANS / f"IMG_{4078 + page}.jpg").convert("RGB")
    mask = red_mask(image)
    rows = row_grid(mask)
    row_height = float(np.median(np.diff(rows)))
    top = float(rows[0])
    if local < 12:
        row = local % 6
        y0, y1 = rows[0], rows[6]
    else:
        row = local - 6
        y0 = rows[max(0, row - 3)]
        y1 = rows[min(71, row + 10)]
    grid_y = max(float(rows[row]) + row_height / 2, top + 8.5 * row_height)
    lines = column_lines(mask, grid_y, row_height)
    macro_left, _, macro_right = lines[macro * 2:macro * 2 + 3]
    pad_x = (macro_right - macro_left) * .03
    box = (
        max(0, int(macro_left - pad_x)), max(0, int(y0 - row_height * .15)),
        min(image.width, int(macro_right + pad_x)), min(image.height, int(y1 + row_height * .15)),
    )
    crop = image.crop(box)
    crop = ImageEnhance.Contrast(crop).enhance(1.2)
    crop.thumbnail((820, 350))
    return crop


def main() -> None:
    known = load_known()
    unique: list[str] = []
    seen: set[str] = set()
    for token in tokens_through_end_marker():
        base = token.rstrip("-")
        if base not in seen:
            unique.append(base)
            seen.add(base)

    tile_w, tile_h = 700, 145
    tiles: list[Image.Image] = []
    for token in unique:
        tile = Image.new("RGB", (tile_w, tile_h), "white")
        draw = ImageDraw.Draw(tile)
        page, macro, local = locate(token)
        label = f"{token}  IMG_{4078 + page}  col {macro + 1} local {local}"
        if token in known:
            label += f"  KNOWN: {known[token]}"
        draw.text((8, 5), label, fill="black")
        try:
            cell = extract_cell(token)
            tile.paste(cell, (8, 32))
        except Exception as exc:  # keep the contact sheet useful if one crop fails
            draw.text((8, 45), f"ERROR: {exc}", fill="red")
        tiles.append(tile)

    cols = 3
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (tile_w * cols, tile_h * rows), "white")
    for index, tile in enumerate(tiles):
        sheet.paste(tile, ((index % cols) * tile_w, (index // cols) * tile_h))
    output = HERE / "key_cells_contact.jpg"
    sheet.save(output, quality=95)
    print(f"wrote {output} ({len(tiles)} unique code groups)")

    for line_number, tokens in enumerate(token_lines_through_end_marker(), 1):
        context_tiles: list[Image.Image] = []
        for token in tokens:
            tile = Image.new("RGB", (900, 420), "white")
            draw = ImageDraw.Draw(tile)
            page, macro, local = locate(token)
            draw.text((8, 5), f"TARGET {token}  IMG_{4078 + page}  col {macro + 1} local {local}", fill="black")
            try:
                context = extract_context(token)
                tile.paste(context, (8, 34))
            except Exception as exc:
                draw.text((8, 50), f"ERROR: {exc}", fill="red")
            context_tiles.append(tile)
        context_rows = (len(context_tiles) + 1) // 2
        context_sheet = Image.new("RGB", (1800, 420 * context_rows), "white")
        for index, tile in enumerate(context_tiles):
            context_sheet.paste(tile, ((index % 2) * 900, (index // 2) * 420))
        context_output = HERE / f"key_context_line{line_number:02d}.jpg"
        context_sheet.save(context_output, quality=95)
        print(f"wrote {context_output}")


if __name__ == "__main__":
    main()
