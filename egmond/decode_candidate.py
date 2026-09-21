"""Replay the working shape-key hypothesis without filling unknowns from prose."""
import pathlib,json
root=pathlib.Path(__file__).resolve().parent
key=json.loads((root/'candidate_key.json').read_text())['tokens']
lines=[]; token_lines=[]
for raw in (root/'body_all_lines_provisional.txt').read_text().splitlines():
    src=raw.split(); tokens=[]; i=0
    while i<len(src):
        pair=''.join(src[i:i+2])
        if i+1<len(src) and pair in ('DD','CE'):
            tokens.append(pair);i+=2
        else: tokens.append(src[i]);i+=1
    token_lines.append(tokens)
    lines.append(''.join(key.get(t,'?') for t in tokens))
(root/'candidate_reading.txt').write_text('\n'.join(lines)+'\n')
(root/'candidate_token_lines.json').write_text(json.dumps(token_lines,indent=2))
for i,line in enumerate(lines,1): print(f'{i:02}: {line}')
