from aiogram import Router,  F
from aiogram.filters.command import Command
from aiogram.filters.text import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, KeyboardButton,ReplyKeyboardMarkup
from datetime import datetime, timedelta
import psycopg2
from keyboards.simple_row import make_row_keyboard
from aiogram.fsm.state import StatesGroup, State

class SetParameterFit(StatesGroup):
    choosing_fitting_line = State()
    choosing_fitting_state = State()

router = Router()

available_options_pprc = ['работает PPR-C', 'ремонт PPR-C', 'остановка для настройки PPR-C']
available_options_pvc = ['работает PVC', 'ремонт PVC', 'остановка для настройки PVC']
available_options_fitting_vodop = ['работает фиттинг водопр', 'ремонт фиттинг водопр', 'остановка для настройки фиттинг водопр']
available_options_fitting_canal = ['работает фиттинг канализ', 'ремонт фиттинг канализ', 'остановка для настройки фиттинг канализ']
available_stanoks = ['1','2','3','4','5','6']


@router.message(Command(commands=["hello"]))
async def hello(message: Message, state: FSMContext):
    await state.clear()
    msg = await message.answer(
                        text="спасибо за ваше сообщение ! ",
                        )
    print(msg)
@router.message(Command(commands=["start"]))
async def cmd_start_3(message: Message, state: FSMContext):
    await state.clear()
    print()
    if (datetime.now()+ timedelta(hours = 6)).hour  in [0, 1,2,3,4,5,6,7, 8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]:
        kb6 = [[KeyboardButton(text='PVC трубa'), KeyboardButton(text='PPR-C трубa'), KeyboardButton(text='Фиттинг водопр'), KeyboardButton(text='Фиттинг канализ'),]]
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
    await message.answer(
                            text="Работает ли сейчас линия PVC трубы ?",
                            reply_markup=make_row_keyboard(available_options_pvc)
                            )
@router.message(Text(text='PPR-C трубa'))
async def working(message: Message, state: FSMContext):
    await message.answer(
                            text="Работает ли сейчас линия PPR-C трубы?",
                            reply_markup=make_row_keyboard(available_options_pprc)
                            )

@router.message(Text(text='Фиттинг водопр'))
async def working(message: Message, state: FSMContext):
    await state.update_data(chosen_type=message.text.lower())
    await message.answer(
                            text="Выберите станок",
                            reply_markup=make_row_keyboard(available_stanoks)
                            )
    await state.set_state(SetParameterFit.choosing_fitting_line)

@router.message(Text(text='Фиттинг канализ'))
async def working(message: Message, state: FSMContext):
    await state.update_data(chosen_type=message.text.lower())
    await message.answer(
                            text="Выберите станок",
                            reply_markup=make_row_keyboard(available_stanoks)
                            )
    await state.set_state(SetParameterFit.choosing_fitting_line)


@router.message(SetParameterFit.choosing_fitting_line,  F.text.in_(available_stanoks))
async def working(message: Message, state: FSMContext):
    await state.update_data(chosen_stanok=message.text.lower())
    user_data = await state.get_data()
    if user_data['chosen_type'] == 'фиттинг водопр':
        await message.answer(
                                text="Работает ли сейчас линия фиттинг трубы?",
                                reply_markup=make_row_keyboard(available_options_fitting_vodop)
                                )
    elif user_data['chosen_type'] == 'фиттинг канализ':
        await message.answer(
                                text="Работает ли сейчас линия фиттинг трубы?",
                                reply_markup=make_row_keyboard(available_options_fitting_canal)
                                )

@router.message(Text(text='ремонт PVC'))
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


@router.message(Text(text='остановка для настройки PVC'))
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

@router.message(Text(text='ремонт PPR-C'))
async def not_working(message: Message, state: FSMContext):
    await state.clear()
    conn = psycopg2.connect(dbname="neondb", user="zhanabayevasset", password="txDhFR1yl8Pi", host='ep-cool-poetry-346809.us-east-2.aws.neon.tech')
    cursor = conn.cursor()
    cursor.execute(f"""insert into pprc_params (working, created_at, updated_at) values (FALSE, current_timestamp + interval'6 hours', current_timestamp + interval'6 hours')""")
    conn.commit()
    cursor.close()
    conn.close()
    await message.answer(
            text="Благодарю за заполненные данные",
            reply_markup=ReplyKeyboardRemove())


