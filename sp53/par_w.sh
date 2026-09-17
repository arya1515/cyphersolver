#!/bin/sh
# par_w.sh <lang> <cipher> <procs> <restarts> <tag> [base]; env HT0 HT1 HW HMAXC HINIT pass through to fasthomo_w.py
L=$1; F=$2; P=$3; R=$4; TAG=$5; B=$6
i=0
while [ $i -lt $P ]; do
  python fasthomo_w.py $L $F 10000000 $R $((2000+i*7+RANDOM%5)) $B > parw_${TAG}_$i.txt 2>&1 &
  i=$((i+1))
done
wait
grep -h "^restart" parw_${TAG}_*.txt | sort -k4 -n | tail -3
best=$(grep -l "^BEST" parw_${TAG}_*.txt | xargs grep -H "^BEST" | sort -t' ' -k2 -n | tail -1 | cut -d: -f1)
echo "from $best"; grep -A1 "^BEST" $best | cut -c1-700
