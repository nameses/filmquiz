from random import randint
import tmdbsimple as tmdb
import constants
from MoviesHelper import MoviesHelper
from Statistic import Statistic

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

    def getSimilarMovieTitle(self, quantity: int, trueMovieID: str, title_to_avoid: str, person_id, type_quiz) -> list:
        """
        returns list of similar/random movies of param quantity with title != param titleToAvoid
        :param title_to_avoid:
        :param trueMovieID:
        :param quantity:
        :return: list
        """
        FULL_QUANTITY = quantity+1
        self.list = [title_to_avoid]

        ids_list = [trueMovieID]

        # get similar movies list
        movie = tmdb.Movies(trueMovieID)
        similar_movies = movie.similar_movies()['results']
        size = len(similar_movies)
        for i in range(0, size):
            # if list is already full, then stop finding new variants
            if len(self.list) == FULL_QUANTITY:
                break
            # random similar movie
            similar_movies_random = similar_movies[randint(0, size-1)]
            similar_movie_title = similar_movies_random['title']
            # duplicate check
            if not self.__duplicate_check(similar_movie_title):
                self.list.append(similar_movie_title)
                ids_list.append(similar_movies_random['id'])
        # if similar_movies' array < quantity
        if len(self.list) != FULL_QUANTITY:
            self.__extendWithRandom(FULL_QUANTITY, ids_list)

        stats = Statistic(person_id)
        if type_quiz == 'PhotoQuiz':
            stats.updating_pq_options(ids_list)
        else:
            stats.updating_dq_options(ids_list)

        # return self.list
        return self.list

    def __extendWithRandom(self, full_quantity: int, ids_list: list):
        """
        returns list of random movies of param quantity with title != param titleToAvoid
        :param full_quantity:
        :return: list
        """
        while True:
            if len(self.list) == full_quantity:
                break
            rand_movie_id = self.getRandomMovieID()
            movie = tmdb.Movies(rand_movie_id).info()
            if not self.__duplicate_check(title := movie['title']):
                self.list.append(title)
                ids_list.append(movie['id'])

    def __duplicate_check(self, movie: str) -> bool:
        for movie_to_avoid in self.list:
            if movie_to_avoid == movie:
                return True
        return False
