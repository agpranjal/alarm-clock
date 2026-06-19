#!/usr/bin/env python3
"""CLI alarm clock."""

import argparse
import json
import re
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import TypedDict

# macOS system sound played via afplay when an alarm rings
DEFAULT_SOUND = Path("/System/Library/Sounds/Ping.aiff")

PROJECT_DIR = Path(__file__).resolve().parent
ALARMS_DIR = PROJECT_DIR / ".alarmclock"
ALARMS_FILE = ALARMS_DIR / "alarms.json"


class Alarm(TypedDict):
    id: int
    time: str


class AlarmWithLabel(Alarm, total=False):
    label: str


def load_alarms() -> list[AlarmWithLabel]:
    if not ALARMS_FILE.exists():
        return []
    with ALARMS_FILE.open(encoding="utf-8") as f:
        return json.load(f)


def save_alarms(alarms: list[AlarmWithLabel]) -> None:
    ALARMS_DIR.mkdir(parents=True, exist_ok=True)
    with ALARMS_FILE.open("w", encoding="utf-8") as f:
        json.dump(alarms, f, indent=2)
        f.write("\n")


def next_alarm_id(alarms: list[AlarmWithLabel]) -> int:
    if not alarms:
        return 1
    return max(alarm["id"] for alarm in alarms) + 1


TIME_PATTERN = re.compile(r"^([01]\d|2[0-3]):([0-5]\d)$")


def validate_time(time_str: str) -> str:
    if not TIME_PATTERN.match(time_str):
        raise SystemExit(f"Invalid time '{time_str}': expected HH:MM (24-hour)")
    return time_str


def cmd_add(args: argparse.Namespace) -> None:
    time_str = validate_time(args.time)
    alarms = load_alarms()
    alarm: AlarmWithLabel = {"id": next_alarm_id(alarms), "time": time_str}
    if args.label:
        alarm["label"] = args.label
    alarms.append(alarm)
    save_alarms(alarms)
    print(f"Added alarm {alarm['id']} at {time_str}")


def cmd_list(args: argparse.Namespace) -> None:
    alarms = load_alarms()
    if not alarms:
        print("No pending alarms.")
        return
    for alarm in alarms:
        label = alarm.get("label", "")
        if label:
            print(f"{alarm['id']}  {alarm['time']}  {label}")
        else:
            print(f"{alarm['id']}  {alarm['time']}")


def cmd_remove(args: argparse.Namespace) -> None:
    alarms = load_alarms()
    for index, alarm in enumerate(alarms):
        if alarm["id"] == args.id:
            alarms.pop(index)
            save_alarms(alarms)
            print(f"Removed alarm {args.id}")
            return
    raise SystemExit(f"Alarm {args.id} not found")


def cmd_run(args: argparse.Namespace) -> None:
    while True:
        now = datetime.now().strftime("%H:%M")
        alarms = load_alarms()
        remaining: list[AlarmWithLabel] = []

        for alarm in alarms:
            if alarm["time"] == now:
                label = alarm.get("label", "")
                message = f"Alarm {alarm['id']} at {alarm['time']}"
                if label:
                    message += f" ({label})"
                print(message, flush=True)
                subprocess.run(["afplay", str(DEFAULT_SOUND)], check=False)
            else:
                remaining.append(alarm)

        if len(remaining) != len(alarms):
            save_alarms(remaining)

        time.sleep(1)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="alarm.py",
        description="A lightweight command-line alarm clock.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Schedule a new alarm")
    add_parser.add_argument("time", help="Alarm time in HH:MM (24-hour)")
    add_parser.add_argument("--label", help="Optional label for the alarm")
    add_parser.set_defaults(func=cmd_add)

    subparsers.add_parser("list", help="List pending alarms").set_defaults(func=cmd_list)

    remove_parser = subparsers.add_parser("remove", help="Remove an alarm by ID")
    remove_parser.add_argument("id", type=int, help="Alarm ID to remove")
    remove_parser.set_defaults(func=cmd_remove)

    subparsers.add_parser("run", help="Start the alarm watcher").set_defaults(func=cmd_run)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
