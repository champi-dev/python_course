import pytest
from datetime import datetime, timedelta
from devdiary.models import Entry, EntryLog


def test_equal_entries_ignore_timestamp():
    assert Entry("recursion", 25, "+") == Entry("recursion", 25, "+")


def test_negative_minutes_rejected():
    with pytest.raises(ValueError):
        Entry("oops", -5)


def test_bad_mood_falls_back():
    assert Entry("x", 10, "banana").mood == Entry.DEFAULT_MOOD


def test_log_roundtrip(tmp_path):
    path = tmp_path / "diary.json"
    log = EntryLog([Entry("a", 10), Entry("b", 20)])
    log.save(path)
    loaded = EntryLog.load(path)
    assert list(loaded) == list(log)


def test_topic_gets_stripped():
    assert Entry(" py ", 5).topic == "py"


def test_empty_topic_rejected():
    with pytest.raises(ValueError):
        Entry("   ", 5)


def test_streak_counts_consecutive_days():
    today = datetime.now()
    log = EntryLog([
        Entry("a", 10, created_at=today),
        Entry("b", 10, created_at=today - timedelta(days=1)),
    ])
    assert log.streak() == 2

    gappy = EntryLog([
        Entry("a", 10, created_at=today),
        Entry("b", 10, created_at=today - timedelta(days=3)),
    ])
    assert gappy.streak() == 1


def test_contains_matches_topic_string():
    log = EntryLog([Entry("recursion", 30)])
    assert "recursion" in log
    assert "django" not in log


def test_sorted_orders_chronologically():
    now = datetime.now()
    old = Entry("old", 10, created_at=now - timedelta(hours=2))
    new = Entry("new", 10, created_at=now)
    assert sorted([new, old]) == [old, new]
