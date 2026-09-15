#!/bin/bash
# non-English Gutenberg (manu/project_gutenberg) after the English run completes
cd /c/Users/dbour/cypher/beale
until grep -q ALLDONE scan.log 2>/dev/null; do sleep 60; done
mkdir -p shards done
curl -sS -m 60 "https://huggingface.co/api/datasets/manu/project_gutenberg/tree/main/data" | python -c "import json,sys; [print(x['path']) for x in json.load(sys.stdin) if not x['path'].split('/')[-1].startswith(('en-','zh-','ru-','pl-'))]" | tr -d '\r' > shard_list2.txt
for p in $(cat shard_list2.txt); do
  b=$(basename $p); f=shards/$b
  [ -f "done/$b" ] && continue
  curl -sSL -m 3600 -o "$f" "https://huggingface.co/datasets/manu/project_gutenberg/resolve/main/$p" || continue
  python scan_corpus.py "$f" results_gutenberg.tsv 10 >> scan.log 2>&1
  touch "done/$b"; rm -f "$f"
done
echo ALLDONE2 >> scan.log
