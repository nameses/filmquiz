from random import randint

from aiogram import Bot, Dispatcher, types
from aiogram.types import InputFile, InlineKeyboardButton, InlineKeyboardMarkup, InputMedia, InputMediaPhoto
import logging
import requests
import json
import csv
import tmdbsimple as tmdb
import constants
from settings import Settings
from MoviesHelper import MoviesHelper

tmdb.REQUESTS_TIMEOUT = (2, 5)
tmdb.API_KEY = constants.TMDB_TOKEN


class Quiz:
    def __init__(self, message: types.Message):
        self.message = message


class PhotoQuiz(Quiz):
    def __init__(self, message: types.Message):
        super().__init__(message)
        self.trueMovieID = None

    async def startPhotoQuiz(self):
        self.trueMovieID = self.getRandomMovieID()
        movie = tmdb.Movies(self.trueMovieID)

        array = movie.images()
        backdropsSize = 0
        for element in array['backdrops']:
            backdropsSize += 1
        new_query = 'https://image.tmdb.org/t/p/original' + array['backdrops'] \
            [randint(0, backdropsSize - 1)]['file_path']
        file = InputFile.from_url(url=new_query)

        response = movie.info()

        # await Settings.BOT.send_message(chat_id=self.message.from_user.id, text="Make your choice!")
        if self.message is None:
            await Settings.BOT.send_message(chat_id=self.message.from_user.id,
                                            text='Try to guess', photo=file,
                                            reply_markup=self.prepareKeyboard(movie.title))
            await Settings.BOT.edit_message_media(media=file)
        else:
            await callback_query.message.edit_text(text='Try to guess!',
                                                   reply_markup=self.prepareKeyboard(movie.title))
            await callback_query.message.edit_media(media=file)

    def prepareKeyboard(self, correctChoice):
        button1 = InlineKeyboardButton(correctChoice, callback_data='true')
        listTitles = self.getMovieVariants(quantity=3)
        button2 = InlineKeyboardButton(listTitles[0], callback_data='false')
        button3 = InlineKeyboardButton(listTitles[1], callback_data='false')
        button4 = InlineKeyboardButton(listTitles[2], callback_data='false')

        keyboard = InlineKeyboardMarkup()
        keyboard.add(button1) \
            .add(button2) \
            .add(button3) \
            .add(button4)
        return keyboard

    def getRandomMovieID(self) -> int:
        return MoviesHelper.getRandomMovieIDFromList()

    def getMovieVariants(self, quantity) -> list:
        list = []
        list.extend(self.getRandomMovieTitle(quantity=1))
        list.extend(self.getSimilarMovieTitle(quantity=2))
        return list

    def getSimilarMovieTitle(self, quantity) -> list:
        list = []
        # self.trueMovieID
        movie = tmdb.Movies(self.trueMovieID)
        responseArr = movie.recommendations()
        size = 0
        for element in responseArr['results']:
            size += 1
        if size == 1:
            list.append(responseArr['results'][0]['title'])
            list.extend(self.getRandomMovieTitle(quantity=1))
        else:
            for i in range(0, quantity):
                list.append(responseArr['results'][randint(0, size - 1)]['title'])
        return list

    def getRandomMovieTitle(self, quantity) -> list:
        list = []
        for i in range(0, quantity):
            randMovieID = self.getRandomMovieID()
            movie = tmdb.Movies(randMovieID)
            response = movie.info()
            list.append(movie.title)
        return list


class DescrQuiz(Quiz):
    def __init__(self, message: types.Message):
        super().__init__(message)

    def startDescrQuiz(self):
        # TODO
        pass


class QuizFactory:
    def createPhotoQuiz(self, message = None) -> PhotoQuiz:
        return PhotoQuiz(message)

    def createDescrQuiz(self, message = None) -> DescrQuiz:
        return DescrQuiz(message)
