import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import NoResultFound

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

from models import Base, Lesson
from db_filling_in import fill_in_db


# Init environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# Telegram bot
TOKEN = os.environ['TOKEN']
bot = Bot(TOKEN)
dp = Dispatcher(bot)

# Database
DB_NAME = os.environ['DB_NAME']
engine = create_engine(f'sqlite:///{DB_NAME}')
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