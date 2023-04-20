import asyncio
import logging
from aiogram import Bot, F
from aiogram import Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from handlers import common, fitting_vodop,  pvc_3, pprc, fitting_can, fitting_other, pert
import os
from aiogram.types import Message
from aiogram.types.photo_size import PhotoSize
from datetime import datetime, timedelta
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from aiogram.fsm.context import FSMContext

token = os.getenv('TOKEN')
dp = Dispatcher()
bot = Bot(token=token)

async def send_message(bot: Bot):
    
    await bot.send_message(443493321,'Проверка контроля качества. \n Перейти в /start')
    # await bot.send_message(1055367376,'Проверка контроля качества. \n Перейти в /start')
    # await bot.send_message(1174180760,'Проверка контроля качества. \n Перейти в /start')
    # await bot.send_message(1051813835,'Проверка контроля качества. \n Перейти в /start')
    # await bot.send_message(1374864950, 'Проверка контроля качества. \n Перейти в /start')
    # await bot.send_message(1309686262, 'Проверка контроля качества. \n Перейти в /start')
    # await bot.send_message(1247023320, 'Проверка контроля качества. \n Перейти в /start')
    

    
    
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

@pvc_3.router2.message(pvc_3.SetParameterPVC3.send_photo,F.content_type.in_({'photo'}))
async def get_photo_pvc(message: Message, state: FSMContext):
    await state.clear()
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
        gfile = drive.CreateFile({'parents': [{'id': '1Dmbaj2-puU0mOo4s35-Ud-1aF8u-WVmK'}]})
        gfile.SetContentFile(upload_file)
        gfile.Upload()

# @fitting_vodop.router.message(fitting_vodop.SetParameterFit.send_photo, F.content_type.in_({'photo'}))
# async def get_photo_fit(message: Message, state: FSMContext):
#     await state.clear()
#     gauth = GoogleAuth()
#     gauth.LocalWebserverAuth()           
#     drive = GoogleDrive(gauth)  
#     file_id =  message.photo[-1].file_id
#     file_unique_id = message.photo[-1].file_unique_id
#     PhotoSize(file_id=file_id, file_unique_id=file_unique_id, width='1920', height='1080')
#     file = await bot.get_file(file_id)
#     file_path = file.file_path
#     filename = 'fit_' + (datetime.now() + timedelta(hours=6)).strftime('%Y-%m-%d %H:%M:%S' + '.jpg')
#     await bot.download_file(file_path, filename )
#     upload_file_list = [filename]
#     for upload_file in upload_file_list:
#         gfile = drive.CreateFile({'parents': [{'id': '1VHMD2m_CBy6zGobYF6YPCJtyhYQdoHGS'}]})
#         gfile.SetContentFile(upload_file)
#         gfile.Upload()

# @pprc.router.message(pprc.SetParameterPPRC.send_photo, F.content_type.in_({'photo'}))
# async def get_photo_pprc(message: Message, state: FSMContext):
#     await state.clear()
#     gauth = GoogleAuth()
#     gauth.LocalWebserverAuth()           
#     drive = GoogleDrive(gauth)  
#     file_id =  message.photo[-1].file_id
#     file_unique_id = message.photo[-1].file_unique_id
#     PhotoSize(file_id=file_id, file_unique_id=file_unique_id, width='1920', height='1080')
#     file = await bot.get_file(file_id)
#     file_path = file.file_path
#     filename = 'pprc_' + (datetime.now() + timedelta(hours=6)).strftime('%Y-%m-%d %H:%M:%S' + '.jpg')
#     await bot.download_file(file_path, filename )
#     upload_file_list = [filename]
#     for upload_file in upload_file_list:
#         gfile = drive.CreateFile({'parents': [{'id': '1VnkFYt-wgCIyaEDoYUsOjjkYP0BzXQcE'}]})#1VHMD2m_CBy6zGobYF6YPCJtyhYQdoHGS#'1yaz2rotCLCAfzusoOujCe7gW1Ec1fFqU'
#         gfile.SetContentFile(upload_file)
#         gfile.Upload()

