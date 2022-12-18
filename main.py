from aiogram import types, executor
import logging
import Quiz
from TelegramBot import TelegramBot
from settings import Settings
from MainKeyboard import MainKeyboard
from Statistic import Statistic

logging.basicConfig(level=logging.INFO)


def main():
    telBot = TelegramBot()
    telBot.start_polling()


if __name__ == '__main__':
    main()
