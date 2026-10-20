"""API behaviour tests for the SecureNotes lab."""
from tests.conftest import login, auth


def test_home_ok(client):
    res = client.get("/")
    assert res.status_code == 200
    assert res.json()["service"] == "SecureNotes API"


def test_register_then_login(client):
    registered = client.post("/register", json={"username": "charlie", "password": "charliepass"})
    assert registered.status_code == 200

    res = client.post("/login", json={"username": "charlie", "password": "charliepass"})
    assert res.status_code == 200
    token = res.json()["access_token"]
    assert isinstance(token, str)
    assert token.count(".") == 2
    assert res.json()["token_type"] == "bearer"


def test_login_wrong_password_is_401(client):
    res = client.post("/login", json={"username": "alice", "password": "wrong-password"})
    assert res.status_code == 401


def test_create_then_list_own_note(client):
    token = login(client, "alice", "alicepass")
    assert token is not None

    created = client.post(
        "/notes",
        json={"title": "Lab note", "body": "A new private note"},
        headers=auth(token),
    )
    assert created.status_code == 200

    listed = client.get("/notes", headers=auth(token))
    assert listed.status_code == 200
    assert any(note["title"] == "Lab note" for note in listed.json())
