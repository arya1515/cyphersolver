# band111.sh name y0 y1 : 3 segments of 950 px (x 1650..4450), 2x
cd /c/Users/dbour/cypher/pelissier1592/cal/crops
n=$1; y0=$2; y1=$3
for s in 0 1 2; do x0=$((1650+s*900)); python ../../crop.py ../../img/c230.jpg $x0 $y0 $((x0+960)) $y1 ${n}_$s.jpg 1900; done
