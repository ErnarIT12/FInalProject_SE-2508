# IP2 Assignment 4 - Telegram Bot with Flask

## Project Description

This project is a webhook-powered Telegram bot for **Introduction to Programming 2 (Python), Assignment 4**.

The bot manages employee records from the previous Assignment 3 topic and demonstrates:

- Flask webhook server
- pyTelegramBotAPI
- Object-Oriented Programming
- modules and packages
- decorators
- generators
- regular expressions
- JSON file storage

## Topic

**Group 4 - Employee**

Each employee record contains:

| Field | Description |
| --- | --- |
| id | Auto-incremented employee ID |
| user_id | Telegram user who saved the employee |
| name | Employee name |
| salary | Employee salary |
| department | Department name |
| worked_since | Year when the employee started working |

## Project Structure

```text
My_project/
├── app.py
├── config.py
├── employees.json
├── requirements.txt
└── bot/
    ├── __init__.py
    ├── handlers.py
    ├── models.py
    └── utils.py
```

## Requirements Coverage

- `app.py` registers a Flask `POST /webhook` route.
- `bot/models.py` contains `Person` and `Employee` classes.
- `Employee` inherits from `Person`.
- `Employee` uses encapsulation with a private `__salary` attribute and `salary` property.
- `Employee` has custom method `to_dict()`.
- `bot/utils.py` contains custom decorator `@log_command`.
- `bot/utils.py` contains generator `fact_generator()`.
- `bot/utils.py` uses regex in `is_valid_date()`.
- `bot/handlers.py` implements all required commands and one bonus command.

## Bot Commands

| Command | Description |
| --- | --- |
| `/start` | Welcome message |
| `/help` | List all commands |
| `/echo text` | Reply with the same text |
| `/save Name Salary Department Year` | Save an employee |
| `/list` | List employees saved by the current Telegram user |
| `/fact` | Return the next fact from the generator |
| `/validate YYYY-MM-DD` | Validate date format using regex |
| `/about` | Show bot info and demonstrate OOP `__str__` |
| `/custom text` | Bonus: translate simple text to Mandarin Chinese |

## Setup

1. Create and activate a virtual environment.

```bash
python -m venv .venv
.venv\Scripts\activate
```

2. Install dependencies.

```bash
pip install -r My_project/requirements.txt
```

3. Create a Telegram bot with BotFather and put your data in `My_project/config.py`.

```python
BOT_TOKEN = "YOUR_REAL_BOT_TOKEN"
WEBHOOK_URL = "https://your-ngrok-url.ngrok-free.app/webhook"
```

4. Start ngrok.

```bash
ngrok http 5000
```

5. Run Flask.

```bash
cd My_project
python app.py
```

## Mode

This submitted version uses **webhook mode** with Flask.

## Submission Notes

Before uploading the ZIP to Moodle:

- Do not include a real Telegram bot token.
- Keep a fake placeholder token such as `BOT_TOKEN = "0000000000:YOUR_BOT_TOKEN_HERE"` in submitted `config.py`.
- Add screenshots or a short screen recording showing `/start`, `/save`, `/list`, and `/validate`.

## Group

SE-2508

Group members: Umirgaliyev Yernar, Bekpatsha Akerke, Bolatbek Nurakhmet, Yessetaiuly Inal
