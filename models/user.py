import hashlib
from datetime import datetime


class User:
    VALID_ROLES = {"admin", "user"}

    def __init__(self, id, username, password_hash, role="user", created_at=None):
        if role not in self.VALID_ROLES:
            raise ValueError("Role must be admin or user")
        self.id = int(id)
        self.username = username
        self.password_hash = password_hash
        self.role = role
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def check_password(self, password):
        return self.password_hash == self.hash_password(password)

    def set_password(self, password):
        self.password_hash = self.hash_password(password)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password_hash": self.password_hash,
            "role": self.role,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            username=data["username"],
            password_hash=data["password_hash"],
            role=data["role"],
            created_at=data["created_at"]
        )
