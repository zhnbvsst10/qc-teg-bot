import asyncio
import logging
from aiogram import Bot, F
from aiogram import Dispatcher, types
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.filters.command import Command
from handlers import common, fitting_vodop,  pvc_3, pprc, fitting_can, fitting_other, pert
import os
import psycopg2

#token = os.getenv('TOKEN')
token = '7491228760:AAFnb_5APIBYInpumPOgLNsF1D5xl6ItBs8'
dp = Dispatcher()
bot = Bot(token=token)


def connect_db():
    conn = psycopg2.connect('postgresql://neondb_owner:npg_qKfatzsHP75o@ep-blue-lake-a4lt99hy-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require')
    return conn

def save_user_id(user_id: int):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (user_id) 
        VALUES (%s) 
        ON CONFLICT (user_id) DO NOTHING;
    """, (user_id,))
    conn.commit()
    cursor.close()
    conn.close()

@dp.message(Command(commands=["register"]))
async def register_user(message: types.Message):
    save_user_id(message.from_user.id)
    await message.reply("Вы зарегистрированы!")


async def send_message(bot: Bot):
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users")
    user_ids = cursor.fetchall()
    cursor.close()
    conn.close()

    for user_id in user_ids:
        try:
            await bot.send_message(user_id[0], 'Проверка контроля качества. \n Перейти в /start')
        except Exception as e:
            print(f"Не удалось отправить сообщение {user_id[0]}: {e}")
    
    

    
    
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
    
