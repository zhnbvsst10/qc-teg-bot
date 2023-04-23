import asyncio
import logging
from aiogram import Bot, F
from aiogram import Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from handlers import common, fitting_vodop,  pvc_3, pprc, fitting_can, fitting_other, pert
import os


token = os.getenv('TOKEN')
dp = Dispatcher()
bot = Bot(token=token)

async def send_message(bot: Bot):
    
    await bot.send_message(443493321,'Проверка контроля качества. \n Перейти в /start')
    await bot.send_message(1055367376,'Проверка контроля качества. \n Перейти в /start')
    await bot.send_message(1174180760,'Проверка контроля качества. \n Перейти в /start')
    await bot.send_message(1051813835,'Проверка контроля качества. \n Перейти в /start')
    await bot.send_message(1374864950, 'Проверка контроля качества. \n Перейти в /start')
    await bot.send_message(1309686262, 'Проверка контроля качества. \n Перейти в /start')
    await bot.send_message(1247023320, 'Проверка контроля качества. \n Перейти в /start')
    
    

    
    
async def main():
    bot.delete_webhook()
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    
    sched = AsyncIOScheduler({'apscheduler.timezone':'Asia/Almaty'})
    sched.add_job(send_message,'cron',hour='0-23/1', minute = '30', kwargs= {'bot':bot} )
    sched.start()
    sched.print_jobs()
    dp.include_router(common.router)
    dp.include_router(pvc_3.router2)
    dp.include_router(pprc.router)
    dp.include_router(fitting_vodop.router)
    dp.include_router(fitting_can.router)
    dp.include_router(fitting_other.router)
    dp.include_router(pert.router2)

    await dp.start_polling(bot, skip_updates=True)




if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
    
