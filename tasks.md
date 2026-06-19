# CLI Alarm Clock — Tasks

Derived from [PRD.md](PRD.md).

## Project setup

- [x] Create `alarm.py` as the single entry point (Python 3, stdlib only)
- [x] Set up `argparse` with subcommands: `add`, `list`, `remove`, `run`
- [x] Add a default sound file path for `afplay` (or document where the sound asset lives)

## Storage layer

- [x] Store alarms at `.alarmclock/alarms.json` in the project root
- [x] Create `.alarmclock/` in the project root on first use if it does not exist
- [x] Define alarm schema: `id` (int), `time` (`HH:MM`), `label` (string, optional)
- [x] Implement read/write helpers that load and save the JSON array on every command
- [x] Generate a unique, monotonically increasing `id` for each new alarm

## CLI: `add` (FR1)

- [x] Parse `add <HH:MM> [--label TEXT]`
- [x] Validate time format (`HH:MM`, 24-hour)
- [x] Append a new alarm entry and persist to JSON
- [x] Print confirmation with the assigned alarm ID

## CLI: `list` (FR2)

- [x] Parse `list` with no required arguments
- [x] Load pending alarms from JSON
- [x] Print each alarm’s ID, time, and label (handle missing label gracefully)
- [x] Show a clear message when no alarms are pending

## CLI: `remove` (FR3)

- [x] Parse `remove <id>`
- [x] Validate that the ID exists
- [x] Delete the matching alarm from JSON and persist
- [x] Print confirmation or a useful error if the ID is not found

## Watcher: `run` (FR4–FR7)

- [x] Parse `run` and enter a foreground polling loop
- [x] Poll current time once per second against all pending alarms’ `HH:MM` values (FR5)
- [x] On match, play sound via `subprocess.run(["afplay", path_to_sound])` (FR6)
- [x] Print a ring message to stdout (visible in `nohup.out` when backgrounded)
- [x] Delete the alarm from JSON immediately after ringing so it cannot re-trigger (FR7)

## Success criteria (verification)

- [x] Verify adding, listing, and removing alarms works correctly via CLI
- [x] Verify a scheduled alarm rings audibly within 1 second of its target time
- [x] Verify a rung alarm no longer appears in `list`
- [x] Verify zero external dependencies beyond Python’s standard library

## Explicitly out of scope (do not build)

- Snooze
- Repeating/recurring alarms
- Persistence across machine restarts (`launchd`/systemd)
- GUI, web UI, or notification-center integration
- Multi-user support
- Cross-platform sound playback (Linux/Windows)
- Alarm volume control / fade-in
