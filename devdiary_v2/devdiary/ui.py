from .models import Entry, EntryLog

SEPARATOR = "=" * 60
DIVIDER = "-" * 60
QUIT_WORD = "done"
LIST_WORD = "list"
STATS_WORD = "stats"


def read_entry():
    topic = input(f"Topic (or '{QUIT_WORD}' / '{LIST_WORD}' / '{STATS_WORD}'): ").strip()
    low = topic.lower()
    if low == QUIT_WORD:
        return QUIT_WORD
    if low == LIST_WORD:
        return LIST_WORD
    if low == STATS_WORD:
        return STATS_WORD

    error_counter = 0
    while True:
        if error_counter == 3:
            return QUIT_WORD
        try:
            minutes = int(input("Minutes: "))
            mood = input(f"Mood [{'/'.join(Entry.VALID_MOODS)}]: ").strip()
            return Entry(topic, minutes, mood)
        except ValueError as e:
            error_counter += 1
            print(f"Error: {e}")


def format_time_ago(entry: Entry) -> str:
    seconds = entry.age().total_seconds()
    if seconds < 3600:
        return f"{seconds / 60:.0f}m ago"
    if seconds < 86400:
        return f"{seconds / 3600:.1f}h ago"
    return f"{seconds / 86400:.0f}d ago"


def print_brief(log: EntryLog) -> None:
    if not log:
        print("(no entries yet)")
        return
    print(DIVIDER)
    for i, entry in enumerate(log, start=1):
        print(entry.format_row(i))
    print(DIVIDER)


def print_stats(log: EntryLog, stats: dict) -> None:
    print(DIVIDER)
    print(f"Entries:         {stats['count']}")
    print(f"Total time:      {stats['total_minutes']} min "
          f"(~{stats['total_minutes'] / 60:.1f} hr)")
    print(f"Average:         {stats['average']:.1f} min/entry")
    print(f"Longest:         {stats['longest'].topic} "
          f"({stats['longest'].minutes} min)")
    topics = {e.topic for e in log}
    print(f"Distinct topics: {len(topics)} ({', '.join(sorted(topics))})")
    print(f"Current streak:  {log.streak()} day(s)")
    print(DIVIDER)


def print_report(log: EntryLog, stats: dict) -> None:
    print()
    print(SEPARATOR)
    print("All entries")
    print(SEPARATOR)
    for i, entry in enumerate(log, start=1):
        print(entry.format_row(i))
    print_stats(log, stats)
