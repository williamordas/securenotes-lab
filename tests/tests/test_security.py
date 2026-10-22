"""Security tests for the SecureNotes lab."""
from tests.conftest import login, auth


def test_protected_route_rejects_no_token(client):
    res = client.get("/notes")
    assert res.status_code == 401


def test_protected_route_rejects_bad_token(client):
    res = client.get("/notes", headers=auth("not.a.jwt"))
    assert res.status_code == 401


def test_user_cannot_read_another_users_note(client):
    alice = login(client, "alice", "alicepass")
    res = client.get("/notes/2", headers=auth(alice))
    assert res.status_code == 403


def test_user_can_read_own_note(client):
    alice = login(client, "alice", "alicepass")
    res = client.get("/notes/1", headers=auth(alice))
    assert res.status_code == 200
    assert res.json()["title"] == "Alice diary"


def test_login_does_not_reveal_which_field_was_wrong(client):
    unknown_user = client.post("/login", json={"username": "no-such-user", "password": "anything"})
    wrong_password = client.post("/login", json={"username": "alice", "password": "wrong-password"})
    assert unknown_user.status_code == wrong_password.status_code == 401
    assert unknown_user.json() == wrong_password.json()


def test_non_admin_cannot_list_users(client):
    alice = login(client, "alice", "alicepass")
    res = client.get("/admin/users", headers=auth(alice))
    assert res.status_code == 403


def test_admin_can_list_users_without_password_leak(client):
    admin = login(client, "admin", "admin123")
    res = client.get("/admin/users", headers=auth(admin))
    assert res.status_code == 200
    users = res.json()
    assert users
    assert all("password" not in user for user in users)
    assert all(set(user) == {"id", "username", "is_admin"} for user in users)
