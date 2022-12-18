from random import randint
import tmdbsimple as tmdb
import constants
from MoviesHelper import MoviesHelper

tmdb.REQUESTS_TIMEOUT = (2, 5)
tmdb.API_KEY = constants.TMDB_TOKEN


class MoviesFinder:
    def __init__(self):
        self.list = None

    def getRandomMovieID(self) -> int:
        """
        get random movie ID from listID in MoviesHelper
        :return int:
        """
        return MoviesHelper.getRandomMovieIDFromList()

    def getSimilarMovieTitle(self, quantity: int, trueMovieID: str, title_to_avoid: str) -> list:
        """
        returns list of similar/random movies of param quantity with title != param titleToAvoid
        :param title_to_avoid:
        :param trueMovieID:
        :param quantity:
        :return:
        """
        FULL_QUANTITY = quantity+1
        self.list = [title_to_avoid]
        # get similar movies list
        movie = tmdb.Movies(trueMovieID)
        similar_movies = movie.similar_movies()['results']
        size = len(similar_movies)
        for i in range(0, size):
            # if list is already full, then stop finding new variants
            if len(self.list) == FULL_QUANTITY:
                break
            # random similar movie
            similar_movie = similar_movies[randint(0, size-1)]['title']
            # duplicate check
            if self.__duplicate_check(similar_movie):
                continue
            self.list.append(similar_movie)
        # if similar_movies' array < quantity
        if len(self.list) != FULL_QUANTITY:
            self.__extendWithRandom(FULL_QUANTITY-len(self.list))
        return self.list

    def __extendWithRandom(self, quantity: int):
        """
        returns list of random movies of param quantity with title != param titleToAvoid
        :param quantity:
        :return: list
        """
        while True:
            if len(self.list) == quantity+1:
                break
            randMovieID = self.getRandomMovieID()
            movie = tmdb.Movies(randMovieID).info()
            if self.__duplicate_check(title := movie['title']):
                continue
            self.list.append(title)

    def __duplicate_check(self, movie: str) -> bool:
        for movie_to_avoid in self.list:
            if movie_to_avoid == movie:
                return True
        return False
