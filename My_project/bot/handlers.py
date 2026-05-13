from bot import bot
from bot.utils import log_command, fact_gen, is_valid_date, translate_to_mandarin
from bot.models import Employee, Person
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_FILE = os.path.join(BASE_DIR, "employees.json")

def load_employees_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []

def save_employees_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

@bot.message_handler(commands=['start'])
@log_command
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот для управления сотрудниками. Жми /help для списка команд.")

@bot.message_handler(commands=['help'])
@log_command
def send_help(message):
    help_text = (
        "/start - Приветствие\n"
        "/help - Список команд\n"
        "/echo [текст] - Повтор текста\n"
        "/save [Имя] [ЗП] [Отдел] [Год] - Сохранить сотрудника\n"
        "/list - Список сотрудников\n"
        "/fact - Интересный IT-факт\n"
        "/validate [YYYY-MM-DD] - Проверка даты\n"
        "/about - О боте (демо ООП)\n"
        "/custom [текст] - Перевод текста на Mandarin Chinese"
    )
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['echo'])
@log_command
def echo_text(message):
    text = message.text.replace("/echo", "").strip()
    if text:
        bot.reply_to(message, text)
    else:
        bot.reply_to(message, "Напиши текст после команды, например: /echo Привет")

@bot.message_handler(commands=['save'])
@log_command
def save_employee(message):
    args = message.text.split()[1:]
    if len(args) != 4:
        bot.reply_to(message, "Формат: /save Имя Зарплата Отдел Год")
        return
    
    try:
        name = args[0]
        salary = int(args[1])
        department = args[2]
        year = int(args[3])
        
        emp = Employee(name, salary, department, year)
        
        employees = load_employees_data()
        new_id = max((e["id"] for e in employees), default=0) + 1
        user_id = message.from_user.id
        
        employees.append(emp.to_dict(new_id, user_id))
        save_employees_data(employees)
        bot.reply_to(message, f"Сотрудник {emp.name} успешно сохранен!")
    except ValueError as e:
        bot.reply_to(message, f"Ошибка данных: {e}")

@bot.message_handler(commands=['list'])
@log_command
def list_employees(message):
    employees = load_employees_data()
    user_id = message.from_user.id
    user_employees = [e for e in employees if e.get("user_id") == user_id]

    if not user_employees:
        bot.reply_to(message, "Список сотрудников пуст.")
        return
    
    response = "Ваши сотрудники:\n"
    for e in user_employees:
        emp_obj = Employee(e["name"], e["salary"], e["department"], e["worked_since"])
        response += f"ID: {e['id']} | {emp_obj}\n"
    
    bot.reply_to(message, response)

@bot.message_handler(commands=['fact'])
@log_command
def send_fact(message):
    # Берем следующий элемент из генератора
    bot.reply_to(message, next(fact_gen))

@bot.message_handler(commands=['validate'])
@log_command
def validate_input(message):
    args = message.text.split()[1:]
    if not args:
        bot.reply_to(message, "Введи дату для проверки: /validate 2026-05-13")
        return
    
    date_str = args[0]
    if is_valid_date(date_str):
        bot.reply_to(message, f"✅ Дата {date_str} имеет корректный формат YYYY-MM-DD.")
    else:
        bot.reply_to(message, f"❌ Неверный формат. Ожидается YYYY-MM-DD.")

@bot.message_handler(commands=['about'])
@log_command
def about_bot(message):
    creator = Person("Student Developer")
    demo_employee = Employee("Demo Employee", 100000, "IT", 2023)
    bot.reply_to(
        message,
        f"Бот для управления сотрудниками.\n"
        f"Разработчик: {creator}\n"
        f"Пример класса Employee: {demo_employee.short_info()} | {demo_employee}"
    )

@bot.message_handler(commands=['custom'])
@log_command
def custom_translate(message):
    text = message.text.replace("/custom", "", 1).strip()
    if not text:
        bot.reply_to(message, "Напиши текст после команды, например: /custom hello")
        return

    bot.reply_to(message, f"Mandarin Chinese: {translate_to_mandarin(text)}")
