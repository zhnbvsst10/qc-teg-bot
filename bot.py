import asyncio
import logging
import aiogram
from aiogram import Bot
from aiogram import Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
# from aiogram.fsm.storage.memory import MemoryStorage
from handlers import common, pvc_1, pvc_3
from aiohttp.web_app import Application
from aiohttp.web import run_app
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
import os

token = '6029120908:AAFSntMGALPmIV7eJPrLbPxXEk_pEEdTRgQ'
# HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')
# WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
# WEBHOOK_PATH = f'/webhook/{token}'
# WEBHOOK_URL = f'jdafhjasdh2u3alskd/{WEBHOOK_PATH}'
# WEBAPP_HOST = '0.0.0.0'
# WEBAPP_PORT = os.getenv('PORT', default=8081)
dp = Dispatcher()
bot = Bot(token=token)

# async def on_startup(dispatcher):
#     await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)


# async def on_shutdown(dispatcher):
#     await bot.delete_webhook()

async def send_message(bot: Bot):
    
    await bot.send_message(443493321,'Проверка контроля качества. \n Перейти в /start')
    await bot.send_message(1055367376,'Проверка контроля качества. \n Перейти в /start')
    await bot.send_message(1174180760,'Проверка контроля качества. \n Перейти в /start')
    await bot.send_message(1051813835,'Проверка контроля качества. \n Перейти в /start')
    
async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    sched = AsyncIOScheduler({'apscheduler.timezone':'Asia/Almaty'})
    sched.add_job(send_message,'cron',hour='8-20/1', minute = '30', kwargs= {'bot':bot} )
    sched.start()
    sched.print_jobs()
    dp.include_router(common.router)
    dp.include_router(pvc_1.router)
    dp.include_router(pvc_3.router2)

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    # app = Application()
    # app["bot"] = bot
    # SimpleRequestHandler(
    #     dispatcher=dp,
    #     bot=bot,
    # ).register(app, path=WEBHOOK_PATH)
    # app.router.add_get("/demo", demo_handler)
    # app.router.add_post("/demo/checkData", check_data_handler)
    # app.router.add_post("/demo/sendMessage", send_message_handler)
    # setup_application(app, dp, bot=bot)
    # run_app(app, host="0.0.0.0", port=8081)
    asyncio.run(main())
    
