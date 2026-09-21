"""Decode Van Reede's 1787-1788 dispatches with DECODE key R1024."""

from pathlib import Path
import re


ROOT = Path(__file__).parent
DECODE = ROOT / "decode"


def load_key() -> dict[int, str]:
    text = (DECODE / "DOC_R1024_D2881_2881.txt").read_text(
        encoding="utf-8", errors="replace"
    )
    key = {}
    for line in text.splitlines():
        match = re.match(r"^\s*(\d+)\s+-\s+(.*?)\s*$", line)
        if match:
            key[int(match.group(1))] = match.group(2)
    return key


def base_group(raw: str) -> int | None:
    raw = raw.replace("J+", "3").replace("J", "3")
    raw = re.sub(r"\{.*?\}|\^\S*|_+|[^0-9?]", "", raw)
    if "?" in raw or not raw:
        return None
    return int(raw)


def decode_document(record: int, filename: str, key: dict[int, str]) -> None:
    source = (DECODE / filename).read_text(encoding="utf-8", errors="replace")
    output = []
    unknown = []
    total = 0
    for line in source.splitlines():
        clear = re.findall(r"<(?:CLEAR|PLAIN)TEXT\s+[A-Z]+\s+(.*?)>", line)
        if clear:
            output.extend(f"[clear: {item}]" for item in clear)
            continue
        if line.startswith("#"):
            continue
        values = []
        for part in line.split("."):
            value = base_group(part)
            if value is not None:
                values.append(value)
        if len(values) < 2:
            continue
        decoded = []
        for value in values:
            total += 1
            if value in key:
                decoded.append(key[value])
            else:
                decoded.append(f"[{value}?]")
                unknown.append(value)
        output.append(" ".join(decoded))
    destination = ROOT / f"plaintext_R{record}_raw.txt"
    destination.write_text("\n".join(output) + "\n", encoding="utf-8")
    print(
        f"R{record}: {total} groups; {total-len(unknown)} read; "
        f"{len(unknown)} unknown -> {destination.name}"
    )


key = load_key()
print(f"key: {len(key)} entries, range {min(key)}-{max(key)}")
decode_document(1026, "DOC_R1026_D1852_1852.txt", key)
decode_document(1027, "DOC_R1027_D2299_2299.txt", key)
