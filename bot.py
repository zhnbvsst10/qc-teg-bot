import asyncio
import logging
import aiogram
from aiogram import Bot, F
from aiogram import Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from handlers import common,  pvc_3
import os
from aiogram.types import Message
from aiogram.types.photo_size import PhotoSize
from datetime import datetime, timedelta
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


token = os.getenv('TOKEN')
dp = Dispatcher()
bot = Bot(token=token)

async def send_message(bot: Bot):
    
    await bot.send_message(443493321,'Проверка контроля качества. \n Перейти в /start')
    # await bot.send_message(1055367376,'Проверка контроля качества. \n Перейти в /start')
    # await bot.send_message(1174180760,'Проверка контроля качества. \n Перейти в /start')
    # await bot.send_message(1051813835,'Проверка контроля качества. \n Перейти в /start')
    
async def main():
    bot.delete_webhook()
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    
    sched = AsyncIOScheduler({'apscheduler.timezone':'Asia/Almaty'})
    sched.add_job(send_message,'cron',hour='8-20/1', minute = '30', kwargs= {'bot':bot} )
    sched.start()
    sched.print_jobs()
    dp.include_router(common.router)
    dp.include_router(pvc_3.router2)

    await dp.start_polling(bot, skip_updates=True)

@common.router.message(F.content_type.in_({'photo'}))
async def get_photo(message: Message):
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()           
    drive = GoogleDrive(gauth)  
    file_id =  message.photo[-1].file_id
    file_unique_id = message.photo[-1].file_unique_id
    PhotoSize(file_id=file_id, file_unique_id=file_unique_id, width='1920', height='1080')
    file = await bot.get_file(file_id)
    file_path = file.file_path
    filename = 'pvc_' + (datetime.now() + timedelta(hours=6)).strftime('%Y-%m-%d %H:%M:%S' + '.jpg')
    await bot.download_file(file_path, filename )
    upload_file_list = [filename]
    for upload_file in upload_file_list:
        gfile = drive.CreateFile({'parents': [{'id': '1yaz2rotCLCAfzusoOujCe7gW1Ec1fFqU'}]})
        gfile.SetContentFile(upload_file)
        gfile.Upload()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
    
