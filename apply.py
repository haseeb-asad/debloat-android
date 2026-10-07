#!/usr/bin/env python3
"""Debloat or restore a OnePlus phone over adb using list.csv.

  ./apply.py debloat            remove + disable rows (rolls back app updates first to free storage)
  ./apply.py debloat --after    also apply the 'after' rows (second-round tests)
  ./apply.py restore            bring every remove/disable/after row back
  ./apply.py debloat --dry-run  show what would happen, change nothing
"""
import csv, os, subprocess, sys

ADB = os.environ.get("ADB", os.path.expanduser("~/Library/Android/sdk/platform-tools/adb"))
HERE = os.path.dirname(os.path.abspath(__file__))


def sh(cmd):
    out = subprocess.run([ADB, "shell", cmd], capture_output=True, text=True)
    return (out.stdout + out.stderr).strip().replace("\n", " ")


def used_kb():
    return int(sh("df /data | tail -1").split()[2])


def has_update(pkg):
    return "codePath=/data/" in sh(f"dumpsys package {pkg} | grep -m1 codePath=")


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode not in ("debloat", "restore"):
        sys.exit(__doc__)
    dry = "--dry-run" in sys.argv
    actions = {"remove", "disable"} | ({"after"} if "--after" in sys.argv or mode == "restore" else set())
    rows = [r for r in csv.DictReader(open(os.path.join(HERE, "list.csv"))) if r["action"] in actions]
    if "device" not in subprocess.run([ADB, "devices"], capture_output=True, text=True).stdout.split("\n", 1)[1]:
        sys.exit("No authorised device. Plug in the phone, enable USB debugging and accept the prompt.")
    present = set(sh("pm list packages -u").replace("package:", "").split())
    installed = set(sh("pm list packages").replace("package:", "").split())

    before, ok, skipped, failed = used_kb(), 0, 0, 0
    os.makedirs(os.path.join(HERE, "results"), exist_ok=True)
    log = open(os.path.join(HERE, "results", f"{mode}.log"), "a")
    for r in rows:
        pkg, act = r["package"], ("disable" if r["action"] == "disable" else "remove")
        if pkg not in present:
            res, status = "not on this phone", "SKIP"
        elif dry:
            res, status = f"would {act if mode == 'debloat' else 'restore'}", "DRY "
        elif mode == "restore":
            res = sh(f"pm enable --user 0 {pkg}") if act == "disable" else sh(f"cmd package install-existing --user 0 {pkg}")
            status = "OK  " if ("new state" in res or "installed for user" in res) else "FAIL"
        else:
            if pkg not in installed and act == "remove":
                res, status = "already removed", "SKIP"
            else:
                if has_update(pkg):
                    sh(f"pm uninstall-system-updates {pkg}")
                res = sh(f"pm disable-user --user 0 {pkg}") if act == "disable" else sh(f"pm uninstall --user 0 {pkg}")
                status = "OK  " if ("Success" in res or "disabled" in res) else "FAIL"
        ok += status == "OK  "; skipped += status == "SKIP"; failed += status == "FAIL"
        line = f"{status} {act:7} {pkg}  {res}"
        print(line); log.write(line + "\n")

    freed = (before - used_kb()) / 1024
    print(f"\n{ok} ok, {skipped} skipped, {failed} failed. Storage freed: {freed:.0f} MB")
    if failed:
        print("Failures are usually protected apps; disable them in Settings > Apps instead.")


if __name__ == "__main__":
    main()
