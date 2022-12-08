import random
import urllib3
from aiogram import Bot, Dispatcher, types
from aiogram.types import InputFile, InlineKeyboardButton, InlineKeyboardMarkup
import logging
import requests
import json
import csv
import tmdbsimple as tmdb
import constants
from settings import Settings
import gzip

tmdb.REQUESTS_TIMEOUT = (2, 5)
tmdb.API_KEY = constants.TMDB_TOKEN


class MoviesHelper:
    listID = []

    @classmethod
    def getMovieList(cls):
        PAGES_AMOUNT = 9
        movie = tmdb.Movies()
        for i in range(0, PAGES_AMOUNT):
            responseArr = movie.top_rated(page=i + 1)
            size = 0
            for element in responseArr['results']:
                if element['original_language'] == 'zh' or \
                        element['original_language'] == 'ja' or \
                        element['original_language'] == 'hi' or \
                        element['original_language'] == 'ko':
                    continue
                else:
                    cls.listID.append(element['id'])

    @classmethod
    def getRandomMovieIDFromList(cls) -> int:
        cls.getMovieList()
        return cls.listID[random.randint(0, cls.listID.__len__() - 1)]
