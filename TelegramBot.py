from aiogram import types, executor
import Quiz
from MainKeyboard import MainKeyboard
from Statistic import Statistic
from settings import Settings

STARTING_QUIZ_MESSAGE = 'Try to guess.'
QUIZ_MESSAGE = 'Try to guess another quiz.'
TRUE_MESSAGE = '+2 points.\n' + QUIZ_MESSAGE
FALSE_MESSAGE = '-3 points.\n' + QUIZ_MESSAGE


class TelegramBot(object):
    def __init__(self):
        self.register_handlers()

    def register_handlers(self):
        dispatcher_handler = Settings.DISPATCHER.register_message_handler
        dispatcher_callback = Settings.DISPATCHER.register_callback_query_handler
        dispatcher_handler(self.cmd_game_photo, commands=['game'], state="*")
        dispatcher_handler(self.cmd_game_photo,
                           lambda mes: mes.text == 'Photo Quiz',
                           state="*")
        dispatcher_handler(self.cmd_game_descr, commands=['game'], state="*")
        dispatcher_handler(self.cmd_game_descr,
                           lambda mes: mes.text == 'Description Quiz',
                           state="*")
        dispatcher_handler(self.cmd_start, commands=['start'], state="*")
        dispatcher_callback(self.process_description_button_true,
                            lambda mes: mes.data == 'DescrQuizTrue')
        dispatcher_callback(self.process_description_button_false,
                            lambda mes: mes.data == 'DescrQuizFalse')
        dispatcher_callback(self.process_photo_button_true,
                            lambda mes: mes.data == 'PhotoQuizTrue')
        dispatcher_callback(self.process_photo_button_false,
                            lambda mes: mes.data == 'PhotoQuizFalse')
        dispatcher_handler(self.statistic_command, commands=['statistic'], state="*")
        dispatcher_handler(self.statistic_command,
                           lambda mes: mes.text == 'Statistic',
                           state="*")

    def start_polling(self):
        executor.start_polling(Settings.DISPATCHER, skip_updates=True)

    # @Settings.DISPATCHER.message_handler(content_types=types.ContentType.TEXT, commands=["game"])
    # @Settings.DISPATCHER.message_handler(lambda mes: mes.text == 'Photo Quiz')
    async def cmd_game_photo(self, message: types.Message):
        quiz = Quiz.QuizFactory.create_photo_quiz(message, message.from_user.id, STARTING_QUIZ_MESSAGE)

        statistic = Statistic(message.from_user.id)
        points = statistic.photo_quiz_points()
        await message.answer(text=f'You have <b>{points}</b> points already.\n',
                             parse_mode='HTML')

        if statistic.get_pq_ids():
            await quiz.resend_quiz()
        else:
            await quiz.start_quiz()

    # @Settings.DISPATCHER.message_handler(content_types=types.ContentType.TEXT, commands=["game"])
    # @Settings.DISPATCHER.message_handler(lambda mes: mes.text == 'Description Quiz')
    async def cmd_game_descr(self, message: types.Message):
        quiz = Quiz.QuizFactory.create_descr_quiz(message, message.from_user.id, STARTING_QUIZ_MESSAGE)

        statistic = Statistic(message.from_user.id)
        points = statistic.description_quiz_points()
        await message.answer(text=f'You have <b>{points}</b> points already.\n',
                             parse_mode='HTML')

        if statistic.get_dq_ids():
            await quiz.resend_quiz()
        else:
            await quiz.start_quiz()

    # @Settings.DISPATCHER.message_handler(commands=["start"])
    async def cmd_start(self, message: types.Message):
        await message.answer("Hello! This is telegram quiz bot. "
                             "You will need to guess a film by an image or a description.",
                             reply_markup=MainKeyboard.get_keyboard())

    # @Settings.DISPATCHER.callback_query_handler(lambda c: c.data == 'PhotoQuizTrue')
    async def process_photo_button_true(self, callback_query: types.CallbackQuery):
        id = callback_query.from_user.id
        await callback_query.message.delete()
        quiz = Quiz.QuizFactory.create_photo_quiz(None, id, TRUE_MESSAGE)

        statistic = Statistic(id)
        statistic.updating_photo_points(True)

        await quiz.start_quiz()

    # @Settings.DISPATCHER.callback_query_handler(lambda c: c.data == 'PhotoQuizFalse')
    async def process_photo_button_false(self, callback_query: types.CallbackQuery):
        id = callback_query.from_user.id
        await callback_query.message.delete()
        quiz = Quiz.QuizFactory.create_photo_quiz(None, id, FALSE_MESSAGE)

        statistic = Statistic(id)
        statistic.updating_photo_points(False)

        await quiz.start_quiz()

    # @Settings.DISPATCHER.callback_query_handler(lambda c: c.data == 'DescrQuizTrue')
    async def process_description_button_true(self, callback_query: types.CallbackQuery):
        id = callback_query.from_user.id
        await callback_query.message.delete()
        quiz = Quiz.QuizFactory.create_descr_quiz(None, id, TRUE_MESSAGE)

        statistic = Statistic(id)
        statistic.updating_description_points(True)

        await quiz.start_quiz()

    # @Settings.DISPATCHER.callback_query_handler(lambda c: c.data == 'DescrQuizFalse')
    async def process_description_button_false(self, callback_query: types.CallbackQuery):
        id = callback_query.from_user.id
        await callback_query.message.delete()
        quiz = Quiz.QuizFactory.create_descr_quiz(None, id, FALSE_MESSAGE)

        statistic = Statistic(id)
        statistic.updating_description_points(False)

        await quiz.start_quiz()

    # @Settings.DISPATCHER.message_handler(commands=['statistic'])
    # @Settings.DISPATCHER.message_handler(lambda mes: mes.text == 'Statistic')
    async def statistic_command(self, message: types.Message):
        id = message.from_user.id

        statistic = Statistic(id)

        await message.answer(text=f'You have <b>{statistic.photo_quiz_points()}</b> Photo Quiz points and '
                                  f'<b>{statistic.description_quiz_points()}</b> Description Quiz points.\n',
                             parse_mode='HTML')

    # @Settings.DISPATCHER.message_handler()
    async def default(self, message: types.Message):
        await message.answer(text=message.text.title())
