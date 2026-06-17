separator_line = "=" * 30

def main():
    print(f"""
{separator_line}
Welcome to DevDiary!
{separator_line}
""")

    entries = []
    while True:
        single_entry = read_entry()
        if single_entry is None:
            break

        entries.append(single_entry)

    if len(entries) == 0:
        print("No entries, exiting... ")
    else:
        stats = calculate_stats(entries)
        print_report(entries, stats)


def read_entry():
    topic = input("Enter a topic: ")
    if topic.lower() == "done":
        return None

    minutes = int(input("How many minutes did you study? "))

    mood = input("Enter one of these moods +, =, -: ")
    if mood not in ("+", "-", "="):
        mood = "="

    return {
        "topic": topic,
        "minutes": minutes,
        "mood": mood
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

def print_report(entries, stats):
    print(separator_line)
    print("Today's entries")
    print(separator_line)

    for i, entry in enumerate(entries):
        print(f"{i + 1}. {entry["topic"]}    {entry["minutes"]} min   [{entry["mood"]}]")

    print("-" * 30)
    print(f"Entries:       {len(entries)}")
    print(f"Total time:    {stats["total_minutes"]} min (~{stats["total_minutes"] / 60:.1f} hr)")
    print(f"Average:       {stats["average"]:.1f}min/entry")
    print(f"Longest:       {stats["longest"]["topic"]} ({stats["longest"]["minutes"]} min)")
    print(separator_line)
    topics = set([e["topic"] for e in entries])
    print(f"Distinct topics: {len(topics)} {', '.join(topics)}")

main()
