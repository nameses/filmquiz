import asyncio
from aiogram import types
import logging
import Quiz
from settings import Settings
from MainKeyboard import MainKeyboard

logging.basicConfig(level=logging.INFO)

STARTING_QUIZ_MESSAGE = 'Try to guess.'
QUIZ_MESSAGE = 'Try to guess another quiz.'
TRUE_MESSAGE = '+2 points.\n' + QUIZ_MESSAGE
FALSE_MESSAGE = '-3 points.\n' + QUIZ_MESSAGE


@Settings.DISPATCHER.message_handler(content_types=types.ContentType.TEXT, commands=["game"])
@Settings.DISPATCHER.message_handler(lambda mes: mes.text == 'Photo Quiz')
async def cmd_game_photo(message: types.Message):
    factory = Quiz.QuizFactory()
    quiz = factory.create_photo_quiz(message, message.from_user.id, STARTING_QUIZ_MESSAGE)
    await quiz.start_quiz()


@Settings.DISPATCHER.message_handler(content_types=types.ContentType.TEXT, commands=["game"])
@Settings.DISPATCHER.message_handler(lambda mes: mes.text == 'Description Quiz')
async def cmd_game_descr(message: types.Message):
    factory = Quiz.QuizFactory()
    quiz = factory.create_descr_quiz(message, message.from_user.id, STARTING_QUIZ_MESSAGE)
    await quiz.start_quiz()


@Settings.DISPATCHER.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer("Hello! This is telegram quiz bot. You will need to guess a film by an image",
                         reply_markup=MainKeyboard.getKeyboard())


@Settings.DISPATCHER.callback_query_handler(lambda c: c.data == 'PhotoQuizTrue')
async def process_photo_button_true(callback_query: types.CallbackQuery):
    id = callback_query.from_user.id
    await callback_query.message.delete()
    # mes = await Settings.BOT.send_message(chat_id=id, text=TRUE_MESSAGE)
    # await mes.delete()
    factory = Quiz.QuizFactory()
    quiz = factory.create_photo_quiz(None, id, TRUE_MESSAGE)
    await quiz.start_quiz()


@Settings.DISPATCHER.callback_query_handler(lambda c: c.data == 'PhotoQuizFalse')
async def process_photo_button_false(callback_query: types.CallbackQuery):
    id = callback_query.from_user.id
    await callback_query.message.delete()
    # mes = await Settings.BOT.send_message(chat_id=id, text=FALSE_MESSAGE)
    # await mes.delete()
    factory = Quiz.QuizFactory()
    quiz = factory.create_photo_quiz(None, id, FALSE_MESSAGE)
    await quiz.start_quiz()


@Settings.DISPATCHER.callback_query_handler(lambda c: c.data == 'DescrQuizTrue')
async def process_description_button_true(callback_query: types.CallbackQuery):
    id = callback_query.from_user.id
    await callback_query.message.delete()
    # mes = await Settings.BOT.send_message(chat_id=id, text=TRUE_MESSAGE)
    # await mes.delete()
    factory = Quiz.QuizFactory()
    quiz = factory.create_descr_quiz(None, id, TRUE_MESSAGE)
    await quiz.start_quiz()


@Settings.DISPATCHER.callback_query_handler(lambda c: c.data == 'DescrQuizFalse')
async def process_description_button_false(callback_query: types.CallbackQuery):
    id = callback_query.from_user.id
    await callback_query.message.delete()
    # mes = await Settings.BOT.send_message(chat_id=id, text=FALSE_MESSAGE)
    # await mes.delete()
    factory = Quiz.QuizFactory()
    quiz = factory.create_descr_quiz(None, id, FALSE_MESSAGE)
    await quiz.start_quiz()


@Settings.DISPATCHER.message_handler()
async def default(message: types.Message):
    await message.answer(text=message.text.title())


async def main():
    await Settings.DISPATCHER.start_polling(Settings.BOT)


if __name__ == '__main__':
    asyncio.run(main())
