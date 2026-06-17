import pytest
from rest_framework.test import APIClient

from diary.models import Entry


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user("tester", password="pw12345")


@pytest.mark.django_db
def test_is_long_true_for_60_plus(user):
    entry = Entry.objects.create(author=user, topic="deep work", minutes=90, mood="+")
    assert entry.is_long() is True


@pytest.mark.django_db
def test_is_long_false_under_60(user):
    entry = Entry.objects.create(author=user, topic="quick note", minutes=20, mood="=")
    assert entry.is_long() is False


def test_home_requires_login(client):
    response = client.get("/")
    assert response.status_code == 302
    assert "/accounts/login/" in response.url


@pytest.mark.django_db
def test_home_shows_only_my_entries(client, django_user_model):
    alice = django_user_model.objects.create_user("alice", password="pw")
    bob = django_user_model.objects.create_user("bob", password="pw")
    Entry.objects.create(author=alice, topic="alice-secret", minutes=10, mood="+")
    Entry.objects.create(author=bob, topic="bob-secret", minutes=10, mood="+")

    client.force_login(alice)
    response = client.get("/")

    assert response.status_code == 200
    assert b"alice-secret" in response.content
    assert b"bob-secret" not in response.content


@pytest.mark.django_db
def test_api_requires_auth():
    response = APIClient().get("/api/entries/")
    assert response.status_code == 401


@pytest.mark.django_db
def test_api_create_stamps_owner(django_user_model):
    carol = django_user_model.objects.create_user("carol", password="pw")
    api = APIClient()
    api.force_authenticate(carol)

    response = api.post(
        "/api/entries/",
        {"topic": "via api", "minutes": 30, "mood": "+", "author": "hacker"},
        format="json",
    )

    assert response.status_code == 201
    assert response.data["author"] == "carol"


@pytest.mark.django_db
def test_api_list_is_paginated(django_user_model):
    user = django_user_model.objects.create_user("dave", password="pw")
    Entry.objects.create(author=user, topic="one", minutes=10, mood="+")
    Entry.objects.create(author=user, topic="two", minutes=20, mood="=")
    api = APIClient()
    api.force_authenticate(user)

    response = api.get("/api/entries/")

    assert response.status_code == 200
    assert response.data["count"] == 2
    assert "results" in response.data
    assert len(response.data["results"]) == 2


@pytest.mark.django_db
def test_filter_by_mood(django_user_model):
    user = django_user_model.objects.create_user("erin", password="pw")
    Entry.objects.create(author=user, topic="good one", minutes=10, mood="+")
    Entry.objects.create(author=user, topic="bad one", minutes=20, mood="-")

    api = APIClient()
    api.force_authenticate(user)
    response = api.get("/api/entries/", {"mood": "+"})

    assert response.status_code == 200
    topics = [e["topic"] for e in response.data["results"]]
    assert topics == ["good one"]


@pytest.mark.django_db
def test_cannot_view_others_entry(client, django_user_model):
    alice = django_user_model.objects.create_user("alice", password="pw")
    bob = django_user_model.objects.create_user("bob", password="pw")
    bobs_entry = Entry.objects.create(author=bob, topic="bob-only", minutes=5, mood="=")

    client.force_login(alice)
    response = client.get(f"/entry/{bobs_entry.pk}/")
    assert response.status_code == 404


@pytest.mark.django_db
def test_api_register_creates_user_and_returns_token(django_user_model):
    api = APIClient()

    response = api.post("/api/register/", {
        "username": "apinewbie",
        "password": "s3cure-pw-9000",
    })

    assert response.status_code == 201
    assert "token" in response.data
    assert "password" not in response.data
    user = django_user_model.objects.get(username="apinewbie")
    assert user.check_password("s3cure-pw-9000")

    api.credentials(HTTP_AUTHORIZATION=f"Token {response.data['token']}")
    assert api.get("/api/entries/").status_code == 200


@pytest.mark.django_db
def test_api_register_rejects_weak_password():
    api = APIClient()
    response = api.post("/api/register/", {"username": "weakling", "password": "123"})
    assert response.status_code == 400
    assert "password" in response.data
