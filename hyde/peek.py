import json,gzip,sys
ident=sys.argv[1]
idx=json.loads(gzip.decompress(open(ident+'_pageindex.json.gz','rb').read()))
print(type(idx), len(idx)); print(str(idx)[:400])
