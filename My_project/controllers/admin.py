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

    def list_all_records(self):
        return self.db.list_records()

    def paginated_records(self, page, per_page=10):
        records = self.list_all_records()
        total = len(records)
        start = (page - 1) * per_page
        end = start + per_page
        pages = max((total + per_page - 1) // per_page, 1)
        return records[start:end], pages
