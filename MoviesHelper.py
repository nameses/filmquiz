import random
import tmdbsimple as tmdb
import constants

tmdb.REQUESTS_TIMEOUT = (2, 5)
tmdb.API_KEY = constants.TMDB_TOKEN


class MoviesHelper:
    listID = []

    @classmethod
    def getMovieList(cls):
        # 1 page = 20 movies
        PAGES_AMOUNT = 20
        movie = tmdb.Movies()
        for i in range(0, PAGES_AMOUNT):
            responseArr = movie.top_rated(page=i + 1)
            size = 0
            for element in responseArr['results']:
                if element['original_language'] == 'zh' or \
                        element['original_language'] == 'ja' or \
                        element['original_language'] == 'hi' or \
                        element['original_language'] == 'ko' or \
                        element['adult'] == True:
                    continue
                else:
                    cls.listID.append(element['id'])

    @classmethod
    def getRandomMovieIDFromList(cls) -> int:
        if cls.listID.__len__() == 0:
            cls.getMovieList()
        return cls.listID[random.randint(0, cls.listID.__len__() - 1)]
