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
                return cls()
        return cls(Entry.from_dict(d) for d in data)
