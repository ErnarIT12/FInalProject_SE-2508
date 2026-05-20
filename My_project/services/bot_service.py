import logging
import asyncio
import inspect
from datetime import datetime
from html import escape


class BotService:
    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id

    def update_settings(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id

    def _send_message(self, text, parse_mode="HTML"):
        if not self.token or not self.chat_id or "YOUR_" in self.token or "YOUR_" in self.chat_id:
            logging.info("Telegram notification skipped: bot token or chat id is not configured.")
            return False
        try:
            self._send_with_python_telegram_bot(text, parse_mode)
            return True
        except ModuleNotFoundError:
            return self._send_with_pytelegrambotapi(text, parse_mode)
        except Exception as error:
            logging.error("Telegram notification failed: %s", error)
            return False

    def _send_with_python_telegram_bot(self, text, parse_mode):
        from telegram import Bot
        bot = Bot(token=self.token)
        result = bot.send_message(chat_id=self.chat_id, text=text, parse_mode=parse_mode)
        if inspect.isawaitable(result):
            asyncio.run(result)

    def _send_with_pytelegrambotapi(self, text, parse_mode):
        try:
            import telebot
            bot = telebot.TeleBot(self.token)
            bot.send_message(self.chat_id, text, parse_mode=parse_mode)
            return True
        except Exception as error:
            logging.error("Telegram notification failed: %s", error)
            return False

    def _timestamp(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def notify_new_user(self, username):
        message = (
            "<b>Admin Panel Alert</b>\n"
            "<b>Event:</b> New user registration\n\n"
            f"<b>Username:</b> <code>{escape(username)}</code>\n"
            f"<b>Created at:</b> <code>{self._timestamp()}</code>\n"
            "<b>Source:</b> <code>/register</code>"
        )
        return self._send_message(message)

    def notify_admin_action(self, action, detail):
        message = (
            "<b>Admin Panel Alert</b>\n"
            "<b>Event:</b> Admin action\n\n"
            f"<b>Action:</b> <code>{escape(action)}</code>\n"
            f"<b>Detail:</b> <code>{escape(detail)}</code>\n"
            f"<b>Time:</b> <code>{self._timestamp()}</code>"
        )
        return self._send_message(message)
