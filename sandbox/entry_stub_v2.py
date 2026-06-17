from datetime import date
SEPARATOR_LINE = "=" * 60

today = date.today()
topic = input("Enter a topic u learned today ")

minutes = int(input("How many minutes did u spend on it? "))
if minutes <= 0:
    print("Minutes must be positive - exiting.")
    exit()

hours = minutes / 60

mood = input("Describe ur mood as a single char ")
if mood not in "+=-":
    print("Mood not recognized - defaulting to '='")
    mood = "="

mood_message = ""
if mood == "+":
    mood_message = "Great session!"
elif mood == "=":
    mood_message = "Steady progress."
elif mood == "-":
    mood_message = "Tough day. Keep going."

category = ""
if minutes < 15:
    category = "quick"
elif 15 <= minutes <= 45:
    category = "focused"
elif 46 <= minutes <= 120:
    category = "deep"
elif minutes > 120:
    category = "marathon"

print(f"""
{SEPARATOR_LINE}
DevDiary entry - {today}
{SEPARATOR_LINE}
Topic:    {topic}
Time:     {minutes} min (~{hours:.1f} hr)
Category: {category}
Mood:     {mood}
Note:     {mood_message}
{"Don't forget to rest your eyes." if category == "marathon" else ""}
""")
