from dotenv import load_dotenv
import os
from os.path import join, dirname
import telebot
from telebot import types

def get_from_env(key):
    dotenv_path = join(dirname(__file__), 'token.env')
    load_dotenv(dotenv_path)
    return os.environ.get(key)

token = get_from_env('TG_BOT_TOKEN')
bot = telebot.TeleBot(token)

@bot.message_handler(content_types= ['photo'])
def get_file(message):
    bot.reply_to(message, 'Великолепная фотография')

@bot.message_handler(commands=['photo'])
def send_ph(message):
    file = open('./photo.jpg', 'rb')
    bot.send_photo(message.chat.id, file)

@bot.message_handler(commands=['audio'])
def send_au(message):
    file = open('./audio.mp3', 'rb')
    bot.send_audio(message.chat.id, file)

bot.polling(none_stop=True)