from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


class KBPhotoQuiz:
    keyboard = None

    def __init__(self):
        button1 = InlineKeyboardButton('1', callback_data='var1')
        button2 = InlineKeyboardButton('2', callback_data='var2')
        button3 = InlineKeyboardButton('3', callback_data='var3')
        button4 = InlineKeyboardButton('4', callback_data='var4')

        self.keyboard = ReplyKeyboardMarkup()
        self.keyboard \
            .add(button1) \
            .add(button2) \
            .add(button3) \
            .add(button4)
