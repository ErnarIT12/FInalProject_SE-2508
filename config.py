import os
from dotenv import load_dotenv

load_dotenv()  


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-fallback-key")
    DB_PATH = os.path.dirname(__file__)
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    CHAT_ID = os.environ.get("CHAT_ID", "")
    DEBUG = os.environ.get("DEBUG", "False").lower() == "true"
    WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "")


# Backward-compatible constants
BOT_TOKEN = Config.BOT_TOKEN
WEBHOOK_URL = Config.WEBHOOK_URL