import random
from random import randint
from aiogram import types
from aiogram.types import InputFile, InlineKeyboardButton, InlineKeyboardMarkup
import tmdbsimple as tmdb
from MoviesFinder import MoviesFinder
import constants
from settings import Settings
import abc
from Statistic import Statistic

tmdb.REQUESTS_TIMEOUT = (2, 5)
tmdb.API_KEY = constants.TMDB_TOKEN


class Quiz(abc.ABC):
    def __init__(self, message: types.Message, user_id: int, text_to_message: str):
        self.message = message
        self.user_id = user_id
        self.text_to_message = text_to_message

        self.trueMovieID = None
        self.moviesFinder = MoviesFinder()

        self.existing_ids = None

    @abc.abstractmethod
    async def start_quiz(self):
        pass

    def prepare_keyboard(self, correct_choice: str) -> InlineKeyboardMarkup:
        """
        Method, that returns a working inline keyboard with variants of films
        :param correct_choice:
        :return InlineKeyboardMarkup:
        """
        class_name = self.__class__.__name__
        VARIANTS_QUANTITY = 4
        if not self.existing_ids:
            # button with correct choice
            # get list of VARIANTS_QUANTITY movies' titles
            list_titles = self.moviesFinder.getSimilarMovieTitle(quantity=VARIANTS_QUANTITY - 1,
                                                                 trueMovieID=self.trueMovieID,
                                                                 title_to_avoid=correct_choice,
                                                                 person_id=self.user_id,
                                                                 type_quiz=class_name)
            # buttons with incorrect choices
            list_buttons = [InlineKeyboardButton(list_titles[0], callback_data=class_name + 'True')]
            for index in range(1, VARIANTS_QUANTITY):
                list_buttons.append(InlineKeyboardButton(list_titles[index], callback_data=class_name + 'False'))
            # keyboard init
            keyboard = InlineKeyboardMarkup()
            # sort buttons in random order
            random.shuffle(list_buttons)
            for btn in list_buttons:
                keyboard.add(btn)
            return keyboard
        else:
            list_buttons = [InlineKeyboardButton(correct_choice, callback_data=class_name + 'True')]
            for index in range(1, VARIANTS_QUANTITY):
                movie = tmdb.Movies(self.existing_ids[index])
                list_buttons.append(InlineKeyboardButton(movie.info()['title'], callback_data=class_name + 'False'))
            keyboard = InlineKeyboardMarkup()
            random.shuffle(list_buttons)
            for btn in list_buttons:
                keyboard.add(btn)
            return keyboard


class PhotoQuiz(Quiz):
    def __init__(self, message: types.Message, user_id: int, text_to_message: str):
        super().__init__(message, user_id, text_to_message)

    async def start_quiz(self):
        # iterate until found at least 1 movie image
        while True:
            # id of movie with correct id
            self.trueMovieID = self.moviesFinder.getRandomMovieID()
            movie = tmdb.Movies(self.trueMovieID)
            # get images to movie, without text
            array = movie.images(include_image_language='null')
            size = len(array['backdrops'])
            # if size != 0, then found at least 1 image
            if size != 0:
                break
        # form new query and get a file of random image of film from url
        random_image = array['backdrops'] \
            [randint(0, size - 1) if size > 1 else 0]['file_path']
        new_query = 'https://image.tmdb.org/t/p/original' + random_image
        file = InputFile.from_url(url=new_query)
        # save file to our database
        statistic = Statistic(self.user_id)
        statistic.updating_fileid(random_image)
        # to receive movie.title
        response = movie.info()
        # send a new quiz with points update or just send new quiz
        await Settings.BOT.send_photo(chat_id=self.user_id,
                                      photo=file, caption='<b>' + self.text_to_message + '</b>',
                                      reply_markup=self.prepare_keyboard(movie.title),
                                      parse_mode='HTML')
        await file.file.close()

    async def resend_quiz(self):
        statistic = Statistic(self.user_id)
        self.existing_ids = statistic.get_pq_ids()
        self.trueMovieID = self.existing_ids[0]
        movie = tmdb.Movies(self.trueMovieID)
        new_query = 'https://image.tmdb.org/t/p/original' + statistic.get_fileid()
        file = InputFile.from_url(url=new_query)
        await Settings.BOT.send_photo(chat_id=self.user_id,
                                      photo=file, caption='<b>' + self.text_to_message + '</b>',
                                      reply_markup=self.prepare_keyboard(movie.info()['title']),
                                      parse_mode='HTML')
        await file.file.close()


class DescrQuiz(Quiz):
    def __init__(self, message: types.Message, user_id: int, text_to_message: str):
        super().__init__(message, user_id, text_to_message)

    async def start_quiz(self):
        self.trueMovieID = self.moviesFinder.getRandomMovieID()
        movie = tmdb.Movies(self.trueMovieID).info()
        await Settings.BOT.send_message(chat_id=self.user_id,
                                        text='<b>' + self.text_to_message + '</b>\n' + movie['overview'],
                                        reply_markup=self.prepare_keyboard(movie['title']),
                                        parse_mode='HTML')

    async def resend_quiz(self):
        statistic = Statistic(self.user_id)
        self.existing_ids = statistic.get_dq_ids()
        self.trueMovieID = self.existing_ids[0]
        movie = tmdb.Movies(self.trueMovieID).info()
        await Settings.BOT.send_message(chat_id=self.user_id,
                                        text='<b>' + self.text_to_message + '</b>\n' + movie['overview'],
                                        reply_markup=self.prepare_keyboard(movie['title']),
                                        parse_mode='HTML')


class QuizFactory:
    @classmethod
    def create_photo_quiz(cls, message=None, user_id=None, text_to_message=None) -> PhotoQuiz:
        return PhotoQuiz(message, user_id, text_to_message)

    @classmethod
    def create_descr_quiz(cls, message=None, user_id=None, text_to_message=None) -> DescrQuiz:
        return DescrQuiz(message, user_id, text_to_message)
