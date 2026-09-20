"""Correct the inherited OCR-based citation after viewing Forbes II p.12."""
import pathlib, sys
root=pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else pathlib.Path(__file__).resolve().parent
paths=list(root.glob('*'))
if (root/'throckmorton').is_dir():
    paths=list((root/'throckmorton').glob('*'))+[root/'README.md',root/'docs/throckmorton.html']
for p in paths:
    if not p.is_file() or p.suffix not in ('.md','.py','.json','.html') or p.name==pathlib.Path(__file__).name or p.name.startswith('record_'):
        continue
    s=p.read_text(encoding='utf-8')
    for old,new in [('Forbes II p.31','Forbes II p.12'),('Forbes II, p.31','Forbes II, p.12'),('Forbes II (1741), p.31','Forbes II (1741), p.12'),('Forbes II, pp.28–35','Forbes II, p.12 (sampled passage)'),('especially p.31','especially p.12')]:
        s=s.replace(old,new)
    p.write_text(s,encoding='utf-8')
