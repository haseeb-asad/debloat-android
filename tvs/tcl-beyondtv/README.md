# TCL Android TV debloat

ADB debloat for a TCL Android TV (model `BeyondTV`, Realtek RTD285o, Android 11, 2 GB RAM).
No root. Everything is reversible.

## Files

| File | What |
|---|---|
| `list.csv` | Packages: `action` (remove / after / keep), what it is, what you lose. `after` rows are undecided and not applied |
| `apply.py` | Debloat or restore from `list.csv`; rolls back app updates first so storage is freed |

## Use

1. On the TV: Settings > Device Preferences > About > press Build 7 times, then Developer options > USB debugging on.
2. `adb connect <tv-ip>:5555` and accept the prompt on the TV. The TV drops off the network in standby, so keep it on.
3. Optional: `adb shell dumpsys netstats --full --uid > netstats.txt` to keep the per-app data usage. Removing a package merges its history into one "removed apps" bucket.
4. Read `list.csv` and change `action` to suit you.
5. `./apply.py debloat --dry-run`, then `./apply.py debloat`
6. Restart the TV and check live TV, HDMI inputs, the remote and casting.

Set `ADB=/path/to/adb` if adb is not at `~/Library/Android/sdk/platform-tools/adb`.
Disconnect other adb devices first; the script talks to the only one attached.

## Do not remove

The `TV core` rows in `list.csv` (live TV, HDMI inputs, settings, remote keys, remote pairing, system update)
and `com.google.android.apps.mediashell` if you cast from a phone.

## Always-listening Assistant

The biggest CPU cost on this TV: `com.google.android.katniss:interactor` held about a third of one core
running "Hey Google" detection, with the Assistant switch in Settings already off. The built-in mic it
listened on only delivers silence here (flat -93.5 dB).

Fix: take the microphone permission away from the Assistant app. Survives a restart.

```
adb shell pm revoke com.google.android.katniss android.permission.RECORD_AUDIO
adb shell am force-stop com.google.android.katniss
```

- Check: `adb shell dumpsys media.audio_flinger | grep "Input device"` shows only `AUDIO_DEVICE_NONE`.
- Cost: voice search from the remote stops working. The search tab still works with the keyboard.
- Undo: `adb shell pm grant com.google.android.katniss android.permission.RECORD_AUDIO`

These do not work from ADB here, so skip them:

- `am start -a com.google.android.assistant.HOTWORD_DISABLE`: refused unless the caller is the Settings app.
- `settings put secure voice_interaction_service '""'`: works until the next restart.
- `cmd role remove-role-holder android.app.role.ASSISTANT ...`: the app is re-added as the fallback holder.
- `pm disable` on the listening service: shell may not change components of a system app.

## Undo

- Everything: `./apply.py restore`
- One app: `adb shell cmd package install-existing <pkg>`
- A factory reset brings everything back.

## Notes

- Load average sits around 21. It is not real load: about 26 Realtek driver threads are parked in
  uninterruptible sleep and Linux counts them. Use `top` for real CPU.
- About 700 MB of the 2 GB is reserved for video hardware, so RAM is the real constraint.
- Play Store keeps about 200 MB of cached processes after you close it. Android reclaims that on demand.
- `com.tcl.smartalexa` and `com.tcl.guard` keep running after removal until the TV restarts.

## My results (idle on the home screen)

9 packages removed, plus one sideloaded app uninstalled by hand; 141 -> 131 packages; 52 MB storage freed.
Idle CPU about 87% -> 97% idle, almost all from the Assistant fix; holds after two restarts.
Available RAM moves between 470 and 730 MB depending on what is cached, so there is no clean before / after RAM number.
