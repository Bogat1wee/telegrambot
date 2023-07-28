
from dotenv import load_dotenv
import os
from os.path import join, dirname
from aiogram import Bot, Dispatcher, executor, types
def get_from_env(key):
    dotenv_path = join(dirname(__file__), 'token.env')
    load_dotenv(dotenv_path)
    return os.environ.get(key)

token = get_from_env('TG_BOT_TOKEN')
bot = Bot(token)
dis = Dispatcher(bot)

@dis.message_handler(commands=['start'])
async def start(message: types.Message):
    #await bot.send_message(message.chat.id, 'Приветствуем вас в нашем telegram боте')
    file = open('./photo.jpg', 'rb')
    await message.answer_photo(file)
@dis.message_handler(content_types=['inline'])
async def second(message: types.Message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Telegram канал', url = 'https://t.me/pythotelegram'))
    markup.add(types.InlineKeyboardButton('Привет', callback_data= 'Привет'))
    await bot.send_message(message.chat.id, 'Привет!', reply_markup=markup)

@dis.callback_query_handler()
async def callback(call):
    await call.message.answer(call.data)

@dis.message_handler(commands=['reply'])
async def reply(message: types.Message):
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton('help'))
    await bot.send_message(message.chat.id, 'Приветствуем вас в нашем telegram боте', reply_markup=markup)

executor.start_polling(dis)