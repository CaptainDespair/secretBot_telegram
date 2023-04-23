from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import configs.config as config

from sqlalchemy.orm import sessionmaker
from database.create_db import engine


Session = sessionmaker(bind=engine)
session = Session()
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())