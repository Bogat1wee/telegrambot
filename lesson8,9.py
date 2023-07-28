import sqlite3

from dotenv import load_dotenv
import os
from os.path import join, dirname
import telebot
from telebot import types
from currency_converter import CurrencyConverter

cur = CurrencyConverter()
money = 0
def get_from_env(key):
    dotenv_path = join(dirname(__file__), 'token.env')
    load_dotenv(dotenv_path)
    return os.environ.get(key)

token = get_from_env('TG_BOT_TOKEN')
bot = telebot.TeleBot(token)

@bot.message_handler(commands =['start'])
def first(message):
    bot.send_message(message.chat.id,f'<i>Здравствуйте! Введите сумму:</i>', parse_mode='html')
    bot.register_next_step_handler(message, summ)

def summ(message):
    global money
    try:
        money = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, 'Формат не верный. Впишите сумму:')
        bot.register_next_step_handler(message, summ)
        return
    if money > 0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        bot1 = types.InlineKeyboardButton('EUR/USD', callback_data='eur/usd')
        bot2 = types.InlineKeyboardButton('USD/EUR', callback_data='usd/eur')
        bot3 = types.InlineKeyboardButton('EUR/JPY', callback_data='eur/jpy')
        bot4 = types.InlineKeyboardButton('JPY/EUR', callback_data='jpy/eur')
        bot5 = types.InlineKeyboardButton('Другое значение', callback_data='else')
        markup.add(bot1, bot2, bot3, bot4, bot5)
        bot.send_message(message.chat.id, 'Выберите пару валют:', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Сумма должна быть положительной. Впишите сумму еще раз:')
        bot.register_next_step_handler(message, summ)

@bot.callback_query_handler(func = lambda call: True)
def callback(call):
    if call.data != 'else':
        value = call.data.upper().split('/')
        r = cur.convert(money, value[0], value[1])
        bot.send_message(call.message.chat.id, f'Получается: {r}. Можете ввести сумму заново:')
        bot.register_next_step_handler(call.message, summ)
    else:
        bot.send_message(call.message.chat.id, "Введите пару значение через '/'")
        bot.register_next_step_handler(call.message, mycur)

def mycur(message):
    try:
        value = message.data.upper().split('/')
        r = cur.convert(money, value[0], value[1])
        bot.send_message(message.chat.id, f'Получается: {r}. Можете ввести сумму заново:')
        bot.register_next_step_handler(message, summ)
    except Exception:
        bot.send_message(message.chat.id, 'Что-то введено не коректно. Попробуйте ввести заново:')
        bot.register_next_step_handler(message, mycur)

bot.polling(none_stop=True)