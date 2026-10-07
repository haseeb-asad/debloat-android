#!/system/bin/sh
# Runs ON the phone. Usage: sh sampler.sh <seconds> <outfile>
N=${1:-3600}; OUT=${2:-/data/local/tmp/bench.csv}
echo "t,n,cpu_user,cpu_sys,ram_used_mb,swap_used_mb" > "$OUT"
read -r _ u n s i w q sq _ < /proc/stat
pu=$((u+n)); ps=$((s+q+sq)); pt=$((u+n+s+i+w+q+sq))
k=1
while [ $k -le $N ]; do
  sleep 1
  read -r _ u n s i w q sq _ < /proc/stat
  cu=$((u+n)); cs=$((s+q+sq)); ct=$((u+n+s+i+w+q+sq)); dt=$((ct-pt)); [ $dt -le 0 ] && dt=1
  usr=$(( (cu-pu)*10000/dt )); sys=$(( (cs-ps)*10000/dt ))
  pu=$cu; ps=$cs; pt=$ct
  mt=0; ma=0; st=0; sf=0
  while read -r key val _; do
    case $key in MemTotal:) mt=$val;; MemAvailable:) ma=$val;; SwapTotal:) st=$val;; SwapFree:) sf=$val;; esac
  done < /proc/meminfo
  printf "%s,%d,%d.%02d,%d.%02d,%d,%d\n" "$(date +%H:%M:%S)" $k $((usr/100)) $((usr%100)) $((sys/100)) $((sys%100)) $(((mt-ma)/1024)) $(((st-sf)/1024)) >> "$OUT"
  k=$((k+1))
done
echo done >> "$OUT.finished"
