import asyncio
from aiogram import types
import logging
import Game
from settings import Settings

logging.basicConfig(level=logging.INFO)
QUIZ_MESSAGE = 'Try to guess another quiz.'


@Settings.DISPATCHER.message_handler(content_types=types.ContentType.TEXT, commands=["test"])
async def cmd_test(message: types.Message):
    message = await Settings.BOT.send_message(chat_id=message.from_user.id, text='Try to guess')
    print(message['message_id'])
    await message.edit_text(text='1')
    await message.edit_media()


@Settings.DISPATCHER.message_handler(content_types=types.ContentType.TEXT, commands=["game"])
async def cmd_game(message: types.Message):
    factory = Game.QuizFactory()
    quiz = factory.createPhotoQuiz(message, False)
    await quiz.startPhotoQuiz()


@Settings.DISPATCHER.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer("Hello! This is telegram quiz bot. You will need to guess a film by an image.\n"
                         "\\game -> start quiz.\n\\statistic -> show player statistic.")


@Settings.DISPATCHER.callback_query_handler(lambda c: c.data == 'true')
async def process_button_true(callback_query: types.CallbackQuery):
    id = callback_query.from_user.id
    await callback_query.message.delete()
    mes = await Settings.BOT.send_message(chat_id=id, text='+2 points.\n' + QUIZ_MESSAGE)
    factory = Game.QuizFactory()
    quiz = factory.createPhotoQuiz(mes, id, canBeEdited=True)
    await quiz.startPhotoQuiz()


@Settings.DISPATCHER.callback_query_handler(lambda c: c.data == 'false')
async def process_button_false(callback_query: types.CallbackQuery):
    id = callback_query.from_user.id
    await callback_query.message.delete()
    mes = await Settings.BOT.send_message(chat_id=id, text='-3 points.\n' + QUIZ_MESSAGE)
    factory = Game.QuizFactory()
    quiz = factory.createPhotoQuiz(mes, id, canBeEdited=True)
    await quiz.startPhotoQuiz()


async def main():
    await Settings.DISPATCHER.start_polling(Settings.BOT)


if __name__ == '__main__':
    asyncio.run(main())
