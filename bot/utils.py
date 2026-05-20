import re
from functools import wraps

def log_command(func):
    @wraps(func)
    def wrapper(message, *args, **kwargs):
        command_name = message.text.split()[0] if message.text else "unknown"
        print(f"Пользователь [{message.from_user.id}] вызвал команду [{command_name}]")
        return func(message, *args, **kwargs)
    return wrapper

def fact_generator():
    facts = [
        "Первый в мире программист — женщина, Ада Лавлейс.",
        "Python назван в честь британского шоу 'Летающий цирк Монти Пайтона', а не змеи.",
        "Первый компьютерный 'баг' (жук) был реальным мотыльком, застрявшим в реле компьютера Mark II."
    ]
    while True: # Бесконечный цикл, чтобы факты не кончались
        for fact in facts:
            yield fact

fact_gen = fact_generator()

def is_valid_date(date_text):
    pattern = r"^(19|20)\d{2}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$"
    return bool(re.match(pattern, date_text))

def translate_to_mandarin(text):
    dictionary = {
        "hello": "你好",
        "hi": "你好",
        "goodbye": "再见",
        "thanks": "谢谢",
        "thank you": "谢谢",
        "employee": "员工",
        "employees": "员工",
        "salary": "工资",
        "department": "部门",
        "work": "工作",
        "year": "年",
        "date": "日期",
        "help": "帮助",
        "student": "学生",
        "students": "学生",
        "book": "书",
        "books": "书",
        "car": "汽车",
        "cars": "汽车",
        "python": "Python 编程语言"
    }
    normalized = text.strip().lower()
    if normalized in dictionary:
        return dictionary[normalized]

    words = re.findall(r"\w+|[^\w\s]", normalized, re.UNICODE)
    translated = [dictionary.get(word, word) for word in words]
    return " ".join(translated)
