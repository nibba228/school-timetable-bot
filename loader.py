import os
from urllib.parse import urlparse

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import NoResultFound

from dotenv import load_dotenv
from loguru import logger
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2


from app.models import Base
from app.models.school import Lesson
from db_filling_in import fill_in_db
from logger_config import config


# logger
logger.configure(**config)
logger.warning('Не забудьте запустить redis-server!')

# Init environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# Redis
REDIS_URL = os.environ.get('REDIS_URL')
redis_url = urlparse(REDIS_URL)

try:
    storage = RedisStorage2(redis_url.hostname, redis_url.port)
except:
    logger.exception('Не удалось подключиться к Redis по {}:{}', redis_url.hostname, redis_url.port)
else:
    logger.success('Подключение к Redis')

# Telegram bot
TOKEN = os.environ.get('BOT_TOKEN')
bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=storage)

# PostgreSQL
DATABASE_URL = os.environ.get('DATABASE_URL')

try:
    engine = create_engine(DATABASE_URL)
except:
    logger.exception('Не удалось подключиться к БД')
else:
    logger.success('Подключение к PostgreSQL')

# SQLAlchemy: set up models
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

# fill in db
try:
    session = Session()
    lesson = session.query(Lesson).filter(Lesson.id == 1).one()
except NoResultFound:
    fill_in_db(session)
finally:
    session.commit()