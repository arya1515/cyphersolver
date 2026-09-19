# usage: strip.sh name y0 y1  -> 4 segments
cd /c/Users/dbour/cypher/pelissier1592/cal/crops
n=$1; y0=$2; y1=$3
for s in 0 1 2 3; do x0=$((1560+s*700)); python ../../crop.py ../../img/c230.jpg $x0 $y0 $((x0+780)) $y1 ${n}_$s.jpg 1560; done
