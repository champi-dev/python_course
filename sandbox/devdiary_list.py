SEPARATOR_LINE = "=" * 30

print(f"""
{SEPARATOR_LINE}
Welcome to DevDiary!
{SEPARATOR_LINE}
""")

entries = []
while True:
    topic = input("Which topic did you study? ")

    if topic.lower() == "done":
        if len(entries) == 0:
            print("No entries, exiting... ")
            break

        print(SEPARATOR_LINE)
        print("Today's entries")
        print(SEPARATOR_LINE)

        for i, entry in enumerate(entries):
            print(f"{i + 1}. {entry["topic"]}    {entry["minutes"]} min   [{entry["mood"]}]")

        print("-" * 30)
        print(f"Entries:       {len(entries)}")

        total_time = sum([e["minutes"] for e in entries])
        print(f"Total time:    {total_time} min (~{total_time / 60:.1f} hr)")

        average_time = total_time / len(entries)
        print(f"Average:       {average_time:.1f}min/entry")

        longest = max(entries, key=lambda e: e["minutes"])
        print(f"Longest:       {longest["topic"]} ({longest["minutes"]} min)")

        print(SEPARATOR_LINE)
        topics = set([e["topic"] for e in entries])
        print(f"Distinct topics: {len(topics)} {', '.join(topics)}")
        break

    minutes = int(input("How many minutes did you study? "))

    mood = input("Enter a mood +, = or - ")
    if not mood in ("+", "=", "-"):
        mood = "="

    entry = {
        "topic": topic,
        "minutes": minutes,
        "mood": mood
    }
    entries.append(entry)

    print(f"Entry saved! {topic}, {mood}, {minutes} min ")
