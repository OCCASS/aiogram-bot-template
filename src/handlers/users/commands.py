from aiogram import types
from aiogram.dispatcher import FSMContext

from src.loader import dp
from src.utils.send import send_message


@dp.message_handler(commands=["start"], state="*")
async def start_command(message: types.Message, state: FSMContext):
    await send_message(f'Hello, <pre>{message.from_user.username}</pre>')
