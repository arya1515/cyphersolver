import pathlib, re, html, sys
root=pathlib.Path(__file__).resolve().parent/'sources'
for p in root.glob('*.html'):
    raw=p.read_text(encoding='utf-8',errors='replace')
    raw=re.sub(r'<(?:script|style)\b.*?</(?:script|style)>','',raw,flags=re.S|re.I)
    raw=re.sub(r'</(?:p|h[1-6]|div|tr)>','\n',raw,flags=re.I)
    text=html.unescape(re.sub('<[^>]+>','',raw))
    text=re.sub(r'[ \t]+',' ',text)
    text=re.sub(r'\n\s*\n','\n',text)
    p.with_suffix('.txt').write_text(text,encoding='utf-8')
    if p.stem in sys.argv[1:]:
        print(text)
