from aiogram import types

from loader import dp
from utils.send import send_message


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await send_message('Hello')
