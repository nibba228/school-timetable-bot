import asyncio

from aiogram import Bot
from aiogram.types import BotCommand

from app.handlers.user.base import register_handlers_base
from app.handlers.user.choosing_class import register_handlers_choosing_class
from app.handlers.user.timetable import register_handlers_timetable

from loader import dp, bot, logger


async def set_commands(bot: Bot):
    commands = [
        BotCommand('start', 'Указать класс и группу'),
        BotCommand('cancel', 'Отменить текущее действие'),
        BotCommand('reset', 'Сбросить класс и группу')
    ]

    await bot.set_my_commands(commands)


@logger.catch
async def main():
    register_handlers_choosing_class(dp)
    register_handlers_timetable(dp)
    register_handlers_base(dp)

    await set_commands(bot)
    
    try:
        logger.success('Бот запущен')
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        logger.debug('Бот выключен')


if __name__ == '__main__':
    asyncio.run(main())