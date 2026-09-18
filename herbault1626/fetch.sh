#!/bin/zsh
# Fetch openings of BnF fr. 3669 (ark btv1b9060205q). usage: ./fetch.sh FIRST LAST [width]
ARK=btv1b9060205q
A=$1; B=$2; W=${3:-1600}
mkdir -p img
for n in $(seq $A $B); do
  out=$(printf "img/c%04d_%s.jpg" $n $W)
  [ -s "$out" ] && continue
  curl -sL -A 'Mozilla/5.0' --retry 4 -m 240 -o "$out" "https://gallica.bnf.fr/iiif/ark:/12148/$ARK/f$n/full/$W,/0/native.jpg"
  echo "$out $(stat -f%z "$out" 2>/dev/null)"
  sleep 0.2
done
