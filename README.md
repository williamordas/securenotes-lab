# SecureNotes API — Completed Combined Lab

This project completes the Weeks 14–15 **Secure It, Then Prove It** laboratory activity.

## What's implemented

- Bcrypt password hashing and password verification.
- Signed JWT access tokens with a `sub` claim and a 30-minute expiry.
- Fail-closed authentication for missing, invalid, expired, and unknown-user tokens.
- Note ownership checks that return HTTP 403 when a user tries to read another user's note.
- An admin-only user listing that returns only `id`, `username`, and `is_admin`.
- Eleven API/security tests with real assertions, plus a completed `TASKS.md` checklist and reflection.

## Run on Windows (PowerShell)

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
pytest -q
uvicorn app.main:app --reload
```

Then open http://127.0.0.1:8000/docs.

Seeded accounts: `admin/admin123` (admin), `alice/alicepass` (note 1), and `bob/bobpass` (note 2).

> Keep the `bcrypt==4.0.1` pin in `requirements.txt`; the lab specifies this version for compatibility with Passlib.

## Coverage

```powershell
pytest --cov=app .
```

## GitHub peer review

The code and tests are ready to commit. The handout's repository setup, branch push, pull request, partner review, and LMS submission steps still need to be completed using your own GitHub account and course workflow.
