#!/bin/bash
cd /c/Users/dbour/cypher/beale
mkdir -p shards done
curl -sS -m 60 "https://huggingface.co/api/datasets/sedthh/gutenberg_english/tree/main/data" | python -c "import json,sys; [print(x['path']) for x in json.load(sys.stdin)]" | tr -d '\r' > shard_list.txt
# prefetch next shard while scanning current
prev=""
for p in $(cat shard_list.txt); do
  b=$(basename $p); f=shards/$b
  [ -f "done/$b" ] && continue
  if [ ! -f "$f.ok" ]; then
    curl -sSL -m 3600 -o "$f" "https://huggingface.co/datasets/sedthh/gutenberg_english/resolve/main/$p" && touch "$f.ok"
  fi
  # start prefetch of the next not-done shard
  nxt=""
  for q in $(cat shard_list.txt); do
    qb=$(basename $q); [ -f "done/$qb" ] && continue; [ "$qb" == "$b" ] && continue; [ -f "shards/$qb.ok" ] && continue
    nxt=$q; break
  done
  if [ -n "$nxt" ]; then
    ( curl -sSL -m 3600 -o "shards/$(basename $nxt)" "https://huggingface.co/datasets/sedthh/gutenberg_english/resolve/main/$nxt" && touch "shards/$(basename $nxt).ok" ) &
    pf=$!
  fi
  python scan_corpus.py "$f" results_gutenberg.tsv 10 >> scan.log 2>&1
  touch "done/$b"; rm -f "$f" "$f.ok"
  [ -n "$nxt" ] && wait $pf
done
echo ALLDONE >> scan.log
