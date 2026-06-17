from pathlib import Path

from . import ui
from .models import EntryLog

DATA_PATH = Path("devdiary.json")


def main():
    print(ui.SEPARATOR)
    print("Welcome to DevDiary!")
    print(ui.SEPARATOR)

    log = EntryLog.load(DATA_PATH)
    if log:
        print(f"Loaded {len(log)} entries — "
              f"last one {ui.format_time_ago(log.entries[-1])}.")
        print(f"Current streak: {log.streak()} day(s).")
    else:
        print("First session — let's go.")

    try:
        while True:
            result = ui.read_entry()
            if result == ui.QUIT_WORD:
                break
            if result == ui.LIST_WORD:
                ui.print_brief(log)
                continue
            if result == ui.STATS_WORD:
                if log:
                    ui.print_stats(log, log.stats())
                else:
                    print("(no entries yet)")
                continue
            log.append(result)
            print(f"  logged: {result.topic} ({result.minutes} min)")
    except KeyboardInterrupt:
        print("\nInterrupted — saving and exiting.")

    if not log:
        print("No entries — see you next time.")
    else:
        ui.print_report(log, log.stats())

    log.save(DATA_PATH)
