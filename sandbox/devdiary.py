from datetime import datetime, date, timedelta
from pathlib import Path
import json

DATA_PATH = Path("devdiary.json")
SEPARATOR = "=" * 60
DIVIDER = "-" * 60
QUIT_WORD = "done"
LIST_WORD = "list"
STATS_WORD = "stats"
VALID_MOODS = ("+", "=", "-")
DEFAULT_MOOD = "="


def load_entries(path):
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_entries(entries, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)


def read_entry():
    topic = input(f"Topic (or '{QUIT_WORD}' / '{LIST_WORD}' / '{STATS_WORD}'): ").strip()
    low = topic.lower()
    if low == QUIT_WORD:
        return QUIT_WORD
    if low == LIST_WORD:
        return LIST_WORD
    if low == STATS_WORD:
        return STATS_WORD

    minutes = int(input("Minutes: "))
    mood = input(f"Mood [{'/'.join(VALID_MOODS)}]: ").strip()
    if mood not in VALID_MOODS:
        mood = DEFAULT_MOOD

    return {
        "topic": topic,
        "minutes": minutes,
        "mood": mood,
        "created_at": datetime.now().isoformat(),
    }


def calculate_stats(entries):
    minutes_list = [e["minutes"] for e in entries]
    return {
        "count": len(entries),
        "total_minutes": sum(minutes_list),
        "average": sum(minutes_list) / len(entries),
        "longest": max(entries, key=lambda e: e["minutes"]),
    }


def format_time_ago(iso_string):
    last_at = datetime.fromisoformat(iso_string)
    seconds = (datetime.now() - last_at).total_seconds()
    if seconds < 3600:
        return f"{seconds / 60:.0f}m ago"
    if seconds < 86400:
        return f"{seconds / 3600:.1f}h ago"
    return f"{seconds / 86400:.0f}d ago"


def compute_streak(entries):
    if not entries:
        return 0
    entry_dates = {
        datetime.fromisoformat(e["created_at"]).date()
        for e in entries
    }
    streak = 0
    day = date.today()
    while day in entry_dates:
        streak += 1
        day -= timedelta(days=1)
    return streak


def format_entry_row(index, entry):
    when = datetime.fromisoformat(entry["created_at"]).strftime("%H:%M")
    return (
        f"[{index}] {entry['topic']:<15} "
        f"{when}  {entry['minutes']:>3} min  {entry['mood']}"
    )


def print_brief(entries):
    if not entries:
        print("(no entries yet)")
        return
    print(DIVIDER)
    for i, entry in enumerate(entries, start=1):
        print(format_entry_row(i, entry))
    print(DIVIDER)


def print_stats(entries, stats):
    print(DIVIDER)
    print(f"Entries:         {stats['count']}")
    print(f"Total time:      {stats['total_minutes']} min "
          f"(~{stats['total_minutes'] / 60:.1f} hr)")
    print(f"Average:         {stats['average']:.1f} min/entry")
    print(f"Longest:         {stats['longest']['topic']} "
          f"({stats['longest']['minutes']} min)")
    topics = {e["topic"] for e in entries}
    print(f"Distinct topics: {len(topics)} ({', '.join(sorted(topics))})")
    print(f"Current streak:  {compute_streak(entries)} day(s)")
    print(DIVIDER)


def print_report(entries, stats):
    print()
    print(SEPARATOR)
    print("All entries")
    print(SEPARATOR)
    for i, entry in enumerate(entries, start=1):
        print(format_entry_row(i, entry))
    print_stats(entries, stats)


def main():
    print(SEPARATOR)
    print("Welcome to DevDiary!")
    print(SEPARATOR)

    entries = load_entries(DATA_PATH)
    if entries:
        print(f"Loaded {len(entries)} entries — "
              f"last one {format_time_ago(entries[-1]['created_at'])}.")
        print(f"Current streak: {compute_streak(entries)} day(s).")
    else:
        print("First session — let's go.")

    while True:
        result = read_entry()
        if result == QUIT_WORD:
            break
        if result == LIST_WORD:
            print_brief(entries)
            continue
        if result == STATS_WORD:
            if entries:
                print_stats(entries, calculate_stats(entries))
            else:
                print("(no entries yet)")
            continue
        entries.append(result)
        print(f"  logged: {result['topic']} ({result['minutes']} min)")

    if not entries:
        print("No entries — see you next time.")
    else:
        print_report(entries, calculate_stats(entries))

    save_entries(entries, DATA_PATH)


if __name__ == "__main__":
    main()
