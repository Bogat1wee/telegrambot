
from dotenv import load_dotenv
import os
from os.path import join, dirname
from aiogram import Bot, Dispatcher, executor, types
from yookassa import Configuration, Payment


def get_from_env(key):
    dotenv_path = join(dirname(__file__), 'token.env')
    load_dotenv(dotenv_path)
    return os.environ.get(key)

token = get_from_env('TG_BOT_TOKEN')
bot = Bot(token)
dis = Dispatcher(bot)

@dis.message_handler(commands=['start'])
async def first(message: types.Message):
    await bot.send_invoice(message.chat.id, title='Pen', description='A high-quality pen', provider_token='1744374395:TEST:7fefb20ef8b80c0bb121', currency='rub', prices=[types.LabeledPrice(label='Настоящая Машина Времени', amount=4200000)], start_parameter='time-machine-example', payload='some-invoice-payload-for-our-internal-use')



executor.start_polling(dis)