import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from models import Base


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