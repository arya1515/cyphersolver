# seg.sh name y0 y1 [x0] : 5 segments of 620px
cd /c/Users/dbour/cypher/pelissier1592/cal/crops
n=$1; y0=$2; y1=$3; X=${4:-1580}
for s in 0 1 2 3 4; do x0=$((X+s*560)); python ../../crop.py ../../img/c230.jpg $x0 $y0 $((x0+620)) $y1 ${n}_$s.jpg 1500; done
