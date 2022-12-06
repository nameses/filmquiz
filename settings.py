from aiogram import Bot, Dispatcher

import constants


class Settings:
    BOT = Bot(token=constants.TG_TOKEN)
    DISPATCHER = Dispatcher(bot=BOT)
