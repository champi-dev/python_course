from dataclasses import dataclass, field
from datetime import datetime, date, timedelta
from pathlib import Path
from typing import ClassVar
import json


@dataclass
class Entry:
    VALID_MOODS: ClassVar[tuple] = ("+", "=", "-")
    DEFAULT_MOOD: ClassVar[str] = "="

    topic: str
    minutes: int
    mood: str = DEFAULT_MOOD
    created_at: datetime = field(default_factory=datetime.now, compare=False)

    def __post_init__(self):
        self.topic = self.topic.strip()
        if not self.topic:
            raise ValueError("topic cannot be empty")
        if self.minutes < 0:
            raise ValueError("minutes must be non-negative")
        if self.mood not in self.VALID_MOODS:
            self.mood = self.DEFAULT_MOOD

    def __lt__(self, other):
        if not isinstance(other, Entry):
            return NotImplemented
        return self.created_at < other.created_at

    def format_row(self, index):
        when = self.created_at.strftime("%H:%M")
        return (f"[{index}] {self.topic:<15} "
                f"{when}  {self.minutes:>3} min  {self.mood}")

    def age(self):
        return datetime.now() - self.created_at

    def to_dict(self):
        return {
            "topic": self.topic,
            "minutes": self.minutes,
            "mood": self.mood,
            "created_at": self.created_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            topic=data["topic"],
            minutes=data["minutes"],
            mood=data["mood"],
            created_at=datetime.fromisoformat(data["created_at"]),
        )


@dataclass
class MilestoneEntry(Entry):
    note: str = ""

    def format_row(self, index):
        return "* " + super().format_row(index)


class EntryLog:
    def __init__(self, entries: list = None):
        self.entries = list(entries) if entries else []

    def append(self, entry: Entry) -> None:
        self.entries.append(entry)

    def __len__(self) -> int:
        return len(self.entries)

    def __iter__(self):
        return iter(self.entries)

    def __contains__(self, topic: str) -> bool:
        return any(e.topic == topic for e in self.entries)

    def stats(self) -> dict:
        minutes = [e.minutes for e in self.entries]
        return {
            "count": len(self),
            "total_minutes": sum(minutes),
            "average": sum(minutes) / len(self.entries),
            "longest": max(self.entries, key=lambda e: e.minutes),
        }

    def streak(self) -> int:
        if not self.entries:
            return 0
        dates = {e.created_at.date() for e in self.entries}
        streak, day = 0, date.today()
        while day in dates:
            streak += 1
            day -= timedelta(days=1)
        return streak

    def save(self, path: Path) -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump([e.to_dict() for e in self.entries], f,
                      indent=2, ensure_ascii=False)

    @classmethod
    def load(cls, path: Path) -> "EntryLog":
        if not path.exists():
            return cls()
        with open(path, encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                print("devdiary.json is corrupted - starting fresh.")
                return cls()
        return cls(Entry.from_dict(d) for d in data)


DATA_PATH = Path("devdiary.json")
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


def main():
    print(SEPARATOR)
    print("Welcome to DevDiary!")
    print(SEPARATOR)

    log = EntryLog.load(DATA_PATH)
    if log:
        print(f"Loaded {len(log)} entries — "
              f"last one {format_time_ago(log.entries[-1])}.")
        print(f"Current streak: {log.streak()} day(s).")
    else:
        print("First session — let's go.")

    try:
        while True:
            result = read_entry()
            if result == QUIT_WORD:
                break
            if result == LIST_WORD:
                print_brief(log)
                continue
            if result == STATS_WORD:
                if log:
                    print_stats(log, log.stats())
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
        print_report(log, log.stats())

    log.save(DATA_PATH)


if __name__ == "__main__":
    main()
