# row113.sh name ycenter [img]: 5 segments of 700px (overlap 60), y from yc-150 to yc+70
cd /c/Users/dbour/cypher/pelissier1592
n=$1; yc=$2; im=${3:-c234}
for s in 0 1 2 3 4; do x0=$((1450+s*640)); python crop.py img/$im.jpg $x0 $((yc-150)) $((x0+700)) $((yc+70)) cal/crops/113_${n}_$s.jpg 1800; done
