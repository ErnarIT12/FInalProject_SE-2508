# IP2 Final Exam — Admin Panel with Authentication & Authorization(Employee)

> **Course:** Introduction to Programming 2 (Python) — IP2  
> **University:** Astana IT University | 2025–2026  
> **Assessment:** Final Exam — 40 points (30 implementation + 10 oral defense)
> **Group Members:** Umirgaliyev Yernar, Bekpatsha Akerke, Bolatbek Nurakhmet, Yessetaiuly Inal
> **Group:** SE-2508

## Overview

A full-stack Admin Panel built with Flask, extending Assignments 3 (Flask Web App) and 4 (Telegram Bot).  
Features session-based authentication, role-based authorization, and Telegram bot notifications.

---

## Features

- **Two roles:** `admin` (full control) and `user` (read-only dashboard)
- **Admin can:** manage users, create/delete records, view all data, configure Telegram bot
- **User can:** view own records, update profile/password
- **Telegram Bot:** sends notifications on registration and admin actions
- **Pure HTML/CSS/JS** frontend — no external CSS frameworks
- **OOP backend** — all logic encapsulated in Python classes

---

## Project Structure

```
My_project/
├── app.py                     # Flask application entry point
├── config.py                  # Config class (SECRET_KEY, BOT_TOKEN, etc.)
├── requirements.txt
├── README.md
│
├── models/
│   ├── user.py                # User class (id, username, password_hash, role)
│   └── record.py              # Record class
│
├── services/
│   ├── db_service.py          # DatabaseService — reads/writes JSON files
│   └── bot_service.py         # BotService — Telegram notifications
│
├── controllers/
│   ├── auth.py                # AuthController + login_required decorator
│   ├── admin.py               # AdminController
│   └── user.py                # UserController
│
├── templates/
│   ├── base.html              # Base template with role-aware navbar
│   ├── auth/                  # login.html, register.html
│   ├── admin/                 # dashboard, users, data, bot_settings
│   ├── user/                  # dashboard, profile
│   └── errors/                # 403.html
│
├── static/
│   ├── css/style.css
│   └── js/main.js
│
├── employees.json             # Bot employee data (Telegram bot)
├── users.json                 # Auto-generated on first run
├── records.json               # Auto-generated on first run
└── bot_config.json            # Auto-generated on first run
```

---

## Setup & Installation

### 1. Clone or unzip the project

```bash
cd My_project
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure the Telegram Bot

Create a `.env` file in the project root (next to `app.py`):

```env
SECRET_KEY=your-random-secret-key
BOT_TOKEN=your-telegram-bot-token
CHAT_ID=your-telegram-chat-id
WEBHOOK_URL=https://your-ngrok-url.ngrok-free.app/webhook
DEBUG=True
```

> **How to get BOT_TOKEN:** create a bot via [@BotFather](https://t.me/BotFather) on Telegram.  
> **How to get CHAT_ID:** message [@userinfobot](https://t.me/userinfobot) on Telegram — it replies with your ID.

⚠️ Never commit the `.env` file — it is listed in `.gitignore`.

### 4. Run the application

```bash
python app.py
```

Open in browser: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## Default Accounts

> These are seeded automatically on first run — no manual setup needed.

| Role  | Username   | Password  |
|-------|------------|-----------|
| Admin | `admin`    | `admin123` |
| User  | `testuser` | `user123`  |

---

## Routes

| Method | URL                        | Access    | Description                  |
|--------|----------------------------|-----------|------------------------------|
| GET    | `/`                        | Any       | Redirects based on role      |
| GET    | `/login`                   | Public    | Login page                   |
| POST   | `/login`                   | Public    | Authenticate user            |
| GET    | `/register`                | Public    | Register page                |
| POST   | `/register`                | Public    | Create new account           |
| POST   | `/logout`                  | Any       | End session                  |
| GET    | `/admin/dashboard`         | Admin     | Stats overview               |
| GET    | `/admin/users`             | Admin     | List all users               |
| POST   | `/admin/users/create`      | Admin     | Create user                  |
| POST   | `/admin/users/delete/<id>` | Admin     | Delete user + their records  |
| GET    | `/admin/data`              | Admin     | Paginated records (10/page)  |
| POST   | `/admin/data/create`       | Admin     | Add new record               |
| POST   | `/admin/data/delete/<id>`  | Admin     | Delete record                |
| GET    | `/admin/bot-settings`      | Admin     | View/update bot token        |
| GET    | `/user/dashboard`          | User      | Own records                  |
| GET    | `/user/profile`            | User      | Profile info                 |
| POST   | `/user/profile`            | User      | Update password              |
| GET    | `/api/admin/users`         | Admin     | JSON — live search users     |
| POST   | `/webhook`                 | Telegram  | Receive bot updates          |

---

## Telegram Bot Commands

| Command                           | Description                     |
|-----------------------------------|---------------------------------|
| `/start`                          | Welcome message                 |
| `/help`                           | List all commands               |
| `/echo [text]`                    | Repeat text                     |
| `/save [Name] [Salary] [Dept] [Year]` | Save an employee            |
| `/list`                           | List your saved employees       |
| `/fact`                           | Random IT fact                  |
| `/validate [YYYY-MM-DD]`          | Validate a date                 |
| `/about`                          | About the bot                   |
| `/custom [text]`                  | Translate to Mandarin Chinese   |

---

## Security Notes

- Passwords are hashed with **SHA-256** via `hashlib` — never stored as plain text
- Sessions managed by Flask with a secret key
- `login_required` decorator protects all routes — unauthorized users get redirected to `/login`, wrong role gets `403`
- Admin cannot delete their own account
- Bot token and Chat ID should be stored in environment variables (`.env`) for production use — never commit real tokens to git

---

## Requirements

```
Flask==3.0.0
pyTelegramBotAPI==4.14.0
python-telegram-bot>=20.0
python-dotenv
```

Install all at once:

```bash
pip install -r requirements.txt
```