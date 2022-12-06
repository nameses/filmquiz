from random import randint

from aiogram import Bot, Dispatcher, types
import logging
import requests
import json
import csv
import tmdbsimple as tmdb
import constants
from settings import Settings


class Quiz:
    def __init__(self, message: types.Message):
        self.message = message


class PhotoQuiz(Quiz):
    def __init__(self, message: types.Message):
        super().__init__(message)

    async def startPhotoQuiz(self):
        Movie_ID = self.getRandomMovieID()
        await self.message.answer("Make your choice!", parse_mode="HTML")
        query = 'https://api.themoviedb.org/3/movie/' + Movie_ID + '/images?api_key=' + constants.TMDB_TOKEN + \
                '&language=en-US&include_image_language=en,null'
        response = requests.get(query)
        if response.status_code == 200:
            array = response.json()
            backdropsSize = 0
            for element in array['backdrops']:
                backdropsSize += 1
            new_query = 'https://image.tmdb.org/t/p/w500/' + \
                        array['backdrops'][randint(0, backdropsSize)]['file_path']
            await Settings.BOT.send_photo(chat_id=self.message.from_user.id, photo=new_query)
        else:
            await self.message.answer('Error code: ' + str(response.status_code))

    def getRandomMovieID(self) -> str:
        # TODO
        return '57158'


class DescrQuiz(Quiz):
    def __init__(self, message: types.Message):
        super().__init__(message)

    def startDescrQuiz(self):
        # TODO
        pass


class QuizFactory:
    @staticmethod
    def createPhotoQuiz(message) -> PhotoQuiz:
        return PhotoQuiz(message)

    @staticmethod
    def createDescrQuiz(message) -> DescrQuiz:
        return DescrQuiz(message)
