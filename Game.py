from random import randint

from aiogram import Bot, Dispatcher, types
from aiogram.types import InputFile
import logging
import requests
import json
import csv
import tmdbsimple as tmdb
import constants
from Keyboards.KBPhotoQuiz import KBPhotoQuiz
from settings import Settings

tmdb.REQUESTS_TIMEOUT = (2, 5)
tmdb.API_KEY = constants.TMDB_TOKEN


class Quiz:
    def __init__(self, message: types.Message):
        self.message = message


class PhotoQuiz(Quiz):
    def __init__(self, message: types.Message):
        super().__init__(message)

    async def startPhotoQuiz(self):
        Movie_ID = self.getRandomMovieID()
        movie = tmdb.Movies(Movie_ID)
        await self.message.answer("Make your choice!", reply_markup=KBPhotoQuiz.keyboard)
        # query = 'https://api.themoviedb.org/3/movie/' + Movie_ID + '/images?api_key=' + constants.TMDB_TOKEN + \
        #         '&language=en-US&include_image_language=en,null'
        # response = requests.get(query)
        # if response.status_code == 200:
        # array = response.json()
        array = movie.images()
        backdropsSize = 0
        for element in array['backdrops']:
            backdropsSize += 1
        new_query = 'https://image.tmdb.org/t/p/w500' + array['backdrops'][randint(0, backdropsSize - 1)]['file_path']
        file = InputFile.from_url(url=new_query)
        await Settings.BOT.send_photo(chat_id=self.message.from_user.id, photo=file)

    def getRandomMovieID(self) -> int:
        # TODO
        return 57158


class DescrQuiz(Quiz):
    def __init__(self, message: types.Message):
        super().__init__(message)

    def startDescrQuiz(self):
        # TODO
        pass


class QuizFactory:
    def createPhotoQuiz(self, message) -> PhotoQuiz:
        return PhotoQuiz(message)

    def createDescrQuiz(self, message) -> DescrQuiz:
        return DescrQuiz(message)
