import os
from aiogram import Bot, Dispatcher, executor, types
import logging
import sys

# from telegram import BotCommand

# Делаем отдельный пункт для всех файлов внутри flight_deals ибо там много всего и не хочется громоздить в одну папку
sys.path.append('flight_deals')
sys.path.append('timemachine_spotipy')

# Импорт свистелок и перделок

from weather_api import weather_forecast
from stocks_api import stocks
from flight_deals.flight_main import flight
from timemachine_spotipy.SpotifyClass import Spotify

# Классы
spotify = Spotify()

TELEGRAM_API_TOKEN = os.environ["TELEGRAM_API_TOKEN"]
print(TELEGRAM_API_TOKEN)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=TELEGRAM_API_TOKEN)
dp = Dispatcher(bot)

# Start and restart
@dp.message_handler(commands=['start', 'restart'])
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm Lane!\nWant to be friends with me? :3\nIf you want to know what I can do type /help")

# Weather
@dp.message_handler(commands=['weather'])
async def weather(message: types.Message):
    forecast = weather_forecast()
    await message.reply(forecast)

# Stocks
@dp.message_handler(commands=['amd'])
async def amd(message: types.Message):
    closes, news = stocks()
    await message.reply(closes)
    if news != 'None':
        for piece in range(0, 3):
            current_message = news[f'news_{piece}']
            formatted_message = f'Author: {current_message[0]}\nTitle: {current_message[1]}\nBody: {current_message[2]}'
            await message.reply(formatted_message)

# Flight Deal Finder
@dp.message_handler(commands=['flights'])
async def flights(message: types.Message):
    # Там на выходе список
    flight_deals = flight()
    for flight_info in flight_deals:
        current_message = flight_info
        await message.reply(current_message)


@dp.message_handler(commands=['spoti'])
async def spoti(message: types.Message):
    try:
        year = message.text.split(' ')[1]
    except IndexError:
        current_message = 'Ошибка. Скорее всего не указан год'
        await message.reply(current_message)
    current_message = spotify.create_playlist(year)
    await message.reply(current_message)

# Просто повторяет то что не входит в команды 
@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    