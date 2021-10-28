from aiogram import Bot
from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram.dispatcher.storage import DisabledStorage
from aiogram.types import BotCommand
from aiogram.utils.executor import start_webhook

from app.handlers.user.base import register_handlers_base
from app.handlers.user.choosing_class import register_handlers_choosing_class
from app.handlers.user.timetable import register_handlers_timetable

from loader import (WEBAPP_HOST, WEBAPP_PORT, WEBHOOK_PATH, WEBHOOK_URL,
                    dp, bot, logger)


async def set_commands(bot: Bot):
    commands = [
        BotCommand('start', 'Указать класс и группу'),
        BotCommand('cancel', 'Отменить текущее действие'),
        BotCommand('reset', 'Сбросить класс и группу')
    ]

    await bot.set_my_commands(commands)


@logger.catch
async def on_startup(dp: Dispatcher):
    await bot.set_webhook(url=WEBHOOK_URL)

    register_handlers_choosing_class(dp)
    register_handlers_timetable(dp)
    register_handlers_base(dp)

    await set_commands(bot)

    logger.warning('Starting bot...')


@logger.catch
async def on_shutdown(dp: Dispatcher):
    await dp.storage.close()
    await dp.storage.wait_closed()


    
    
    logger.warning('Shutting down bot...')


if __name__ == '__main__':
    start_webhook(dp, WEBHOOK_PATH, on_startup=on_startup, on_shutdown=on_shutdown,
                  skip_updates=True, host=WEBAPP_HOST, port=WEBAPP_PORT)