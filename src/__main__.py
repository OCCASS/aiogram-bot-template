from aiogram import executor

from src.handlers import register_all as register_all_handlers
from src.loader import dp
from src.service.database.create import create_database
from src.utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    register_all_handlers()

    await set_default_commands(dispatcher)
    await create_database()


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup)
