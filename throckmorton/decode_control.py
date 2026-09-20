"""Replay the explicitly transcribed archive-key control; no inferred substitutions."""
import json, pathlib, sys
root=pathlib.Path(__file__).resolve().parent
stem=sys.argv[1] if len(sys.argv)>1 else 'control'
data=json.loads((root/(stem+'.json')).read_text(encoding='utf-8'))
tokens=[token for word in data['words'] for token in word]
reading=' '.join(filter(None,(''.join(data['key'][t] for t in word) for word in data['words'])))
print(reading)
print(f'{len(tokens)} transcribed cipher tokens, including {sum(not data["key"][t] for t in tokens)} nulls')
(root/(stem+'_tokens.txt')).write_text(' '.join(tokens)+'\n',encoding='utf-8')
(root/(stem+'_reading.txt')).write_text(reading+'\n',encoding='utf-8')
