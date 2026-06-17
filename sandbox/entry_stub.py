from datetime import date

today = date.today()
topic = input("Enter a topic u learned today ")
minutes = input("How many minutes did u spend on it? ")
mood = input("Describe ur mood as a single char ")
hours = int(minutes) / 60
SEPARATOR_LINE = "=" * 60

print(f"""
{SEPARATOR_LINE}
DevDiary entry - {today}
{SEPARATOR_LINE}
Topic:  {topic}
Time:   {minutes} min (~{hours:.1f} hr)
Mood:   {mood}
""")

if mood == "+":
    print("Great session!")
elif mood == "-":
    print("Tough day. Keep going.")

