import telebot
import config

# Инициализируем бота
bot = telebot.TeleBot(config.BOT_TOKEN)

# Импортируем handlers, чтобы они зарегистрировались при запуске
from bot import handlers