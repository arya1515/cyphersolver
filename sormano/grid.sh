#!/bin/sh
# grid.sh VIEW TAG X0 Y0 NCOLS NROWS  (800px tiles, 50px overlap, out 3200)
V=$1; TAG=$2; X0=$3; Y0=$4; NC=$5; NR=$6
r=0
while [ $r -lt $NR ]; do
  c=0
  while [ $c -lt $NC ]; do
    X=$((X0 + c*750)); Y=$((Y0 + r*750))
    O="raw/${TAG}_r${r}c${c}.jpg"
    if [ ! -s "$O" ]; then
      curl -s -A "Mozilla/5.0" "https://gallica.bnf.fr/iiif/ark:/12148/btv1b9060015d/f$V/$X,$Y,800,800/3200,/0/native.jpg" -o "$O"
      sz=$(stat -c%s "$O"); echo "$O $sz"
      sleep 1.1
    fi
    c=$((c+1))
  done
  r=$((r+1))
done
