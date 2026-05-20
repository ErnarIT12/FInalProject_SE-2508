# IP2 Final Exam - Admin Panel with Authentication

## Project Description

This is a Flask admin panel for the IP2 Final Exam. It extends the previous employee records project with authentication, authorization, role-based dashboards, JSON storage, and Telegram admin notifications.

## Features

- Login, logout, and registration with Flask sessions.
- Two roles: `admin` and `user`.
- Admin dashboard with total users, total records, and recent users.
- Admin user management: list, create, delete users.
- Admin records page with pagination.
- User dashboard with the logged-in user's own records.
- User profile page with password update.
- Passwords are hashed with SHA-256 using `hashlib`.
- Telegram notification service for new registrations and admin actions.
- Plain HTML/CSS/JS frontend with Jinja2 template inheritance.
- Client-side validation, delete confirmation, and fetch-based user search.

## Project Structure

```text
My_project/
├── app.py
├── config.py
├── requirements.txt
├── users.json
├── records.json
├── controllers/
│   ├── auth.py
│   ├── admin.py
│   └── user.py
├── models/
│   ├── user.py
│   └── record.py
├── services/
│   ├── db_service.py
│   └── bot_service.py
├── templates/
│   ├── base.html
│   ├── auth/
│   ├── admin/
│   ├── user/
│   └── errors/
└── static/
    ├── css/style.css
    └── js/main.js
```

## Default Accounts

Admin account:

```text
username: admin
password: admin123
```

User account:

```text
username: testuser
password: user123
```

## How to Run

```bash
cd My_project
pip install -r requirements.txt
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## Telegram Setup

In `config.py`, replace placeholders only when demonstrating Telegram notifications:

```python
class Config:
    BOT_TOKEN = "YOUR_REAL_BOT_TOKEN"
    CHAT_ID = "YOUR_ADMIN_CHAT_ID"
```

Do not submit real tokens to Moodle. If the bot token or chat ID is wrong, the Flask app logs the error and continues working.

## Criteria Coverage

- T1: `User`, `Record`, and `DatabaseService` are implemented with `to_dict()` and `from_dict()`.
- T2: `AuthController` handles login, logout, registration, sessions, and `login_required`.
- T3: `AdminController` handles admin dashboard, users, records, role checks, and bot notifications.
- T4: `UserController` handles profile, password update, own records, and record creation.
- T5: Templates extend `base.html`; custom CSS and JS are in `static/`.
- T6: `BotService` sends Telegram notifications and catches errors.

## Defense Notes

Session stores:

```text
user_id, username, role
```

Deleting a user also deletes all records with the same `user_id` from `records.json`.

Duplicate usernames are blocked in `DatabaseService.add_user()`.

Passwords are never stored as plain text; `User.hash_password()` creates SHA-256 hashes.

## Submission

Do not include:

- `venv/`
- `__pycache__/`
- `.env`
- real Telegram tokens
