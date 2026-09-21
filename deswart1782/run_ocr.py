import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "vendor"))

from rapidocr_onnxruntime import RapidOCR

engine = RapidOCR(det_use_dml=False, cls_use_dml=False, rec_use_dml=False)

for value in sys.argv[1:]:
    path = Path(value).resolve()
    result, elapsed = engine(str(path))
    output = []
    for box, text, score in result or []:
        output.append({"box": box, "text": text, "score": score})
    target = path.with_suffix(path.suffix + ".ocr.json")
    target.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{path.name}: {len(output)} regions in {elapsed}; {target.name}")
    for item in output:
        print(f"{item['score']:.3f}\t{item['text']}")
