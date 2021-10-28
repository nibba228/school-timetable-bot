import os
from asyncio import get_event_loop
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

# Init environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# Redis
REDIS_URL = os.getenv('REDIS_URL')
redis_url = urlparse(REDIS_URL)

try:
    storage = RedisStorage2(redis_url.hostname, redis_url.port)
except:
    logger.exception('Не удалось подключиться к Redis по {}:{}', redis_url.hostname, redis_url.port)
else:
    logger.success('Подключение к Redis')

# Telegram bot
WEBHOOK_HOST = os.getenv('WEBHOOK_HOST')
WEBHOOK_PATH = os.getenv('WEBHOOK_PATH')
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'
TOKEN = os.getenv('BOT_TOKEN')

loop = get_event_loop()
bot = Bot(TOKEN, loop=loop)
dp = Dispatcher(bot, storage=storage)

# PostgreSQL
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL and DATABASE_URL.startswith('postgres'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

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

# Web app
WEBAPP_HOST = os.getenv('WEBAPP_HOST')
WEBAPP_PORT = int(os.getenv('PORT', 5000))