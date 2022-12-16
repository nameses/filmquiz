import random
from random import randint
from aiogram import types
from aiogram.types import InputFile, InlineKeyboardButton, InlineKeyboardMarkup
import tmdbsimple as tmdb
from MoviesFinder import MoviesFinder
import constants
from settings import Settings

tmdb.REQUESTS_TIMEOUT = (2, 5)
tmdb.API_KEY = constants.TMDB_TOKEN


class Quiz:
    def __init__(self, message: types.Message, user_id: str, text_to_message: str):
        self.message = message
        self.user_id = user_id
        self.text_to_message = text_to_message

        self.trueMovieID = None
        self.moviesFinder = MoviesFinder()

    async def start_quiz(self):
        pass

    def prepare_keyboard(self, correct_choice) -> InlineKeyboardMarkup:
        """
        Method, that returns a working inline keyboard with variants of films
        :param correctChoice:
        :return InlineKeyboardMarkup:
        """
        class_name = self.__class__.__name__
        VARIANTS_QUANTITY = 4
        # button with correct choice
        button1 = InlineKeyboardButton(correct_choice, callback_data=class_name + 'True')
        # get list of VARIANTS_QUANTITY movies' titles
        list_titles = self.moviesFinder.getMovieVariants(quantity=VARIANTS_QUANTITY - 1,
                                                         trueMovieID=self.trueMovieID,
                                                         titleToAvoid=correct_choice)
        # buttons with incorrect choices
        button2 = InlineKeyboardButton(list_titles[0], callback_data=class_name + 'False')
        button3 = InlineKeyboardButton(list_titles[1], callback_data=class_name + 'False')
        button4 = InlineKeyboardButton(list_titles[2], callback_data=class_name + 'False')
        # keyboard init
        keyboard = InlineKeyboardMarkup()
        # sort buttons in random order
        list_buttons = [button1, button2, button3, button4]
        random.shuffle(list_buttons)
        for btn in list_buttons:
            keyboard.add(btn)
        return keyboard


class PhotoQuiz(Quiz):
    def __init__(self, message: types.Message, user_id: str, text_to_message: str):
        super().__init__(message, user_id, text_to_message)
        # self.trueMovieID = None
        # self.moviesFinder = MoviesFinder()

    async def start_quiz(self):
        # id of movie with correct id
        self.trueMovieID = self.moviesFinder.getRandomMovieID()
        movie = tmdb.Movies(self.trueMovieID)
        # get images to movie, without text
        array = movie.images(include_image_language='null')
        # if there are no images without text, get all ones
        if len(array['backdrops']) == 0:
            array = movie.images()
        size = len(array['backdrops'])
        # form new query and get a file of random image of film from url
        new_query = 'https://image.tmdb.org/t/p/original' + array['backdrops'] \
            [randint(0, size - 1) if size > 1 else 0]['file_path']
        file = InputFile.from_url(url=new_query)
        # to receive movie.title
        response = movie.info()
        # send a new quiz with points update or just send new quiz
        await Settings.BOT.send_photo(chat_id=self.user_id,
                                      photo=file, caption='<b>' + self.text_to_message + '</b>',
                                      reply_markup=self.prepare_keyboard(movie.title),
                                      parse_mode='HTML')
        await file.file.close()


class DescrQuiz(Quiz):
    def __init__(self, message: types.Message, user_id: str, text_to_message: str):
        super().__init__(message, user_id, text_to_message)
        # self.trueMovieID = None
        # self.moviesFinder = MoviesFinder()

    async def start_quiz(self):
        self.trueMovieID = self.moviesFinder.getRandomMovieID()
        movie = tmdb.Movies(self.trueMovieID).info()
        await Settings.BOT.send_message(chat_id=self.user_id,
                                        text='<b>' + self.text_to_message + '</b>\n' + movie['overview'],
                                        reply_markup=self.prepare_keyboard(movie['title']),
                                        parse_mode='HTML')


class QuizFactory:
    def create_photo_quiz(self, message=None, user_id=None, text_to_message=None) -> PhotoQuiz:
        return PhotoQuiz(message, user_id, text_to_message)

    def create_descr_quiz(self, message=None, user_id=None, text_to_message=None) -> DescrQuiz:
        return DescrQuiz(message, user_id, text_to_message)
