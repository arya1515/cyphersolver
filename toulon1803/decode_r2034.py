#!/usr/bin/env python3
"""Decode the hand transcription of DECODE R2034 with Croiset's R1035 key."""

from __future__ import annotations

import csv
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
CODEBOOK = HERE / "oterleek_codes" / "Codebook" / "Nomenclator.csv"
TRANSCRIPTION = HERE / "transcription.txt"


def load_codebook() -> dict[str, str]:
    with CODEBOOK.open(encoding="utf-8", newline="") as handle:
        return {row[0].strip(): row[1] for row in csv.reader(handle) if len(row) >= 2}


def load_lines() -> list[list[str]]:
    lines: list[list[str]] = []
    for raw in TRANSCRIPTION.read_text(encoding="utf-8").splitlines():
        raw = raw.strip()
        if raw and not raw.startswith("#"):
            lines.append(raw.split())
    return lines


def decode_token(token: str, codebook: dict[str, str]) -> dict[str, object]:
    has_suffix = token.endswith("-")
    base = token[:-1] if has_suffix else token
    meaning = codebook.get(base)
    return {
        "code": token,
        "meaning": meaning,
        "suffix": has_suffix,
        "rendered": None if meaning is None else meaning + ("-en" if has_suffix else ""),
    }


def main() -> None:
    codebook = load_codebook()
    decoded_lines = [
        [decode_token(token, codebook) for token in line] for line in load_lines()
    ]
    for number, line in enumerate(decoded_lines, 1):
        print(f"L{number}: " + " | ".join(
            f"{item['code']}={item['rendered'] or '???'}" for item in line
        ))
    (HERE / "decoded_tokens.json").write_text(
        json.dumps(decoded_lines, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
