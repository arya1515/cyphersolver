#!/bin/sh
# crop.sh VIEW X Y W H OUTSCALEWIDTH OUTFILE
V=$1; X=$2; Y=$3; W=$4; H=$5; S=$6; O=$7
curl -s -A "Mozilla/5.0" "https://gallica.bnf.fr/iiif/ark:/12148/btv1b9060015d/f$V/$X,$Y,$W,$H/$S,/0/native.jpg" -o "$O"
echo "$O $(stat -c%s "$O")"
