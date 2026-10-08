#!/usr/bin/env python3
"""Usage: compare.py results/before.csv results/after.csv  -> same metrics as the author's sheet"""
import csv, sys
def load(p):
    rows = list(csv.DictReader(open(p)))
    return {k: [float(r[k]) for r in rows] for k in ("cpu_user", "cpu_sys", "ram_used_mb", "swap_used_mb")}
def p95(v): s = sorted(v); return s[min(len(s) - 1, int(0.95 * len(s)))]
def top5(v): s = sorted(v); n = max(1, len(s) // 20); return sum(s[-n:]) / n
TH = {"cpu_user": 0.5, "cpu_sys": 1, "ram_used_mb": 4000, "swap_used_mb": 1500}
def stats(v, k): return {"AVG": sum(v) / len(v), "P95": p95(v), "Top 5% avg": top5(v),
                         f"Peaks (>{TH[k]})": sum(x > TH[k] for x in v) / len(v)}
b, a = load(sys.argv[1]), load(sys.argv[2])
print(f"samples: before {len(b['cpu_user'])}, after {len(a['cpu_user'])}\n")
print(f"{'metric':14}{'stat':16}{'before':>10}{'after':>10}{'change':>10}")
for k in b:
    sb, sa = stats(b[k], k), stats(a[k], k)
    for s in sb:
        ch = (sa[s] - sb[s]) / sb[s] * 100 if sb[s] else 0
        print(f"{k:14}{s:16}{sb[s]:10.2f}{sa[s]:10.2f}{ch:+9.1f}%")
