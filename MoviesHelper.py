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
        PAGES_AMOUNT = 3
        movie = tmdb.Movies()
        for i in range(0, PAGES_AMOUNT):
            responseArr = movie.top_rated(page=i+1)
            size = 0
            for element in responseArr['results']:
                size += 1
            for i in range(0, size):
                cls.listID.append(responseArr['results'][i]['id'])

    @classmethod
    def getRandomMovieIDFromList(cls) -> int:
        cls.getMovieList()
        return cls.listID[random.randint(0, cls.listID.__len__()-1)]

