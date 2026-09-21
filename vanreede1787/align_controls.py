"""Extract DECODE's known-plaintext Van Reede controls for alignment work."""

from pathlib import Path
import re


ROOT = Path(__file__).parent / "decode"


def normalize_group(raw: str) -> str | None:
    raw = raw.replace("J?", "3").replace("J+", "3").replace("J", "3")
    digits = "".join(re.findall(r"\d", raw))
    return str(int(digits)) if digits else None


def extract(record: int, doc: str) -> None:
    text = (ROOT / doc).read_text(encoding="utf-8", errors="replace")
    plain = []
    for language, line in re.findall(r"<PLAINTEXT\s+([A-Z]+)\s+(.*?)>", text):
        if language == "FR" and "Grand Chifre" not in line:
            plain.append(line)

    groups = []
    for line in text.splitlines():
        if line.startswith("#"):
            continue
        cleaned = re.sub(r"<[^>]+>", "", line)
        candidates = [normalize_group(part) for part in re.split(r"[.,]", cleaned)]
        candidates = [group for group in candidates if group is not None]
        if len(candidates) >= 2:
            groups.extend(candidates)

    plain_text = " ".join(plain)
    words = re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ*]+(?:['’][A-Za-zÀ-ÖØ-öø-ÿ*]+)?", plain_text)
    (Path(__file__).parent / f"control_R{record}_plaintext.txt").write_text(
        plain_text + "\n", encoding="utf-8"
    )
    (Path(__file__).parent / f"control_R{record}_groups.txt").write_text(
        " ".join(groups) + "\n", encoding="utf-8"
    )
    print(f"R{record}: {len(words)} plaintext words; {len(groups)} code groups")

    if record == 1028:
        control_lines = []
        for language, line in re.findall(r"<PLAINTEXT\s+([A-Z]+)\s+(.*?)>", text):
            if "PPP" in line:
                break
            if language == "FR":
                control_lines.append(line)
        control = " ".join(control_lines)
        control = re.sub(r"^.*?mes idées sur\s+", "", control, flags=re.I)
        replacements = {
            "entre : roit": "entreroit", "at tendront": "attendront",
            "recom mande": "recommande", "d'ouvertu res": "d'ouvertures",
            "Ma drid": "Madrid", "l'en trainer": "l'entrainer",
            "cepen dant": "cependant", "de mander": "demander",
        }
        for old, new in replacements.items():
            control = control.replace(old, new)
        control = re.sub(
            r"je dois me servir encore du chiffre pour vous dire,?", "", control,
            flags=re.I,
        )
        control_words = re.findall(
            r"[A-Za-zÀ-ÖØ-öø-ÿ*]+(?:['’][A-Za-zÀ-ÖØ-öø-ÿ*]+)?", control
        )
        (Path(__file__).parent / "control_R1028_aligned_words.txt").write_text(
            "\n".join(control_words) + "\n", encoding="utf-8"
        )
        print(f"R1028 alignment candidate: {len(control_words)} words")


extract(1028, "DOC_R1028_D2283_2283.txt")
extract(1029, "DOC_R1029_D2286_2286.txt")
