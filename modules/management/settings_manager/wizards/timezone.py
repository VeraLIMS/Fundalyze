"""Wizard to set the preferred timezone."""

from zoneinfo import available_timezones

from modules.config_utils import load_settings, save_settings

LABEL = "Timezone"


def run_wizard() -> None:
    print("\n=== Timezone Setup ===")
    zones = sorted(available_timezones())
    query = input("Filter by name (e.g. 'Europe') or leave empty to list all: ").strip()
    matches = [z for z in zones if query.lower() in z.lower()] if query else zones
    if not matches:
        print("No matching timezones found.\n")
        return
    for idx, tz in enumerate(matches, start=1):
        print(f"{idx}) {tz}")
        if idx >= 50:
            break
    choice = input(f"Select 1-{min(len(matches),50)}: ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= min(len(matches),50)):
        print("Invalid choice.\n")
        return
    tz = matches[int(choice) - 1]
    settings = load_settings()
    settings["timezone"] = tz
    save_settings(settings)
    print(f"Timezone set to {tz}.\n")
