import random
from random import randint
from aiogram import types
from aiogram.types import InputFile, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
import tmdbsimple as tmdb
from MoviesFinder import MoviesFinder
import constants
from settings import Settings


class MainKeyboard:
    keyboard = None

    @classmethod
    def get_keyboard(cls):
        if not cls.keyboard:
            button1 = KeyboardButton('Photo Quiz')
            button2 = KeyboardButton('Description Quiz')
            button3 = KeyboardButton('Statistic')

            cls.keyboard = ReplyKeyboardMarkup(resize_keyboard=True) \
                .add(button1).add(button2).add(button3)
        return cls.keyboard
