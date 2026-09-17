#!/bin/sh
# par.sh <lang> <cipher> <procs> <restarts-per-proc> <tag> [base]  -> runs fasthomo.py hot in parallel, aggregates to par_<tag>.txt
L=$1; F=$2; P=$3; R=$4; TAG=$5; B=$6
i=0
while [ $i -lt $P ]; do
  HT0=6.0 HT1=0.1 python fasthomo.py $L $F 10000000 $R $((1000+i*7+RANDOM%5)) $B > par_${TAG}_$i.txt 2>&1 &
  i=$((i+1))
done
wait
grep -h "^restart" par_${TAG}_*.txt | sort -k4 -n | tail -3
best=$(grep -l "^BEST" par_${TAG}_*.txt | xargs grep -H "^BEST" | sort -t' ' -k2 -n | tail -1 | cut -d: -f1)
echo "from $best"; grep -A1 "^BEST" $best | cut -c1-600
