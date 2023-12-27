import telebot
import os

from dotenv import load_dotenv
load_dotenv()

bot = telebot.TeleBot(os.getenv("TELEGRAM_BOT_TOKEN"))