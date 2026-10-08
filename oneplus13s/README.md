# OnePlus 13s debloat

ADB debloat for OnePlus phones on OxygenOS 16, built from
[Jimka22x's r/oneplus list](https://www.reddit.com/r/oneplus/comments/1qzqd27/oneplus_13_oxygen16_debloat_1603501/)
([their sheet](https://docs.google.com/spreadsheets/d/1QtIntoT9Svvcrm_FqMwqJrh7VPuPsn-pt3FcB-9n__8/edit?usp=sharing)),
adjusted for the 13s (Plus Key / Plus Mind kept) plus a pass over the rest of the phone.
Tested on a 13s (CPH2723IN, 16.0.10.500). No root. Everything is reversible.

## Files

| File | What |
|---|---|
| `list.csv` | Every package: `action` (remove / disable / after / keep), matching what was done on my phone, what it is, what you lose |
| `apply.py` | Debloat or restore from `list.csv`; rolls back app updates first so storage is freed |
| `bench.sh` + `sampler.sh` | Reboot and log CPU / RAM / swap once a second |
| `compare.py` | Before vs after: AVG, P95, top 5%, peaks (same metrics as the original post) |
| `results/` | My 10-minute before/after runs |

## Use

1. Install adb (Android platform-tools), enable USB debugging, plug in, accept the prompt.
2. Read `list.csv` and change `action` to suit you. Lines are skipped if the package is not on your phone.
3. Optional before benchmark: `./bench.sh before 600`
4. `./apply.py debloat --dry-run`, then `./apply.py debloat`
5. Optional after benchmark: `./bench.sh after 600`, then `./compare.py results/before.csv results/after.csv`

Set `ADB=/path/to/adb` if adb is not at `~/Library/Android/sdk/platform-tools/adb`.

## Before you remove

- `com.oneplus.note`: notes saved only in OnePlus Notes are deleted; export or sync first.
- `com.android.contacts` / `com.android.incallui` are the OnePlus Phone and Contacts apps. Set Google Phone, Contacts and Messages as defaults first.
- `com.oneplus.gallery` is kept: removing it breaks opening photos from the camera.
- `after` rows (secure keyboard, live wallpapers, a Qualcomm secure-zone helper) are the second round, not applied yet; apply with `./apply.py debloat --after`.
- A factory reset brings everything back.

## Undo

- Everything: `./apply.py restore`
- One app: `adb shell cmd package install-existing <pkg>` (removed) or `adb shell pm enable <pkg>` (disabled)
- The 'OnePlus preinstalled apps (uninstallable)' group is fully deleted, so `restore` cannot bring it back. Reinstall from the store, or from the phone's factory copy: `adb shell ls /my_stock/del-app /my_product/del-app`, then `adb shell pm install -r --user 0 /my_stock/del-app/<Name>/<Name>.apk`

## Other tweaks (no root)

| Tweak | Command | Undo / notes |
|---|---|---|
| 0.5x animations | `adb shell settings put global window_animation_scale 0.5` (same for `transition_animation_scale`, `animator_duration_scale`) | Set back to `1`. Usually survives turning Developer options off; ADB itself needs it on. |
| Ad-blocking DNS | `adb shell settings put global private_dns_mode hostname` then `adb shell settings put global private_dns_specifier dns.adguard-dns.com` | `private_dns_mode off`. If a hotel/cafe Wi-Fi login page won't load, turn Private DNS off briefly. |
| Smaller UI (display density) | `adb shell wm density 440` (stock on the 13s is 560; Settings > Display size gives ~476) | `adb shell wm density reset`. Go in small steps; too low makes apps cramped. |
| Delete Google ad ID | Not possible via ADB. `adb shell am start -a com.google.android.gms.settings.ADS_PRIVACY` opens the page; tap "Delete advertising ID" | - |
| Block an app running in background | OnePlus blocks `cmd appops` from ADB. Use Settings > Apps > <app> > Battery usage > "Allow background activity" off, or enable "Disable permission monitoring" in Developer options and run `adb shell cmd appops set <pkg> RUN_ANY_IN_BACKGROUND ignore` | Notifications via Google push still arrive. |
| Recompile apps | `adb shell cmd package compile -m speed-profile <pkg>` per app, then `adb shell cmd package bg-dexopt-job` | Same job Android runs overnight while charging; uses storage (~800 MB here). Only worth it right after a system update. |

## My results (13s, 10 min each, right after unlock, no factory reset)

139 packages removed, 4 disabled; 537 -> 398 packages; about 1.3 GB storage freed.
The benchmark was taken after the first 122 removals.
CPU system -16% avg, CPU spikes (top 5%) -17 to -21%, RAM P95 -23%, RAM avg -4%. Most of the gain is in the first minute after boot.
Full table in `results/comparison.txt`.
