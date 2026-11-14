# Samsung Galaxy Note 20 Ultra (AT&T) debloat

ADB debloat for a Note 20 Ultra 5G, model `SM-N986U`, AT&T firmware (`N986USQS2EULI`), Android 12 / One UI 4.0.
The phone is used in Pakistan on a Telenor SIM. No root. Everything is reversible.

## Files

| File | What |
|---|---|
| `list.csv` | Packages: `action` (remove / after / keep), what it is, what you lose |
| `apply.py` | Debloat or restore from `list.csv`. Rolls back app updates first, so storage is freed |

## Use

1. Turn on Developer options > Wireless debugging. Pair once: `adb pair <ip>:<pairing-port> <code>`.
2. `adb connect <ip>:<port>`. The phone shows twice in `adb devices`, so set `ANDROID_SERIAL=<ip>:<port>`.
3. Read `list.csv` and change `action` to suit you.
4. `./apply.py debloat --dry-run`, then `./apply.py debloat`.

## AT&T firmware problems

| Problem | Fix |
|---|---|
| Mobile data quick settings tile hidden | Add `MobileData` to the tile list (below) |
| No system updates off the AT&T network. The update screen says "No update is available" | Flash the unlocked `N986U1` (`XAA`) firmware with Odin on Windows. This usually erases the phone. Not done |
| AT&T usage tracking (`com.att.iqi`) and silent app installer (`com.dti.att`) | In `list.csv` |
| Hidden Facebook and Amazon installers | In `list.csv` |

Mobile data tile:

```
adb shell settings put secure sysui_qs_tiles "Wifi,MobileData,$(adb shell settings get secure sysui_qs_tiles | sed 's/^Wifi,//')"
```

Undo: put back the old value of `sysui_qs_tiles`.

## Do not remove

- `com.ws.dm`: the AT&T software update client.
- `com.sec.android.soagent`: the Samsung update agent.
- The other `keep` rows in `list.csv`.

## Undo

- Everything: `./apply.py restore`
- One app: `adb shell cmd package install-existing <pkg>`
- A factory reset brings everything back.

## My results (2026-11-14)

47 packages removed, 0 failed. Storage freed: about 2.1 GB (14.8 GB free before, 17.3 GB after).
