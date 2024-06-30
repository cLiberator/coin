import asyncio
from aiogram import Dispatcher
from bot_funcs import bot
from handlers import user_router
from database_models import async_setup

dp = Dispatcher()


@dp.startup()
async def on_startup():
    await bot.delete_webhook(True)


async def run_bot():
    await async_setup()
    dp.include_router(user_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(run_bot())
    except Exception as e:
        print(e)
