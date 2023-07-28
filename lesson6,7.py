import sqlite3

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

name = ''
@bot.message_handler(commands =['start'])
def first(message):
    con = sqlite3.connect('telegrambot.sql')
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users(id int auto_increment primary key, name varchar(50), VALUE varchar(50))')
    con.commit()
    cur.close()
    con.close()
    bot.send_message(message.chat.id, 'Привет! Напиши свое имя')
    bot.register_next_step_handler(message, user_name)

def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, 'Напишите ваш счет')
    bot.register_next_step_handler(message, user_value)

def user_value(message):
    value = message.text.strip()
    con = sqlite3.connect('telegrambot.sql')
    cur = con.cursor()
    cur.execute(f'INSERT INTO users (name, VALUE) VALUES ("%s", "%s")' % (name, value))
    con.commit()
    cur.close()
    con.close()

    markup = types.ReplyKeyboardMarkup()
    bd = types.KeyboardButton('Список пользователей')
    markup.row(bd)
    bot.send_message(message.chat.id, 'Вы успешно зарегестрированы!', reply_markup=markup)
    bot.register_next_step_handler(message, new)

def new(message):
    if message.text == 'Список пользователей':
        con = sqlite3.connect('telegrambot.sql')
        cur = con.cursor()
        cur.execute('SELECT * FROM users')
        users = cur.fetchall()
        info = ' '
        for i in users:
            info += f'Имя:{i[1]}, ваш счет:{i[2]}\n'
        cur.close()
        con.close()

        bot.send_message(message.chat.id, info)


bot.polling(none_stop=True)