import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "vendor"))

import cv2
import numpy as np
import onnx

MODEL = ROOT / "vendor" / "rapidocr_onnxruntime" / "models" / "ch_PP-OCRv4_rec_infer.onnx"


def characters():
    model = onnx.load(str(MODEL), load_external_data=False)
    values = {item.key: item.value for item in model.metadata_props}
    return ["blank", *values["character"].splitlines(), " "]


def recognize(net, chars, image):
    h, w = image.shape[:2]
    out_w = max(320, int(np.ceil(48 * w / h)))
    resized_w = min(out_w, int(np.ceil(48 * w / h)))
    resized = cv2.resize(image, (resized_w, 48)).astype("float32")
    resized = resized.transpose((2, 0, 1)) / 255.0
    resized = (resized - 0.5) / 0.5
    blob = np.zeros((1, 3, 48, out_w), dtype=np.float32)
    blob[0, :, :, :resized_w] = resized
    net.setInput(blob, "x")
    pred = net.forward()
    indexes = pred.argmax(axis=2)[0]
    probs = pred.max(axis=2)[0]
    text = []
    scores = []
    previous = -1
    for index, score in zip(indexes, probs):
        if index and index != previous:
            text.append(chars[index])
            scores.append(float(score))
        previous = int(index)
    return "".join(text), (sum(scores) / len(scores) if scores else 0.0)


def main(path):
    image = cv2.imread(str(path))
    net = cv2.dnn.readNetFromONNX(str(MODEL))
    chars = characters()
    # R2045 p5: the cipher occupies x=260..3600, y=0..3900 in 15 lines.
    x1, x2 = 180, image.shape[1] - 120
    centers = [180 + i * 245 for i in range(16)]
    for number, center in enumerate(centers, 1):
        y1, y2 = max(0, center - 105), min(image.shape[0], center + 120)
        crop = image[y1:y2, x1:x2]
        text, score = recognize(net, chars, crop)
        print(f"{number:02d}\t{score:.3f}\t{text}")


if __name__ == "__main__":
    main(Path(sys.argv[1]).resolve())
