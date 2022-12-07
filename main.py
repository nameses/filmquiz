import asyncio

from aiogram import types
import logging
# import requests
# import json
# import constants
import Game
from settings import Settings
import MoviesHelper

logging.basicConfig(level=logging.INFO)


@Settings.DISPATCHER.message_handler(content_types=types.ContentType.TEXT, commands=["test"])
async def cmd_test(message=None):
    message = await Settings.BOT.send_message(chat_id=message.from_user.id, text='Try to guess')
    print(message['message_id'])
    await message.edit_text(text='1')
    await message.edit_media()


@Settings.DISPATCHER.message_handler(content_types=types.ContentType.TEXT, commands=["game"])
async def cmd_game(message):
    factory = Game.QuizFactory()
    quiz = factory.createPhotoQuiz(message)
    await quiz.startPhotoQuiz()


@Settings.DISPATCHER.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer("Hello! This is telegram quiz bot. You will need to guess a film by an image.\n"
                         "\\game -> start quiz.\n\\statistic -> show player statistic.")


QUIZ_MESSAGE = 'Try to guess another quiz.'


@Settings.DISPATCHER.callback_query_handler(lambda c: c.data == 'true')
async def process_button_true(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(text=('+2 points.\n' + QUIZ_MESSAGE))
    await cmd_game(callback_query.message)


@Settings.DISPATCHER.callback_query_handler(lambda c: c.data == 'false')
async def process_button_false(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(text='-3 points.\n' + QUIZ_MESSAGE)
    await cmd_game(callback_query.message)


async def main():
    # moviesHelper = MoviesHelper()
    await Settings.DISPATCHER.start_polling(Settings.BOT)


if __name__ == '__main__':
    asyncio.run(main())
