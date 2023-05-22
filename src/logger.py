import logging.handlers

from src.data import settings


def init_logger():
    logging.basicConfig(
        format="%(asctime)s - [%(levelname)s] - %(name)s - %(filename)s:%(lineno)d - %(message)s",
        level=logging.INFO,
        handlers=[
            logging.StreamHandler(),
            logging.handlers.RotatingFileHandler(
                filename=settings.PROJECT_DIR / "logs.log", maxBytes=1024 * 1024 * 5, backupCount=2
            ),
        ],
    )
