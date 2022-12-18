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
        PAGES_AMOUNT = 12
        movie = tmdb.Movies()
        for i in range(0, PAGES_AMOUNT):
            responseArr = movie.top_rated(page=i + 1)
            for element in responseArr['results']:
                if not element['original_language'] in ('zh', 'ja', 'hi', 'ko') \
                        and not element['adult']:
                    cls.listID.append(element['id'])

    @classmethod
    def getRandomMovieIDFromList(cls) -> int:
        if not cls.listID.__len__():
            cls.getMovieList()
        return cls.listID[random.randint(0, cls.listID.__len__() - 1)]
