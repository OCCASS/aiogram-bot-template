from pathlib import Path
from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str('BOT_TOKEN')
POSTGRESQL_URI = env.str('POSTGRESQL_URI')

BASE_DIR = Path(__file__).parent.parent