@router.message(Text(text='остановка для настройки PPR-C'))
async def not_working(message: Message, state: FSMContext):
    await state.clear()
    conn = psycopg2.connect(dbname="neondb", user="zhanabayevasset", password="txDhFR1yl8Pi", host='ep-cool-poetry-346809.us-east-2.aws.neon.tech')
    cursor = conn.cursor()
    cursor.execute(f"""insert into pprc_params (working, created_at, updated_at) values (FALSE, current_timestamp + interval'6 hours', current_timestamp + interval'6 hours')""")
    conn.commit()
    cursor.close()
    conn.close()
    await message.answer(
            text="Благодарю за заполненные данные",
            reply_markup=ReplyKeyboardRemove())

@router.message(Text(text='ремонт фиттинг водопр'))
async def not_working(message: Message, state: FSMContext):
    
    user_data = await state.get_data()
    
    conn = psycopg2.connect(dbname="neondb", user="zhanabayevasset", password="txDhFR1yl8Pi", host='ep-cool-poetry-346809.us-east-2.aws.neon.tech')
    cursor = conn.cursor()
    cursor.execute(f"""insert into fitting_vodop_params (working, STANOK,created_at, updated_at) values (FALSE, {user_data['chosen_stanok']}, current_timestamp + interval'6 hours', current_timestamp + interval'6 hours')""")
    conn.commit()
    cursor.close()
    conn.close()
    await state.clear()
    await message.answer(
            text="Благодарю за заполненные данные",
            reply_markup=ReplyKeyboardRemove())


@router.message(Text(text='остановка для настройки фиттинг водопр'))
async def not_working(message: Message, state: FSMContext):

    user_data = await state.get_data()
    conn = psycopg2.connect(dbname="neondb", user="zhanabayevasset", password="txDhFR1yl8Pi", host='ep-cool-poetry-346809.us-east-2.aws.neon.tech')
    cursor = conn.cursor()
    cursor.execute(f"""insert into fitting_vodop_params (working, STANOK,created_at, updated_at) values (FALSE, {user_data['chosen_stanok']}, current_timestamp + interval'6 hours', current_timestamp + interval'6 hours')""")
    conn.commit()
    cursor.close()
    conn.close()
    await state.clear()
    await message.answer(
            text="Благодарю за заполненные данные",
            reply_markup=ReplyKeyboardRemove())


@router.message(Text(text='ремонт фиттинг канализ'))
async def not_working(message: Message, state: FSMContext):
    
    user_data = await state.get_data()
    
    conn = psycopg2.connect(dbname="neondb", user="zhanabayevasset", password="txDhFR1yl8Pi", host='ep-cool-poetry-346809.us-east-2.aws.neon.tech')
    cursor = conn.cursor()
    cursor.execute(f"""insert into fitting_canal_params (working, STANOK,created_at, updated_at) values (FALSE, {user_data['chosen_stanok']}, current_timestamp + interval'6 hours', current_timestamp + interval'6 hours')""")
    conn.commit()
    cursor.close()
    conn.close()
    await state.clear()
    await message.answer(
            text="Благодарю за заполненные данные",
            reply_markup=ReplyKeyboardRemove())


@router.message(Text(text='остановка для настройки фиттинг канализ'))
async def not_working(message: Message, state: FSMContext):

    user_data = await state.get_data()
    conn = psycopg2.connect(dbname="neondb", user="zhanabayevasset", password="txDhFR1yl8Pi", host='ep-cool-poetry-346809.us-east-2.aws.neon.tech')
    cursor = conn.cursor()
    cursor.execute(f"""insert into fitting_canal_params (working, STANOK,created_at, updated_at) values (FALSE, {user_data['chosen_stanok']}, current_timestamp + interval'6 hours', current_timestamp + interval'6 hours')""")
    conn.commit()
    cursor.close()
    conn.close()
    await state.clear()
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
