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
    factory = Game.QuizFactory()
    quiz = factory.createPhotoQuiz(message)
    await quiz.startPhotoQuiz()


@Settings.DISPATCHER.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer("Hello! This is telegram quiz bot. You will need to guess a film by an image.\n"
                         "\\game -> start quiz.\n\\statistic -> show player statistic.")


@Settings.DISPATCHER.callback_query_handler(func=lambda c: c.data == 'var1')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Нажата первая кнопка!')


async def main():
    await Settings.DISPATCHER.start_polling(Settings.BOT)


if __name__ == '__main__':
    asyncio.run(main())
