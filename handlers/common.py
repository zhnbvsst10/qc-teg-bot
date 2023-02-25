from aiogram import Router
from aiogram.filters.command import Command
from aiogram.filters.text import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, KeyboardButton,ReplyKeyboardMarkup
from datetime import datetime, timedelta
import psycopg2

router = Router()

available_options = ['работает', 'ремонт', 'остановка для настройки']

@router.message(Command(commands=["hello"]))
async def hello(message: Message, state: FSMContext):
    await state.clear()
    msg = await message.answer(
                        text="спасибо за ваше сообщение ! ",
                        )
    print(msg)
@router.message(Command(commands=["start"]))
#@router.message(Text(text='работает'))
async def cmd_start_3(message: Message, state: FSMContext):
    await state.clear()
    print()
    if (datetime.now()+ timedelta(hours = 6)).hour  in [0, 8,9,10,11,12,13,14,15,16,17,18,18,20]:
        kb6 = [[KeyboardButton(text='PVC трубa'),KeyboardButton(text='PPR-C трубa') ]]
        keyboard6 = ReplyKeyboardMarkup(keyboard=kb6,resize_keyboard=True)
        await message.answer(
                        text="Выберите изделие: ",
                        reply_markup=keyboard6
                        )
    else:
        msg = await message.answer(
                        text="В данный момент работы не ведутся ",
                        )

#@router.message(Command(commands=["start"]))
@router.message(Text(text='PVC трубa'))
async def working(message: Message, state: FSMContext):
    kb6 = [[KeyboardButton(text='работает'),KeyboardButton(text='остановка для настройки'), KeyboardButton(text='ремонт'), ]]
    keyboard6 = ReplyKeyboardMarkup(keyboard=kb6,resize_keyboard=True)
    await message.answer(
                            text="Работает ли сейчас линия ?",
                            reply_markup=keyboard6
                            )
@router.message(Text(text='ремонт'))
async def not_working(message: Message, state: FSMContext):
    await state.clear()
    conn = psycopg2.connect(dbname="neondb", user="zhanabayevasset", password="txDhFR1yl8Pi", host='ep-cool-poetry-346809.us-east-2.aws.neon.tech')
    cursor = conn.cursor()
    cursor.execute(f"""insert into pvc_params (working, created_at, updated_at) values (FALSE, current_timestamp + interval'6 hours', current_timestamp + interval'6 hours')""")
    conn.commit()
    cursor.close()
    conn.close()
    await message.answer(
            text="Благодарю за заполненные данные",
            reply_markup=ReplyKeyboardRemove())


@router.message(Text(text='остановка для настройки'))
async def not_working(message: Message, state: FSMContext):
    await state.clear()
    conn = psycopg2.connect(dbname="neondb", user="zhanabayevasset", password="txDhFR1yl8Pi", host='ep-cool-poetry-346809.us-east-2.aws.neon.tech')
    cursor = conn.cursor()
    cursor.execute(f"""insert into pvc_params (working, created_at, updated_at) values (FALSE, current_timestamp + interval'6 hours', current_timestamp + interval'6 hours')""")
    conn.commit()
    cursor.close()
    conn.close()
    await message.answer(
            text="Благодарю за заполненные данные",
            reply_markup=ReplyKeyboardRemove())



@router.message(Command(commands=["cancel"]))
@router.message(Text(text="отмена", ))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Действие отменено",
        reply_markup=ReplyKeyboardRemove()
    )
