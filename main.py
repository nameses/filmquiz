import asyncio
from aiogram import types
import logging
import Quiz
from settings import Settings
from MainKeyboard import MainKeyboard

logging.basicConfig(level=logging.INFO)
QUIZ_MESSAGE = 'Try to guess another quiz.'


@Settings.DISPATCHER.message_handler(content_types=types.ContentType.TEXT, commands=["game"])
@Settings.DISPATCHER.message_handler(lambda mes: mes.text == 'Photo Quiz')
async def cmdGamePhoto(message: types.Message):
    factory = Quiz.QuizFactory()
    quiz = factory.createPhotoQuiz(message, False)
    await quiz.startQuiz()


@Settings.DISPATCHER.message_handler(content_types=types.ContentType.TEXT, commands=["game"])
@Settings.DISPATCHER.message_handler(lambda mes: mes.text == 'Description Quiz')
async def cmdGameDescr(message: types.Message):
    factory = Quiz.QuizFactory()
    quiz = factory.createDescrQuiz(message, False)
    await quiz.startQuiz()


@Settings.DISPATCHER.message_handler(commands=["start"])
async def cmdStart(message: types.Message):
    await message.answer("Hello! This is telegram quiz bot. You will need to guess a film by an image",
                         reply_markup=MainKeyboard.getKeyboard())


@Settings.DISPATCHER.callback_query_handler(lambda c: c.data == 'true')
async def processButtonTrue(callback_query: types.CallbackQuery):
    id = callback_query.from_user.id
    await callback_query.message.delete()
    mes = await Settings.BOT.send_message(chat_id=id, text='+2 points.\n' + QUIZ_MESSAGE)
    factory = Quiz.QuizFactory()
    quiz = factory.createPhotoQuiz(mes, id, canBeEdited=True)
    await quiz.startQuiz()


@Settings.DISPATCHER.callback_query_handler(lambda c: c.data == 'false')
async def processButtonFalse(callback_query: types.CallbackQuery):
    id = callback_query.from_user.id
    await callback_query.message.delete()
    mes = await Settings.BOT.send_message(chat_id=id, text='-3 points.\n' + QUIZ_MESSAGE)
    factory = Quiz.QuizFactory()
    quiz = factory.createPhotoQuiz(mes, id, canBeEdited=True)
    await quiz.startQuiz()


@Settings.DISPATCHER.message_handler()
async def default(message: types.Message):
    await message.answer(text=message.text.title())

async def main():
    await Settings.DISPATCHER.start_polling(Settings.BOT)


if __name__ == '__main__':
    asyncio.run(main())
