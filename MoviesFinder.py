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


class MoviesFinder:
    def __init__(self):
        pass

    def getRandomMovieID(self) -> int:
        """
        get random movie ID from listID in MoviesHelper
        :return int:
        """
        return MoviesHelper.getRandomMovieIDFromList()

    def getMovieVariants(self, quantity: int, trueMovieID: str, titleToAvoid: str) -> list:
        """
        get list of similar/random movies
        :param trueMovieID:
        :param titleToAvoid:
        :param quantity:
        :return list:
        """
        list = []
        # quantitySimilarMovies = quantity // 3
        list.extend(self.__getSimilarMovieTitle(quantity=quantity, trueMovieID=trueMovieID, titleToAvoid=titleToAvoid))
        # list.extend(self.getRandomMovieTitle(quantity=quantity))
        return list

    def __getSimilarMovieTitle(self, quantity: int, trueMovieID: str, titleToAvoid: str) -> list:
        """
        returns list of similar movies of param quantity with title != param titleToAvoid
        :param trueMovieID:
        :param quantity:
        :param titleToAvoid:
        :return:
        """
        list = []
        # get similar movies list
        movie = tmdb.Movies(trueMovieID)
        responseArr = movie.similar_movies()
        # responseArr['results'] is results array
        # if list has 1 element -> add it to list
        size = len(responseArr['results'])
        if size == 0:
            # get random movies
            # checking for duplicate of titles is optional, probability of this is too low
            list.extend(self.__getRandomMovieTitle(quantity=quantity, titleToAvoid=titleToAvoid))
        elif size == 1 and quantity >= 2:
            # 1 similar and other are random
            # probability of duplicates is low too, check only for correct title
            title = responseArr['results'][0]['title']
            if title == titleToAvoid:
                title = self.__getRandomMovieTitle(quantity=1, titleToAvoid=titleToAvoid)
            list.append(title)
            list.extend(self.__getRandomMovieTitle(quantity=quantity - 1, titleToAvoid=titleToAvoid))
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

    def __getRandomMovieTitle(self, quantity: int, titleToAvoid: str) -> list:
        """
        returns list of random movies of param quantity with title != param titleToAvoid
        :param titleToAvoid:
        :param quantity:
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
