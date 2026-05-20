from functools import wraps

from flask import abort, redirect, session, url_for


def login_required(role=None):
    def decorator(view):
        @wraps(view)
        def wrapper(*args, **kwargs):
            if "user_id" not in session:
                return redirect(url_for("login"))
            if role and session.get("role") != role:
                abort(403)
            return view(*args, **kwargs)
        return wrapper
    return decorator


class AuthController:
    def __init__(self, db_service, bot_service):
        self.db = db_service
        self.bot = bot_service

    def login(self, username, password):
        user = self.db.get_user_by_username(username)
        if not user or not user.check_password(password):
            raise ValueError("Invalid username or password")
        session["user_id"] = user.id
        session["username"] = user.username
        session["role"] = user.role
        return user

    def logout(self):
        session.clear()

    def register(self, username, password):
        if len(username.strip()) < 3:
            raise ValueError("Username must be at least 3 characters")
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters")
        user = self.db.add_user(username, password, "user")
        self.bot.notify_new_user(user.username)
        return user
