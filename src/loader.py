from aiogram import Bot
from aiogram import Dispatcher
from aiogram import types
from aiogram.contrib.fsm_storage.files import JSONStorage

from src.data import config
from src.logging import init_logger
from src.middlewares.throttling import ThrottlingMiddleware

init_logger()

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=JSONStorage("states.json"))

# Config throttling middleware
dp.middleware.setup(ThrottlingMiddleware())
