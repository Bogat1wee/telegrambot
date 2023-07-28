
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
async def yookassa(message):
    Configuration.account_id = get_from_env('SHOP_ID')
    Configuration.secret_key = get_from_env('PAYMENT_TOKEN')

    payment = Payment.create({
        "amount": {
            "value": "999.00",
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://www.example.com/return_url"
        },
        "capture": True,
        "description": "Заказ №37",
        "metadata": {
          "message": message
        }
    })
    await bot.send_message(message.chat.id, 'привет')




executor.start_polling(dis)