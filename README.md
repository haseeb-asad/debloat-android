# debloat-android

No-root ADB debloat lists and scripts for Android phones and TVs, one folder per device.
Reversible unless a device README says otherwise.

| Device | Folder |
|---|---|
| OnePlus 13s (OxygenOS 16 and 17) | [`phones/oneplus13s/`](phones/oneplus13s/) |
| TCL Android TV (BeyondTV, Android 11) | [`tvs/tcl-beyondtv/`](tvs/tcl-beyondtv/) |

## Use

1. Install adb (Android platform-tools), turn on USB debugging, connect one device. `adb devices` should show it as `device`.
2. Open the device folder and read its README.
3. Edit `list.csv`: set `action` per package (`remove` / `disable` / `after` / `keep`).
4. `./apply.py debloat --dry-run`, then `./apply.py debloat`.

Undo with `./apply.py restore`. Packages not on your device are skipped.

## For agents

- Read the device README and `list.csv` before running anything.
- Run `--dry-run` first and show the owner the output.
- Apply only `remove` and `disable` rows. Ask before touching a `keep` or `after` row, or a package that is not in the list.
- Know the undo for a step before you take it; each device README has an Undo section.

## Contributing

Contributions are welcome: a new device, a fix to a list, or a note on what broke for you.

- New device: copy the closest folder to `phones/<device>/` or `tvs/<device>/`, fill in `list.csv`, and add a row to the table above.
- Say what you tested on (model, OS version) and what each removal costs the user.
- Keep it no-root and reversible, or say clearly where it is not.
