import asyncio

from aiogram import types
import logging
# import requests
# import json
# import constants
import Game
from settings import Settings

logging.basicConfig(level=logging.INFO)


@Settings.DISPATCHER.message_handler(content_types=types.ContentType.TEXT, commands=["game"])
async def cmd_game(message: types.Message):
    await Game.QuizFactory.createPhotoQuiz(message).startPhotoQuiz()


@Settings.DISPATCHER.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer("Hello! This is telegram quiz bot. You will need to guess a film by an image.\n"
                         "\\game -> start quiz.\n\\statistic -> show player statistic.")


async def main():
    await Settings.DISPATCHER.start_polling(Settings.BOT)


if __name__ == '__main__':
    asyncio.run(main())
