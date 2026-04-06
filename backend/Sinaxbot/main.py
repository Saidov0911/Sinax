import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.bot import DefaultBotProperties
from config import BOT_TOKEN
from handlers import application, list as list_handler

logging.basicConfig(level=logging.INFO)

async def main():
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    dp.include_router(application.router)
    dp.include_router(list_handler.router)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())