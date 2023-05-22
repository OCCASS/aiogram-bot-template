from pathlib import Path

from environs import Env

env = Env()
env.read_env()

BASE_DIR = Path(__file__).parent.parent
PROJECT_DIR = BASE_DIR.parent
TEMPLATES_DIR = PROJECT_DIR / "templates"

BOT_TOKEN = env.str("BOT_TOKEN")
POSTGRESQL_URI = env.str("POSTGRESQL_URI")
