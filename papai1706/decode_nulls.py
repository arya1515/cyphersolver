"""Read the Constantinople despatches R793-R796 with Pápai's key (decode.py, DECODE R580/R581).
Groups above 322 are outside the table; in R795 they are nulls (the contemporary interlinear decipherment skips
them) and are dropped here, shown as '·'. Usage: python decode.py DOC_R795_*.txt"""
import sys, re
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import decode as P
_show = P.show
def show(n):
    if n > 322 and n not in P.KEY: return "·"
    return _show(n)
P.show = show
for f in sys.argv[1:]:
    sys.argv = [sys.argv[0], f]
    exec(compile(Path(P.__file__).read_text(encoding="utf-8").split('if __name__ == "__main__":')[1].replace("\n    ", "\n"), "main", "exec"), vars(P))
