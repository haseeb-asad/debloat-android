#!/bin/bash
# Usage: ./bench.sh <label> [seconds]   e.g. ./bench.sh before-1 3600
# Reboots the phone, starts logging the moment adb comes back, pulls the CSV when done.
set -e
A=${ADB:-$HOME/Library/Android/sdk/platform-tools/adb}
L=${1:?label}; N=${2:-3600}; DIR="$(cd "$(dirname "$0")" && pwd)"; R=/data/local/tmp
mkdir -p "$DIR/results"
"$A" push "$DIR/sampler.sh" $R/sampler.sh >/dev/null
echo "Rebooting. Unlock once (accept USB debugging if asked), lock it, then leave it alone."
"$A" reboot
"$A" wait-for-device
"$A" push "$DIR/sampler.sh" $R/sampler.sh >/dev/null 2>&1 || true
"$A" shell "rm -f $R/bench.csv $R/bench.csv.finished; nohup sh $R/sampler.sh $N $R/bench.csv >/dev/null 2>&1 &"
echo "Logging started $(date +%H:%M:%S) for $N s."
until "$A" shell "[ -f $R/bench.csv.finished ]" 2>/dev/null; do sleep 30; done
"$A" pull $R/bench.csv "$DIR/results/$L.csv" >/dev/null
echo "Saved results/$L.csv"
