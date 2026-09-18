#!/bin/zsh
ARK=btv1b52524472n
n=$1; x=$2; y=$3; w=$4; h=$5; name=$6; ow=${7:-3600}
mkdir -p crops
curl -sL -A 'Mozilla/5.0' --retry 3 -m 240 -o "crops/z${n}_${name}.jpg" "https://gallica.bnf.fr/iiif/ark:/12148/$ARK/f$n/$x,$y,$w,$h/$ow,/0/native.jpg"
echo "crops/z${n}_${name}.jpg"
