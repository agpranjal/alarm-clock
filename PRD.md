# PRD: CLI Alarm Clock

## 1. Overview
A lightweight command-line alarm clock for personal use. No database, no GUI, no web front end. Alarms are stored in a flat JSON file and triggered by a background polling process.

## 2. Goals
- Let the user schedule one-time alarms from the terminal.
- Trigger an audible alert at the scheduled time with zero manual polling by the user.
- Keep the implementation minimal: single JSON file for storage, no external services.

## 3. Non-Goals
- No snooze functionality.
- No repeating/recurring alarms (daily, weekly, etc.).
- No survival across machine restarts (no `launchd`/systemd integration).
- No GUI, web UI, or notification-center integration.
- No multi-user support.

## 4. Target User
Single user (Pranjal), running on macOS, comfortable starting/stopping a background process manually via terminal.

## 5. User Stories
- As a user, I can add an alarm for a specific time with an optional label.
- As a user, I can list all currently pending alarms.
- As a user, I can remove an alarm before it rings.
- As a user, I can start a background process that watches for alarms and rings them.
- As a user, once an alarm rings, it disappears from my list automatically — I don't have to clean it up.

## 6. Functional Requirements

| ID | Requirement |
|----|-------------|
| FR1 | `add <HH:MM> [--label TEXT]` — creates a new alarm entry with a unique ID, the given time, and an optional label. |
| FR2 | `list` — prints all pending alarms with their ID, time, and label. |
| FR3 | `remove <id>` — deletes the alarm with the given ID from storage. |
| FR4 | `run` — starts the watcher loop in the foreground (intended to be launched via `nohup ... &` for background use). |
| FR5 | The watcher checks the current time once per second against all pending alarms' `HH:MM` values. |
| FR6 | On a match, the watcher plays a sound via `subprocess` (e.g. `afplay`) and prints a message to stdout/nohup.out. |
| FR7 | Immediately after ringing, the alarm is deleted from the JSON file so it cannot re-trigger. |

## 7. Data Model
Stored at `~/.alarmclock/alarms.json` as a JSON array:
```json
[
  {"id": 1, "time": "07:30", "label": "wake up"}
]
```

## 8. Technical Design
- **Language**: Python 3
- **CLI parsing**: `argparse` (subcommands: `add`, `list`, `remove`, `run`)
- **Storage**: flat JSON file, read/written on every command (no DB)
- **Sound playback**: `subprocess.run(["afplay", path_to_sound])` (macOS-only, no extra dependency)
- **Process model**: foreground script intended to be run with `nohup python3 alarm.py run &`; no daemonization, no PID file, no restart-survival
- **Polling interval**: 1 second

## 9. Out of Scope / Future Considerations (not built now)
- Repeating alarms
- Snooze
- launchd-based persistence across reboots
- Cross-platform sound playback (Linux/Windows)
- Alarm volume control / fade-in

## 10. Success Criteria
- Adding, listing, and removing alarms works correctly via CLI.
- A scheduled alarm rings audibly within 1 second of its target time.
- After ringing, the alarm no longer appears in `list`.
- App has zero external dependencies beyond Python's standard library.