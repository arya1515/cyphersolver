#!/bin/zsh
# Fetch pages of the Nevers cipher key book BnF fr. 3995 (ark btv1b525085665).
ARK=btv1b525085665
A=$1; B=$2; W=${3:-1400}
mkdir -p img3995
for n in $(seq $A $B); do
  out=$(printf "img3995/c%04d_%s.jpg" $n $W)
  [ -s "$out" ] && continue
  curl -sL -A 'Mozilla/5.0' --retry 4 -m 240 -o "$out" "https://gallica.bnf.fr/iiif/ark:/12148/$ARK/f$n/full/$W,/0/native.jpg"
  echo "$out $(stat -f%z "$out" 2>/dev/null)"
  sleep 0.2
done
