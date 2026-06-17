from pathlib import Path
from datetime import datetime
import json

PATH = Path("devdiary.json")
SEPARATOR_LINE = "=" * 30
DIVIDER = "-" * 30
QUIT_WORD = "done"
LIST_WORD = "list"
VALID_MOODS = ("+", "-", "=")
DEFAULT_MOOD = VALID_MOODS[2]

def main():
    print(f"""
{SEPARATOR_LINE}
Welcome to DevDiary!
{SEPARATOR_LINE}
""")

    entries = load_entries(PATH)
    if len(entries) > 0:
        print(f"Loaded {len(entries)} entries.")
        print(f"Most recent entry logged {format_time_ago(entries[-1]["created_at"])}")
    while True:
        single_entry = read_entry()
        if single_entry == QUIT_WORD:
            break

        if single_entry == LIST_WORD:
            print_brief(entries)
            continue

        entries.append(single_entry)

    if len(entries) == 0:
        print("No entries, exiting... ")
    else:
        stats = calculate_stats(entries)
        print_report(entries, stats)

    save_entries(entries, PATH)

def load_entries(entries_path):
    if not entries_path.exists():
        return []
    with open(entries_path, encoding="utf-8") as f:
        return json.load(f)

def save_entries(entries, entries_path):
    with open(entries_path, mode="w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)

def read_entry():
    topic = input("Enter a topic: ")
    if topic.lower() == QUIT_WORD:
        return QUIT_WORD

    if topic.lower() == LIST_WORD:
        return LIST_WORD

    minutes = int(input("How many minutes did you study? "))

    mood = input("Enter one of these moods +, =, -: ")
    if mood not in VALID_MOODS:
        mood = DEFAULT_MOOD

    return {
        "topic": topic,
        "minutes": minutes,
        "mood": mood,
        "created_at": datetime.now().isoformat()
    }

def calculate_stats(entries=None):
    if entries is None:
        entries = []

    count = len(entries)
    total_minutes = sum([e["minutes"] for e in entries])
    average = total_minutes / count
    longest = max(entries, key=lambda e: e["minutes"])

    return {
        "count": count,
        "total_minutes": total_minutes,
        "average": average,
        "longest": longest
    }

def format_time_ago(iso_string):
    delta = datetime.now() - datetime.fromisoformat(iso_string)
    hours = delta.total_seconds() / 3600

    if hours >= 1:
        return f"{hours:.0f}h ago"
    return f"{hours*60:.0f}m ago"

def print_brief(entries):
    for i, entry in enumerate(entries):
        print(f"{i + 1}: {entry["topic"]}")

def print_report(entries, stats):
    print(SEPARATOR_LINE)
    print("All entries")
    print(SEPARATOR_LINE)

    for i, entry in enumerate(entries):
        print(f"{i + 1}. {entry["topic"]} {datetime.fromisoformat(entry["created_at"]).strftime("%H:%M")}    {entry["minutes"]} min   [{entry["mood"]}]")

    print(DIVIDER)
    print(f"Entries:       {len(entries)}")
    print(f"Total time:    {stats["total_minutes"]} min (~{stats["total_minutes"] / 60:.1f} hr)")
    print(f"Average:       {stats["average"]:.1f}min/entry")
    print(f"Longest:       {stats["longest"]["topic"]} ({stats["longest"]["minutes"]} min)")
    print(SEPARATOR_LINE)
    topics = set([e["topic"] for e in entries])
    print(f"Distinct topics: {len(topics)} {', '.join(topics)}")

if __name__ == "__main__":
    main()
