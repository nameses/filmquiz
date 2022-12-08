import random
from random import randint
from aiogram import types
from aiogram.types import InputFile, InlineKeyboardButton, InlineKeyboardMarkup
import tmdbsimple as tmdb
import constants
from settings import Settings
from MoviesHelper import MoviesHelper

tmdb.REQUESTS_TIMEOUT = (2, 5)
tmdb.API_KEY = constants.TMDB_TOKEN


class Quiz:
    def __init__(self, message: types.Message, user_id: str, canBeEdited: bool):
        self.message = message
        self.user_id = user_id
        self.canBeEdited = canBeEdited


class PhotoQuiz(Quiz):
    def __init__(self, message: types.Message, user_id: str, canBeEdited: bool):
        super().__init__(message, user_id, canBeEdited)
        self.trueMovieID = None

    async def startPhotoQuiz(self):
        # id of movie with correct id
        self.trueMovieID = self.getRandomMovieID()
        movie = tmdb.Movies(self.trueMovieID)
        # get images to movie
        array = movie.images(include_image_language='null')
        # if there are no images without text, get all ones
        if len(array['backdrops']) == 0:
            array = movie.images()
        # form new query and get a file of random image of film from url
        new_query = 'https://image.tmdb.org/t/p/original' + array['backdrops'] \
            [randint(0, len(array['backdrops']) - 1)]['file_path']
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
        listTitles = self.getMovieVariants(quantity=VARIANTS_QUANTITY - 1, titleToAvoid=correctChoice)
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

    def getRandomMovieID(self) -> int:
        """
        get random movie ID from listID in MoviesHelper
        :return int:
        """
        return MoviesHelper.getRandomMovieIDFromList()

    def getMovieVariants(self, quantity=3, titleToAvoid=None) -> list:
        """
        get list of similar/random movies
        :param titleToAvoid:
        :param quantity:
        :return list:
        """
        list = []
        # # 1/3 of quantity will be from similar list, everything else is random movies
        # quantitySimilarMovies = quantity // 3
        list.extend(self.getSimilarMovieTitle(quantity=quantity, titleToAvoid=titleToAvoid))
        # list.extend(self.getRandomMovieTitle(quantity=quantity))
        return list

    def getSimilarMovieTitle(self, quantity: int, titleToAvoid: str) -> list:
        """
        returns list of similar movies of param quantity with title != param titleToAvoid
        :param quantity:
        :param titleToAvoid:
        :return:
        """
        list = []
        # get similar movies list
        movie = tmdb.Movies(self.trueMovieID)
        responseArr = movie.similar_movies()
        # responseArr['results'] is results array
        # if list has 1 element -> add it to list
        size = len(responseArr['results'])
        if size == 0:
            # get random movies
            while True:
                title = self.getRandomMovieTitle(quantity=quantity, titleToAvoid=titleToAvoid)
                if title != titleToAvoid:
                    break
            list.extend(title)
        elif size == 1 and quantity >= 2:
            # 1 similar and other are random
            while True:
                title = responseArr['results'][0]['title']
                if title != titleToAvoid:
                    break
            list.append(title)
            list.extend(self.getRandomMovieTitle(quantity=quantity - 1, titleToAvoid=titleToAvoid))
        elif size == 1 and quantity == 1:
            # 1 similar movie
            while True:
                title = responseArr['results'][0]['title']
                if title != titleToAvoid:
                    break
            list.append(title)
        else:
            # many random movies
            for i in range(0, quantity):
                list.append(responseArr['results'][randint(0, size - 1)]['title'])
        return list

    def getRandomMovieTitle(self, quantity: int, titleToAvoid: str) -> list:
        """
        returns list of random movies of param quantity with title != param titleToAvoid
        :param quantity:
        :param titleToAvoid:
        :return:
        """
        list = []
        for i in range(0, quantity):
            while True:
                randMovieID = self.getRandomMovieID()
                movie = tmdb.Movies(randMovieID)
                response = movie.info()
                title = movie.title
                if title != titleToAvoid:
                    break
            list.append(title)
        return list


class DescrQuiz(Quiz):
    def __init__(self, message: types.Message, user_id: str, canBeEdited: bool):
        super().__init__(message, user_id, canBeEdited)

    def startDescrQuiz(self):
        # TODO
        pass


class QuizFactory:
    def createPhotoQuiz(self, message=None, user_id=None, canBeEdited=False) -> PhotoQuiz:
        return PhotoQuiz(message, user_id, canBeEdited)

    def createDescrQuiz(self, message=None, user_id=None, canBeEdited=False) -> DescrQuiz:
        return DescrQuiz(message, user_id, canBeEdited)
