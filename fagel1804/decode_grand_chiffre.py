import pathlib
import re


root = pathlib.Path(__file__).parent
key_path = root / "key1024" / "DOC_R1024_D2881_2881.txt"
cipher_path = root / "ciphertext.txt"

key = {}
for line in key_path.read_text(encoding="utf-8-sig").splitlines():
    match = re.match(r"\s*(\d+)\s*-\s*(.+?)\s*$", line)
    if match:
        key.setdefault(int(match.group(1)), []).append(match.group(2))

def show_direct_lookup():
    for line in cipher_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("#") or line.startswith("[clear:"):
            continue
        numbers = [int(value) for value in re.findall(r"(?<![\^\d/])\d+", line)]
        print(" | ".join(f"{number}:{'/'.join(key.get(number, ['?']))}" for number in numbers))


def show_word_patterns():
    text = cipher_path.read_text(encoding="utf-8")
    text = "\n".join(line for line in text.splitlines() if not line.startswith("#"))
    text = re.sub(r"\[clear:.*?\]", lambda match: "<" + match.group(0)[7:-1].strip() + ">", text)
    text = re.sub(r"\[interlinear insertion, boxed:\s*(.*?)\]", r"<INSERT \1>", text)
    words = [part.strip(" ,\n") for part in re.split(r",", text) if part.strip(" ,\n")]
    for index, word in enumerate(words, 1):
        print(f"{index:03}: {word}")


if __name__ == "__main__":
    show_word_patterns()
