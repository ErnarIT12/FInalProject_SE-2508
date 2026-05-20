import logging

import telebot
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for

from config import Config
from controllers.admin import AdminController
from controllers.auth import AuthController, login_required
from controllers.user import UserController
from services.bot_service import BotService
from services.db_service import DatabaseService
from bot import bot as telegram_bot


app = Flask(__name__)
app.config["SECRET_KEY"] = Config.SECRET_KEY

db_service = DatabaseService(Config.DB_PATH)
bot_settings = db_service.get_bot_settings(Config.BOT_TOKEN, Config.CHAT_ID)
bot_service = BotService(bot_settings["bot_token"], bot_settings["chat_id"])
auth_controller = AuthController(db_service, bot_service)
admin_controller = AdminController(db_service, bot_service)
user_controller = UserController(db_service)


@app.context_processor
def inject_session_user():
    return {"current_user": session}


@app.route("/")
def index():
    if "user_id" not in session:
        return redirect(url_for("login"))
    if session.get("role") == "admin":
        return redirect(url_for("admin_dashboard"))
    return redirect(url_for("user_dashboard"))


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        try:
            user = auth_controller.login(request.form["username"], request.form["password"])
            if user.role == "admin":
                return redirect(url_for("admin_dashboard"))
            return redirect(url_for("user_dashboard"))
        except ValueError as exc:
            error = str(exc)
    return render_template("auth/login.html", error=error)


@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        try:
            auth_controller.register(request.form["username"], request.form["password"])
            flash("Account created successfully. You can log in now.", "success")
            return redirect(url_for("login"))
        except ValueError as exc:
            error = str(exc)
    return render_template("auth/register.html", error=error)


@app.route("/logout", methods=["POST"])
def logout():
    auth_controller.logout()
    return redirect(url_for("login"))


@app.route("/admin/dashboard")
@login_required(role="admin")
def admin_dashboard():
    return render_template("admin/dashboard.html", stats=admin_controller.dashboard_stats())


@app.route("/admin/users")
@login_required(role="admin")
def admin_users():
    return render_template("admin/users.html", users=admin_controller.list_users(), error=None)


@app.route("/admin/users/create", methods=["POST"])
@login_required(role="admin")
def admin_create_user():
    try:
        admin_controller.create_user(
            request.form["username"],
            request.form["password"],
            request.form["role"]
        )
        flash("User created successfully.", "success")
        return redirect(url_for("admin_users"))
    except ValueError as exc:
        return render_template("admin/users.html", users=admin_controller.list_users(), error=str(exc))


@app.route("/admin/users/delete/<int:user_id>", methods=["POST"])
@login_required(role="admin")
def admin_delete_user(user_id):
    try:
        admin_controller.delete_user(user_id, session["user_id"])
        flash("User and related records deleted.", "success")
    except ValueError as exc:
        flash(str(exc), "error")
    return redirect(url_for("admin_users"))


@app.route("/admin/data")
@login_required(role="admin")
def admin_data():
    page = max(int(request.args.get("page", 1)), 1)
    records, pages = admin_controller.paginated_records(page)
    users = admin_controller.list_users()
    return render_template("admin/data.html", records=records, users=users, page=page, pages=pages, error=None)


@app.route("/admin/data/create", methods=["POST"])
@login_required(role="admin")
def admin_create_record():
    try:
        admin_controller.create_record(request.form)
        flash("Record created successfully.", "success")
    except ValueError as exc:
        flash(str(exc), "error")
    return redirect(url_for("admin_data"))


@app.route("/admin/data/delete/<int:record_id>", methods=["POST"])
@login_required(role="admin")
def admin_delete_record(record_id):
    try:
        admin_controller.delete_record(record_id)
        flash("Record deleted successfully.", "success")
    except ValueError as exc:
        flash(str(exc), "error")
    return redirect(url_for("admin_data"))


@app.route("/admin/bot-settings", methods=["GET", "POST"])
@login_required(role="admin")
def admin_bot_settings():
    if request.method == "POST":
        settings = admin_controller.update_bot_settings(
            request.form.get("bot_token", ""),
            request.form.get("chat_id", "")
        )
        flash("Telegram bot settings updated.", "success")
        return render_template("admin/bot_settings.html", settings=settings)

    settings = admin_controller.get_bot_settings(Config.BOT_TOKEN, Config.CHAT_ID)
    return render_template("admin/bot_settings.html", settings=settings)


@app.route("/api/admin/users")
@login_required(role="admin")
def api_admin_users():
    query = request.args.get("q", "").lower().strip()
    users = admin_controller.list_users()
    if query:
        users = [user for user in users if query in user.username.lower() or query in user.role.lower()]
    return jsonify([{
        "id": user.id,
        "username": user.username,
        "role": user.role,
        "created_at": user.created_at
    } for user in users])


@app.route("/webhook", methods=["POST"])
def telegram_webhook():
    if not request.is_json:
        return "Forbidden", 403
    update = telebot.types.Update.de_json(request.get_data().decode("utf-8"))
    telegram_bot.process_new_updates([update])
    return "", 200


@app.route("/user/dashboard")
@login_required()
def user_dashboard():
    records = user_controller.get_my_records(session["user_id"])
    return render_template("user/dashboard.html", records=records, error=None)


@app.route("/user/profile", methods=["GET", "POST"])
@login_required()
def user_profile():
    error = None
    success = None
    if request.method == "POST":
        try:
            user_controller.update_profile(session["user_id"], request.form)
            success = "Password updated successfully"
        except ValueError as exc:
            error = str(exc)
    profile = user_controller.get_profile(session["user_id"])
    record_count = user_controller.record_count(session["user_id"])
    return render_template("user/profile.html", profile=profile, record_count=record_count, error=error, success=success)


@app.errorhandler(403)
def forbidden(error):
    return render_template("errors/403.html"), 403


def configure_telegram_webhook():
    from config import WEBHOOK_URL

    webhook_url = WEBHOOK_URL.strip()
    if not webhook_url or "YOUR_" in webhook_url:
        logging.info("Telegram command webhook skipped: WEBHOOK_URL is not configured.")
        return
    try:
        telegram_bot.remove_webhook()
        telegram_bot.set_webhook(url=webhook_url)
        logging.info("Telegram command webhook configured: %s", webhook_url)
    except Exception as error:
        logging.error("Telegram command webhook setup failed: %s", error)


if __name__ == "__main__":
    configure_telegram_webhook()
    app.run(debug=Config.DEBUG)
