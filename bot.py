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

@bot.message_handler(commands =['start'])
def first(message):
    markup = types.ReplyKeyboardMarkup()
    bot1 = types.KeyboardButton('Перейти в telegram группу')
    bot2 = types.KeyboardButton('help')
    markup.row(bot1, bot2)
    bot.send_message(message.chat.id,f'<i>Приветствуем вас, <b>{message.from_user.first_name}</b>, в нашем telegram боте</i>', \
                     parse_mode='html', reply_markup=markup)
    bot.register_next_step_handler(message, txt)

def txt(message):
    if message.text == 'Перейти в telegram группу':
        bot.send_message(message.chat.id, '<i><b>https://t.me/pythotelegram</b></i>', parse_mode='html')
    elif message.text == 'help' or message.text.lower() == 'помощь':
        bot.send_message(message.chat.id,f'<i>Ответы на вопросы можно найти в нашем telegram канале : <b>@pythotelegram</b></i>',\
                         parse_mode='html')

    @bot.message_handler(content_types=['photo'])
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

    #для кнопок под текстом
    #markup = types.InlineKeyboardMarkup()
    #bot1 = types.InlineKeyboardButton('Перейти в telegram группу', url = 'https://t.me/pythotelegram')
    #bot2 = types.InlineKeyboardButton('help', callback_data='hlp')
    #markup.row(bot1, bot2)
    #bot.send_message(message.chat.id, f'<i>Приветствуем вас, <b>{message.from_user.first_name}</b>, в нашем telegram боте</i>',\
    #parse_mode='html', reply_markup=markup)

    #@bot.callback_query_handler(func = lambda callback: True)
    #def callback_message(callback):
    #if callback.data == 'hlp':
    #bot.send_message(callback.message.chat.id, f'<i>Ответы на вопросы можно найти в нашем telegram канале : <b>@pythotelegram</b></i>',\
    #parse_mode='html')

@bot.message_handler(commands =['help', 'Помощь'])
def first(message):
    bot.send_message(message.chat.id, f'<i>Ответы на вопросы можно найти в нашем telegram канале : <b>@pythotelegram</b></i>', parse_mode='html')

bot.polling(none_stop=True)