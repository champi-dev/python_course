SEPARATOR_LINE = "=" * 60

print(f"""
{SEPARATOR_LINE}
Welcome to DevDiary!
{SEPARATOR_LINE}
""")

minutes_acc = 0
logged_acc = 0
while True:
    topic = input("Enter the topic you studied ")

    if topic.lower() == "done":
        if logged_acc == 0:
            print("No entries logged. See you next time")
        else:
            print(f"""
{SEPARATOR_LINE}
Session summary
{SEPARATOR_LINE}
Entries logged: {logged_acc}
Total time: {minutes_acc} min (~{(minutes_acc / 60):.1f} hr)
{SEPARATOR_LINE}
""")
        break

    minutes = int(input("How many minutes did you study? "))
    minutes_acc += minutes

    print(f"logged: {topic} ({minutes} min).")
    logged_acc += 1
