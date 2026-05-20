class UserController:
    def __init__(self, db_service):
        self.db = db_service

    def get_profile(self, user_id):
        user = self.db.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        return user

    def update_profile(self, user_id, data):
        user = self.get_profile(user_id)
        password = data.get("password", "")
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters")
        user.set_password(password)
        self.db.update_user(user)
        return user

    def get_my_records(self, user_id):
        return self.db.get_records_by_user(user_id)

    def create_record(self, user_id, form_data):
        return self.db.add_record(
            user_id=user_id,
            name=form_data.get("name", ""),
            salary=form_data.get("salary", 0),
            department=form_data.get("department", ""),
            worked_since=form_data.get("worked_since", 0)
        )

    def record_count(self, user_id):
        return self.db.count_records_by_user(user_id)
