import os

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
redis_host = os.environ['REDIS_HOST']
redis_port = int(os.environ['REDIS_PORT'])
try:
    storage = RedisStorage2(redis_host, redis_port)
except:
    logger.exception('Не удалось подключиться к Redis по {}:{}', redis_host, redis_port)
else:
    logger.success('Подключение к Redis')

# Telegram bot
TOKEN = os.environ['TOKEN']
bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=storage)

# PostgreSQL
params = 'HOST', 'PORT', 'USER', 'PASS'
host, port, username, password = [os.environ['POSTGRES_' + param] for param in params]

try:
    engine = create_engine(f'postgresql://{username}:{password}@{host}:{port}/timetable')
except:
    logger.exception('Не удалось подключиться к БД по {}:{}', host, port)
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