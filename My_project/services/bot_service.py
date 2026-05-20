import logging
import asyncio
import inspect


class BotService:
    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id

    def _send_message(self, text):
        if not self.token or not self.chat_id or "YOUR_" in self.token or "YOUR_" in self.chat_id:
            logging.info("Telegram notification skipped: bot token or chat id is not configured.")
            return False
        try:
            self._send_with_python_telegram_bot(text)
            return True
        except ModuleNotFoundError:
            return self._send_with_pytelegrambotapi(text)
        except Exception as error:
            logging.error("Telegram notification failed: %s", error)
            return False

    def _send_with_python_telegram_bot(self, text):
        from telegram import Bot
        bot = Bot(token=self.token)
        result = bot.send_message(chat_id=self.chat_id, text=text)
        if inspect.isawaitable(result):
            asyncio.run(result)

    def _send_with_pytelegrambotapi(self, text):
        try:
            import telebot
            bot = telebot.TeleBot(self.token)
            bot.send_message(self.chat_id, text)
            return True
        except Exception as error:
            logging.error("Telegram notification failed: %s", error)
            return False

    def notify_new_user(self, username):
        return self._send_message(f"New user registered: {username}")

    def notify_admin_action(self, action, detail):
        return self._send_message(f"Admin action: {action}. Detail: {detail}")
