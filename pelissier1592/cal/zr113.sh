# zr113.sh name y0 y1 x0 x1 nseg [img] : nseg equal segments, 1800 px wide output each
cd /c/Users/dbour/cypher/pelissier1592
n=$1; y0=$2; y1=$3; a=$4; b=$5; k=$6; im=${7:-c234}
w=$(( (b-a)/k ))
for ((s=0;s<k;s++)); do x0=$((a+s*w-30)); python crop.py img/$im.jpg $x0 $y0 $((x0+w+60)) $y1 cal/crops/113_${n}_$s.jpg 1800; done
