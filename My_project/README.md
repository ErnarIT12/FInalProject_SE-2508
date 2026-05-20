# IP2 Final Exam - Admin Panel with Authentication

Run from this folder:

```bash
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`.

Default accounts:

```text
admin / admin123
testuser / user123
```

Configure Telegram notifications in `config.py` by setting `Config.BOT_TOKEN` and `Config.CHAT_ID`. Do not submit real tokens.

Main criteria implemented:

- OOP models: `models/user.py`, `models/record.py`
- JSON service: `services/db_service.py`
- Telegram service: `services/bot_service.py`
- Auth controller and `login_required`: `controllers/auth.py`
- Admin controller: `controllers/admin.py`
- User controller: `controllers/user.py`
- Jinja templates: `templates/`
- Custom CSS/JS: `static/`