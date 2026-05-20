import os


class Config:
    SECRET_KEY = "change-this-secret-key-before-production"
    DB_PATH = os.path.dirname(__file__)
    BOT_TOKEN = "8806949111:AAHU5LlsBVVSpopOJllj78QXupBEr4oViLM"
    CHAT_ID = "1228859868"
    DEBUG = True


# Backward-compatible constants for the Assignment 4 bot package.
BOT_TOKEN = Config.BOT_TOKEN
WEBHOOK_URL = "https://inconstant-jacinta-syllabically.ngrok-free.dev/webhook"