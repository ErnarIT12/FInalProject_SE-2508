import json
import os

from models.record import Record
from models.user import User


class DatabaseService:
    def __init__(self, db_path):
        self.db_path = db_path
        self.users_file = os.path.join(db_path, "users.json")
        self.records_file = os.path.join(db_path, "records.json")
        self.seed()

    def seed(self):
        if not os.path.exists(self.users_file):
            users = [
                User(1, "admin", User.hash_password("admin123"), "admin").to_dict(),
                User(2, "testuser", User.hash_password("user123"), "user").to_dict()
            ]
            self._write_json(self.users_file, users)
        if not os.path.exists(self.records_file):
            records = [
                Record(1, 2, "Aruzhan Karimova", 450000, "Finance", 2022).to_dict(),
                Record(2, 2, "Nursultan Bekov", 800000, "IT", 2020).to_dict(),
                Record(3, 1, "Madi Tulegen", 1000000, "Management", 2019).to_dict()
            ]
            self._write_json(self.records_file, records)

    def _read_json(self, path):
        if not os.path.exists(path):
            return []
        with open(path, "r", encoding="utf-8") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []

    def _write_json(self, path, data):
        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def list_users(self):
        return [User.from_dict(item) for item in self._read_json(self.users_file)]

    def save_users(self, users):
        self._write_json(self.users_file, [user.to_dict() for user in users])

    def get_user_by_id(self, user_id):
        for user in self.list_users():
            if user.id == int(user_id):
                return user
        return None

    def get_user_by_username(self, username):
        username = username.lower().strip()
        for user in self.list_users():
            if user.username.lower() == username:
                return user
        return None

    def add_user(self, username, password, role="user"):
        if self.get_user_by_username(username):
            raise ValueError("Username already exists")
        users = self.list_users()
        next_id = max((user.id for user in users), default=0) + 1
        user = User(next_id, username.strip(), User.hash_password(password), role)
        users.append(user)
        self.save_users(users)
        return user

    def delete_user(self, user_id):
        user_id = int(user_id)
        users = [user for user in self.list_users() if user.id != user_id]
        self.save_users(users)
        records = [record for record in self.list_records() if record.user_id != user_id]
        self.save_records(records)

    def update_user(self, user):
        users = self.list_users()
        for index, current in enumerate(users):
            if current.id == user.id:
                users[index] = user
                self.save_users(users)
                return user
        raise ValueError("User not found")

    def list_records(self):
        return [Record.from_dict(item) for item in self._read_json(self.records_file)]

    def save_records(self, records):
        self._write_json(self.records_file, [record.to_dict() for record in records])

    def add_record(self, user_id, name, salary, department, worked_since):
        records = self.list_records()
        next_id = max((record.id for record in records), default=0) + 1
        record = Record(next_id, user_id, name, salary, department, worked_since)
        records.append(record)
        self.save_records(records)
        return record

    def get_records_by_user(self, user_id):
        return [record for record in self.list_records() if record.user_id == int(user_id)]

    def count_records_by_user(self, user_id):
        return len(self.get_records_by_user(user_id))
