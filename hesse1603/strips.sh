#!/bin/zsh
# usage: strips.sh LEAF  -> crops/lLEAF_yNNNN.jpg, 900px strips with 100px overlap, full width
L=$1; f=img/leaf_$(printf %04d $L).jpg
for y in 250 1050 1850 2650 3450; do sips -c 900 2425 --cropOffset $y 0 $f --out crops/l${L}_y$y.jpg >/dev/null 2>&1; done
