# CLI Alarm Clock

A minimal command-line alarm clock for macOS. Schedule one-time alarms from the terminal; a background watcher plays a sound when they fire.

No database, no GUI, no external dependencies — just Python 3 and a JSON file.

## Requirements

- macOS (uses `afplay` for sound)
- Python 3

## Quick start

```bash
# Start the watcher (leave this running)
nohup python3 alarm.py run &

# Schedule an alarm
python3 alarm.py add 07:30 --label "wake up"

# See pending alarms
python3 alarm.py list

# Cancel an alarm
python3 alarm.py remove 1
```

## Commands

| Command | Description |
|---------|-------------|
| `add <HH:MM> [--label TEXT]` | Schedule a new one-time alarm (24-hour time) |
| `list` | List all pending alarms |
| `remove <id>` | Remove an alarm by ID |
| `run` | Start the watcher loop (polls every second) |

### Examples

```bash
python3 alarm.py add 14:30
python3 alarm.py add 09:00 --label "standup"
python3 alarm.py list
python3 alarm.py remove 2
```

## How it works

1. **`add` / `list` / `remove`** read and write `.alarmclock/alarms.json` in the project root, then exit.
2. **`run`** stays alive, checking the current time once per second against all pending alarms.
3. When an alarm matches, the watcher plays a system sound, prints a message to stdout, and removes the alarm from the file so it cannot ring again.

Run the watcher in the background with `nohup`:

```bash
nohup python3 alarm.py run &
```

Output goes to `nohup.out`. To stop the watcher, find and kill the process:

```bash
pkill -f "alarm.py run"
```

## Storage

Alarms are stored at `.alarmclock/alarms.json`:

```json
[
  {"id": 1, "time": "07:30", "label": "wake up"}
]
```

This directory is gitignored.

## Limitations

- One-time alarms only (no daily/weekly repeat)
- No snooze
- Does not survive machine restarts — restart the watcher after a reboot
- macOS only (sound playback via `afplay`)
