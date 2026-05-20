class Person:
    def __init__(self, name):
        if not str(name).strip():
            raise ValueError("Имя не может быть пустым")
        self.name = name

    def __str__(self):
        return f"Person: {self.name}"

    def short_info(self):
        return f"{self.name}"

class Employee(Person):
    def __init__(self, name, salary, department, worked_since):
        super().__init__(name)
        self.__salary = 0
        self.salary = salary
        if not str(department).strip():
            raise ValueError("Отдел не может быть пустым")
        if not 1900 <= worked_since <= 2026:
            raise ValueError("Год начала работы должен быть между 1900 и 2026")
        self.department = department
        self.worked_since = worked_since

    @property
    def salary(self):
        return self.__salary

    @salary.setter
    def salary(self, value):
        if not 1 <= value <= 50000000:
            raise ValueError("Зарплата должна быть от 1 до 50000000")
        self.__salary = value

    def to_dict(self, employee_id, user_id):
        return {
            "id": employee_id,
            "user_id": user_id,
            "name": self.name,
            "salary": self.salary,
            "department": self.department,
            "worked_since": self.worked_since
        }

    def __str__(self):
        return f"Employee: {self.name} | Department: {self.department} | Salary: {self.salary} | Since: {self.worked_since}"
