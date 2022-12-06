import asyncio
from aiogram import Bot, Dispatcher, types
import logging
import requests
import json
import csv
import tmdbsimple as tmdb
import constants


logging.basicConfig(level=logging.INFO)
bot = Bot(token=constants.TG_TOKEN)
dp = Dispatcher(bot=bot)


@dp.message_handler(content_types=types.ContentType.TEXT, commands=["game"])
async def cmd_game(message: types.Message):
    Movie_ID = '57158'
    await message.answer("Make your choice!", parse_mode="HTML")
    query = 'https://api.themoviedb.org/3/movie/' + Movie_ID + '/images?api_key=' + constants.TMDB_TOKEN + \
            '&language=en-US&include_image_language=en,null'
    response = requests.get(query)
    if response.status_code == 200:
        array = response.json()
        new_query = 'https://image.tmdb.org/t/p/w500/' + array['posters'][0]['file_path']
        # response = requests.get(new_query)
        # new_array = response.json()
        # new_text = json.dumps(new_array)
        await bot.send_photo(chat_id=message.from_user.id, photo=new_query)
    else:
        await message.answer('Error code: ' + str(response.status_code))


@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer("Hello! This is telegram quiz bot. You will need to guess a film by an image.\n"
                         "\\game -> start quiz.\n\\statistic -> show player statistic.")


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
