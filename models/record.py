from datetime import datetime


class Record:
    def __init__(self, id, user_id, name, salary, department, worked_since, created_at=None):
        self.id = int(id)
        self.user_id = int(user_id)
        self.name = self._require_text(name, "Name")
        self.salary = self._validate_salary(salary)
        self.department = self._require_text(department, "Department")
        self.worked_since = self._validate_year(worked_since)
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _require_text(self, value, field):
        value = str(value).strip()
        if not value:
            raise ValueError(f"{field} cannot be empty")
        return value

    def _validate_salary(self, value):
        value = int(value)
        if not 1 <= value <= 50000000:
            raise ValueError("Salary must be between 1 and 50000000")
        return value

    def _validate_year(self, value):
        value = int(value)
        if not 1900 <= value <= 2026:
            raise ValueError("Worked since must be between 1900 and 2026")
        return value

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "salary": self.salary,
            "department": self.department,
            "worked_since": self.worked_since,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            user_id=data["user_id"],
            name=data["name"],
            salary=data["salary"],
            department=data["department"],
            worked_since=data["worked_since"],
            created_at=data.get("created_at")
        )
