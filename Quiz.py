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
    def __init__(self, message: types.Message, user_id: str, canBeEdited: bool):
        self.message = message
        self.user_id = user_id
        self.canBeEdited = canBeEdited

    async def startQuiz(self):
        pass


class PhotoQuiz(Quiz):
    def __init__(self, message: types.Message, user_id: str, canBeEdited: bool):
        super().__init__(message, user_id, canBeEdited)
        self.trueMovieID = None
        self.moviesFinder = MoviesFinder()

    async def startQuiz(self):
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
        # delete, receive points and send a new quiz with points update or just send new quiz
        if self.canBeEdited:
            text = self.message.text.title()
            await self.message.delete()
            await Settings.BOT.send_photo(chat_id=self.user_id,
                                          photo=file, caption=text,
                                          reply_markup=self.prepareKeyboard(movie.title))
        else:
            await Settings.BOT.send_photo(chat_id=self.message.from_user.id,
                                          photo=file, caption='Try to guess',
                                          reply_markup=self.prepareKeyboard(movie.title))
        await file.file.close()

    def prepareKeyboard(self, correctChoice) -> InlineKeyboardMarkup:
        """
        Method, that returns a working inline keyboard with variants of films
        :param correctChoice:
        :return InlineKeyboardMarkup:
        """
        VARIANTS_QUANTITY = 4
        # button with correct choice
        button1 = InlineKeyboardButton(correctChoice, callback_data='true')
        # get list of VARIANTS_QUANTITY movies' titles
        listTitles = self.moviesFinder.getMovieVariants(quantity=VARIANTS_QUANTITY - 1,
                                                        trueMovieID=self.trueMovieID,
                                                        titleToAvoid=correctChoice)
        # buttons with uncorrect choices
        button2 = InlineKeyboardButton(listTitles[0], callback_data='false')
        button3 = InlineKeyboardButton(listTitles[1], callback_data='false')
        button4 = InlineKeyboardButton(listTitles[2], callback_data='false')
        # keyboard init
        keyboard = InlineKeyboardMarkup()
        # sort buttons in random order
        listButtons = [button1, button2, button3, button4]
        listIndexes = [0, 1, 2, 3]
        for i in range(0, VARIANTS_QUANTITY):
            randIndex = random.randint(0, listIndexes.__len__() - 1)
            keyboard.add(listButtons[listIndexes[randIndex]])
            listIndexes.remove(listIndexes[randIndex])
        return keyboard


class DescrQuiz(Quiz):
    def __init__(self, message: types.Message, user_id: str, canBeEdited: bool):
        super().__init__(message, user_id, canBeEdited)

    def startQuiz(self):
        # TODO
        pass


class QuizFactory:
    def createPhotoQuiz(self, message=None, user_id=None, canBeEdited=False) -> PhotoQuiz:
        return PhotoQuiz(message, user_id, canBeEdited)

    def createDescrQuiz(self, message=None, user_id=None, canBeEdited=False) -> DescrQuiz:
        return DescrQuiz(message, user_id, canBeEdited)