# @fitting_can.router.message(pprc.SetParameterPPRC.send_photo, F.content_type.in_({'photo'}))
# async def get_photo_pprc(message: Message, state: FSMContext):
#     await state.clear()
#     gauth = GoogleAuth()
#     gauth.LocalWebserverAuth()           
#     drive = GoogleDrive(gauth)  
#     file_id =  message.photo[-1].file_id
#     file_unique_id = message.photo[-1].file_unique_id
#     PhotoSize(file_id=file_id, file_unique_id=file_unique_id, width='1920', height='1080')
#     file = await bot.get_file(file_id)
#     file_path = file.file_path
#     filename = 'fitting_canal_' + (datetime.now() + timedelta(hours=6)).strftime('%Y-%m-%d %H:%M:%S' + '.jpg')
#     await bot.download_file(file_path, filename )
#     upload_file_list = [filename]
#     for upload_file in upload_file_list:
#         gfile = drive.CreateFile({'parents': [{'id': '1ARI8PS_-W0lqY9OXW3l_CmsXuk-c5reK'}]})#1VHMD2m_CBy6zGobYF6YPCJtyhYQdoHGS#'1yaz2rotCLCAfzusoOujCe7gW1Ec1fFqU'
#         gfile.SetContentFile(upload_file)
#         gfile.Upload()

# @fitting_other.router.message(pprc.SetParameterPPRC.send_photo, F.content_type.in_({'photo'}))
# async def get_photo_pprc(message: Message, state: FSMContext):
#     await state.clear()
#     gauth = GoogleAuth()
#     gauth.LocalWebserverAuth()           
#     drive = GoogleDrive(gauth)  
#     file_id =  message.photo[-1].file_id
#     file_unique_id = message.photo[-1].file_unique_id
#     PhotoSize(file_id=file_id, file_unique_id=file_unique_id, width='1920', height='1080')
#     file = await bot.get_file(file_id)
#     file_path = file.file_path
#     filename = 'fitting_other_' + (datetime.now() + timedelta(hours=6)).strftime('%Y-%m-%d %H:%M:%S' + '.jpg')
#     await bot.download_file(file_path, filename )
#     upload_file_list = [filename]
#     for upload_file in upload_file_list:
#         gfile = drive.CreateFile({'parents': [{'id': '1JsCMWFtu4SNODoEr51PPFGKj8tU_q9sk'}]})#1VHMD2m_CBy6zGobYF6YPCJtyhYQdoHGS#'1yaz2rotCLCAfzusoOujCe7gW1Ec1fFqU'
#         gfile.SetContentFile(upload_file)
#         gfile.Upload()

# @pert.router.message(pprc.SetParameterPPRC.send_photo, F.content_type.in_({'photo'}))
# async def get_photo_pprc(message: Message, state: FSMContext):
#     await state.clear()
#     gauth = GoogleAuth()
#     gauth.LocalWebserverAuth()           
#     drive = GoogleDrive(gauth)  
#     file_id =  message.photo[-1].file_id
#     file_unique_id = message.photo[-1].file_unique_id
#     PhotoSize(file_id=file_id, file_unique_id=file_unique_id, width='1920', height='1080')
#     file = await bot.get_file(file_id)
#     file_path = file.file_path
#     filename = 'pert_' + (datetime.now() + timedelta(hours=6)).strftime('%Y-%m-%d %H:%M:%S' + '.jpg')
#     await bot.download_file(file_path, filename )
#     upload_file_list = [filename]
#     for upload_file in upload_file_list:
#         gfile = drive.CreateFile({'parents': [{'id': '1NwwKZX-0JbjnoagbHu5c5LpGCPia_rz3'}]})#1VHMD2m_CBy6zGobYF6YPCJtyhYQdoHGS#'1yaz2rotCLCAfzusoOujCe7gW1Ec1fFqU'
#         gfile.SetContentFile(upload_file)
#         gfile.Upload()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
    
