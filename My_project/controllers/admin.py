class AdminController:
    def __init__(self, db_service, bot_service):
        self.db = db_service
        self.bot = bot_service

    def dashboard_stats(self):
        users = self.db.list_users()
        records = self.db.list_records()
        recent_users = sorted(users, key=lambda user: user.created_at, reverse=True)[:5]
        return {
            "total_users": len(users),
            "total_records": len(records),
            "recent_users": recent_users
        }

    def list_users(self):
        return self.db.list_users()

    def create_user(self, username, password, role):
        user = self.db.add_user(username, password, role)
        self.bot.notify_admin_action("created user", f"username={user.username}, role={user.role}")
        return user

    def delete_user(self, user_id, current_admin_id):
        if int(user_id) == int(current_admin_id):
            raise ValueError("Admin cannot delete themselves")
        self.db.delete_user(user_id)
        self.bot.notify_admin_action("deleted user", f"user_id={user_id}")

    def create_record(self, form_data):
        record = self.db.add_record(
            user_id=form_data.get("user_id"),
            name=form_data.get("name", ""),
            salary=form_data.get("salary", 0),
            department=form_data.get("department", ""),
            worked_since=form_data.get("worked_since", 0)
        )
        self.bot.notify_admin_action("created record", f"record_id={record.id}, user_id={record.user_id}")
        return record

    def delete_record(self, record_id):
        self.db.delete_record(record_id)
        self.bot.notify_admin_action("deleted record", f"record_id={record_id}")

    def list_all_records(self):
        return self.db.list_records()

    def paginated_records(self, page, per_page=10):
        records = self.list_all_records()
        total = len(records)
        start = (page - 1) * per_page
        end = start + per_page
        pages = max((total + per_page - 1) // per_page, 1)
        return records[start:end], pages

    def get_bot_settings(self, default_token="", default_chat_id=""):
        return self.db.get_bot_settings(default_token, default_chat_id)

    def update_bot_settings(self, bot_token, chat_id):
        settings = self.db.save_bot_settings(bot_token, chat_id)
        self.bot.update_settings(settings["bot_token"], settings["chat_id"])
        self.bot.notify_admin_action("updated bot settings", "Telegram bot token/chat id changed")
        return settings
