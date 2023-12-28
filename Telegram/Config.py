import telebot
import os

from dotenv import load_dotenv
load_dotenv()

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
bot = telebot.TeleBot(os.getenv("TELEGRAM_BOT_TOKEN"), use_class_middlewares=True)


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance