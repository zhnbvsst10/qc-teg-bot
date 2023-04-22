from aiogram import Router,  F
from aiogram.filters.command import Command
from aiogram.filters.text import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, KeyboardButton,ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton,ReplyKeyboardBuilder
from datetime import datetime, timedelta
import psycopg2
from keyboards.simple_row import make_row_keyboard
from aiogram.fsm.state import StatesGroup, State

class SetParameterFit(StatesGroup):
    choosing_fitting_line = State()
    choosing_fitting_state = State()
    state_pprc_renov = State()
    state_pprc_setting = State()
    state_pert_renov = State()
    state_pert_setting = State()
    state_pvc_renov = State()
    state_pvc_setting = State()
    state_fit_vodop_renov = State()
    state_fit_vodop_setting = State()
    state_fit_canal_renov = State()
    state_fit_canal_setting = State()
    state_fit_other_renov = State()
    state_fit_other_setting = State()

router = Router()

available_options_pprc = ['работает PPR-C', 'ремонт PPR-C', 'остановка для настройки PPR-C']
available_options_pvc = ['работает PVC', 'ремонт PVC', 'остановка для настройки PVC']
available_options_fitting_vodop = ['работает фиттинг водопр', 'ремонт фиттинг водопр', 'остановка для настройки фиттинг водопр']
available_options_fitting_canal = ['работает фиттинг канализ', 'ремонт фиттинг канализ', 'остановка для настройки фиттинг канализ']
available_options_fitting_other = ['работает фиттинг др', 'ремонт фиттинг др', 'остановка для настройки фиттинг др']
available_options_pert = ['работает pert', 'ремонт pert', 'остановка для настройки pert']
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
    button1 = KeyboardButton(text='PVC трубa')
    button2 = KeyboardButton(text='PPR-C трубa')
    button3 = KeyboardButton(text='Фиттинг водопр')
    button4 = KeyboardButton(text='Фиттинг др')
    button5 = KeyboardButton(text='Фиттинг канализ')
    button6 = KeyboardButton(text='pert')
    markup1 = ReplyKeyboardBuilder([[button1]]).row(button2).row(button3).row(button4).row(button5).row(button6).as_markup()

    if (datetime.now()+ timedelta(hours = 6)).hour  in [0, 1,2,3,4,5,6,7, 8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]:
        await message.answer(
                        text="Выберите изделие: ",
                        reply_markup=markup1
                        )
    else:
        msg = await message.answer(
                        text="В данный момент работы не ведутся ",
                        )

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
@router.message(Text(text='Фиттинг др'))
async def working(message: Message, state: FSMContext):
    await state.update_data(chosen_type=message.text.lower())
    await message.answer(
                            text="Выберите станок",
                            reply_markup=make_row_keyboard(available_stanoks)
                            )
    await state.set_state(SetParameterFit.choosing_fitting_line)

@router.message(Text(text='pert'))
async def working(message: Message, state: FSMContext):
    await message.answer(
                            text="Работает ли сейчас линия pert?",
                            reply_markup=make_row_keyboard(available_options_pert)
                            )


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
    elif user_data['chosen_type'] == 'фиттинг др':
        await message.answer(
                                text="Работает ли сейчас линия фиттинг трубы?",
                                reply_markup=make_row_keyboard(available_options_fitting_other)
                                )

@router.message(Text(text='ремонт PVC'))
async def not_working(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
            text="введите описание",
            reply_markup=ReplyKeyboardRemove()
            )
    await state.set_state(SetParameterFit.state_pvc_renov)

@router.message(SetParameterFit.state_pvc_renov)
async def not_working(message: Message, state: FSMContext):
    await state.update_data(state_=message.text.lower())
    user_data = await state.get_data()
    conn = psycopg2.connect(dbname="neondb", user="zhanabayevasset", password="txDhFR1yl8Pi", host='ep-cool-poetry-346809.us-east-2.aws.neon.tech')
    cursor = conn.cursor()
    cursor.execute(f"""insert into pvc_params (working, working_descr,created_at, updated_at) values ('ремонт', '{user_data['state_']}',current_timestamp + interval'6 hours', current_timestamp + interval'6 hours')""")
    conn.commit()
    cursor.close()
    conn.close()
    await message.answer(
            text="Благодарю за заполненные данные",
            reply_markup=ReplyKeyboardRemove())


@router.message(Text(text='остановка для настройки PVC'))
async def not_working(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
            text="введите описание",
            reply_markup=ReplyKeyboardRemove()
            
            )
    await state.set_state(SetParameterFit.state_pvc_setting)

@router.message(SetParameterFit.state_pvc_setting)
async def not_working(message: Message, state: FSMContext):
    await state.update_data(state_=message.text.lower())
    user_data = await state.get_data()
    conn = psycopg2.connect(dbname="neondb", user="zhanabayevasset", password="txDhFR1yl8Pi", host='ep-cool-poetry-346809.us-east-2.aws.neon.tech')
    cursor = conn.cursor()
    cursor.execute(f"""insert into pvc_params (working, working_descr, created_at, updated_at) values ('настройка', '{user_data['state_']}', current_timestamp + interval'6 hours', current_timestamp + interval'6 hours')""")
    conn.commit()
    cursor.close()
    conn.close()
    await message.answer(
            text="Благодарю за заполненные данные",
            reply_markup=ReplyKeyboardRemove())


@router.message(Text(text='ремонт pert'))
async def not_working(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
            text="введите описание",
            reply_markup=ReplyKeyboardRemove()
            )
    await state.set_state(SetParameterFit.state_pert_renov)

@router.message(SetParameterFit.state_pert_renov)
async def not_working(message: Message, state: FSMContext):
    await state.update_data(state_=message.text.lower())
    user_data = await state.get_data()
    conn = psycopg2.connect(dbname="neondb", user="zhanabayevasset", password="txDhFR1yl8Pi", host='ep-cool-poetry-346809.us-east-2.aws.neon.tech')
    cursor = conn.cursor()
    cursor.execute(f"""insert into pert_params (working, working_descr, created_at, updated_at) values ('ремонт', '{user_data['state_']}',current_timestamp + interval'6 hours', current_timestamp + interval'6 hours')""")
    conn.commit()
    cursor.close()
    conn.close()
    await message.answer(
            text="Благодарю за заполненные данные",
            reply_markup=ReplyKeyboardRemove())


@router.message(Text(text='остановка для настройки pert'))
async def not_working(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
            text="введите описание",
            reply_markup=ReplyKeyboardRemove()
            )
    await state.set_state(SetParameterFit.state_pert_setting)

@router.message(SetParameterFit.state_pert_setting)
async def not_working(message: Message, state: FSMContext):
    await state.update_data(state_=message.text.lower())
    user_data = await state.get_data()
    conn = psycopg2.connect(dbname="neondb", user="zhanabayevasset", password="txDhFR1yl8Pi", host='ep-cool-poetry-346809.us-east-2.aws.neon.tech')
    cursor = conn.cursor()
    cursor.execute(f"""insert into pert_params (working, working_descr, created_at, updated_at) values ('настройка', '{user_data['state_']}', current_timestamp + interval'6 hours', current_timestamp + interval'6 hours')""")
    conn.commit()
    cursor.close()
    conn.close()
    await message.answer(
            text="Благодарю за заполненные данные",
            reply_markup=ReplyKeyboardRemove())



@router.message(Text(text='ремонт PPR-C'))
async def not_working(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
            text="введите описание",
            reply_markup=ReplyKeyboardRemove()
            )
    await state.set_state(SetParameterFit.state_pprc_renov)

@router.message(SetParameterFit.state_pprc_renov)
async def not_working(message: Message, state: FSMContext):
    await state.update_data(state_=message.text.lower())
    user_data = await state.get_data()
    conn = psycopg2.connect(dbname="neondb", user="zhanabayevasset", password="txDhFR1yl8Pi", host='ep-cool-poetry-346809.us-east-2.aws.neon.tech')
    cursor = conn.cursor()
    cursor.execute(f"""insert into pprc_params (working, working_descr, created_at, updated_at) values ('ремонт', '{user_data['state_']}',current_timestamp + interval'6 hours', current_timestamp + interval'6 hours')""")
    conn.commit()
    cursor.close()
    conn.close()
    await message.answer(
            text="Благодарю за заполненные данные",
            reply_markup=ReplyKeyboardRemove())


@router.message(Text(text='остановка для настройки PPR-C'))
async def not_working(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
            text="введите описание",
            reply_markup=ReplyKeyboardRemove()
            )
    await state.set_state(SetParameterFit.state_pprc_setting)

@router.message(SetParameterFit.state_pprc_setting)
async def not_working(message: Message, state: FSMContext):
    await state.update_data(state_=message.text.lower())
    user_data = await state.get_data()
    conn = psycopg2.connect(dbname="neondb", user="zhanabayevasset", password="txDhFR1yl8Pi", host='ep-cool-poetry-346809.us-east-2.aws.neon.tech')
    cursor = conn.cursor()
    cursor.execute(f"""insert into pprc_params (working, working_descr, created_at, updated_at) values ('настройка', '{user_data['state_']}',current_timestamp + interval'6 hours', current_timestamp + interval'6 hours')""")
    conn.commit()
    cursor.close()
    conn.close()
    await message.answer(
            text="Благодарю за заполненные данные",
            reply_markup=ReplyKeyboardRemove())

@router.message(Text(text='ремонт фиттинг водопр'))
async def not_working(message: Message, state: FSMContext):
    await message.answer(
            text="введите описание",
            reply_markup=ReplyKeyboardRemove()
            )
    await state.set_state(SetParameterFit.state_fit_vodop_renov)

@router.message(SetParameterFit.state_fit_vodop_renov)
async def not_working(message: Message, state: FSMContext):

    await state.update_data(state_=message.text.lower())
    user_data = await state.get_data()
    conn = psycopg2.connect(dbname="neondb", user="zhanabayevasset", password="txDhFR1yl8Pi", host='ep-cool-poetry-346809.us-east-2.aws.neon.tech')
    cursor = conn.cursor()
    cursor.execute(f"""insert into fitting_vodop_params (working,working_descr STANOK,created_at, updated_at) values ('ремонт','{user_data['state_']}', {user_data['chosen_stanok']}, current_timestamp + interval'6 hours', current_timestamp + interval'6 hours')""")
    conn.commit()
    cursor.close()
    conn.close()
    await state.clear()
    await message.answer(
            text="Благодарю за заполненные данные",
            reply_markup=ReplyKeyboardRemove())


@router.message(Text(text='остановка для настройки фиттинг водопр'))
async def not_working(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
            text="введите описание",
            reply_markup=ReplyKeyboardRemove()
            )
    await state.set_state(SetParameterFit.state_fit_vodop_setting)

@router.message(SetParameterFit.state_fit_vodop_setting)
async def not_working(message: Message, state: FSMContext):
    await state.update_data(state_=message.text.lower())
    user_data = await state.get_data()
    conn = psycopg2.connect(dbname="neondb", user="zhanabayevasset", password="txDhFR1yl8Pi", host='ep-cool-poetry-346809.us-east-2.aws.neon.tech')
    cursor = conn.cursor()
    cursor.execute(f"""insert into fitting_vodop_params (working,working_descr,  STANOK,created_at, updated_at) values ('настройка','{user_data['state_']}', {user_data['chosen_stanok']}, current_timestamp + interval'6 hours', current_timestamp + interval'6 hours')""")
    conn.commit()
    cursor.close()
    conn.close()
    await state.clear()
    await message.answer(
            text="Благодарю за заполненные данные",
            reply_markup=ReplyKeyboardRemove())


@router.message(Text(text='ремонт фиттинг канализ'))
async def not_working(message: Message, state: FSMContext):
    await message.answer(
            text="введите описание",
            reply_markup=ReplyKeyboardRemove()
            )
    await state.set_state(SetParameterFit.state_fit_canal_renov)
@router.message(SetParameterFit.state_fit_canal_renov)
async def not_working(message: Message, state: FSMContext):
    
    await state.update_data(state_=message.text.lower())
    user_data = await state.get_data()
    
    conn = psycopg2.connect(dbname="neondb", user="zhanabayevasset", password="txDhFR1yl8Pi", host='ep-cool-poetry-346809.us-east-2.aws.neon.tech')
    cursor = conn.cursor()
    cursor.execute(f"""insert into fitting_canal_params (working,working_descr, STANOK,created_at, updated_at) values ('ремонт','{user_data['state_']}', {user_data['chosen_stanok']}, current_timestamp + interval'6 hours', current_timestamp + interval'6 hours')""")
    conn.commit()
    cursor.close()
    conn.close()
    await state.clear()
    await message.answer(
            text="Благодарю за заполненные данные",
            reply_markup=ReplyKeyboardRemove())


@router.message(Text(text='остановка для настройки фиттинг канализ'))
async def not_working(message: Message, state: FSMContext):

    await message.answer(
            text="введите описание",
            reply_markup=ReplyKeyboardRemove()
            )
    await state.set_state(SetParameterFit.state_fit_canal_setting)
@router.message(SetParameterFit.state_fit_canal_setting)
async def not_working(message: Message, state: FSMContext):
    await state.update_data(state_=message.text.lower())
    user_data = await state.get_data()
    conn = psycopg2.connect(dbname="neondb", user="zhanabayevasset", password="txDhFR1yl8Pi", host='ep-cool-poetry-346809.us-east-2.aws.neon.tech')
    cursor = conn.cursor()
    cursor.execute(f"""insert into fitting_canal_params (working,working_descr, STANOK,created_at, updated_at) values ('настройка', '{user_data['state_']}',{user_data['chosen_stanok']}, current_timestamp + interval'6 hours', current_timestamp + interval'6 hours')""")
    conn.commit()
    cursor.close()
    conn.close()
    await state.clear()
    await message.answer(
            text="Благодарю за заполненные данные",
            reply_markup=ReplyKeyboardRemove())


@router.message(Text(text='ремонт фиттинг др'))
async def not_working(message: Message, state: FSMContext):
    await message.answer(
            text="введите описание",
            reply_markup=ReplyKeyboardRemove()
            )
    await state.set_state(SetParameterFit.state_fit_other_renov)

@router.message(SetParameterFit.state_fit_other_renov)
async def not_working(message: Message, state: FSMContext):
    
    await state.update_data(state_=message.text.lower())
    user_data = await state.get_data()
    
    conn = psycopg2.connect(dbname="neondb", user="zhanabayevasset", password="txDhFR1yl8Pi", host='ep-cool-poetry-346809.us-east-2.aws.neon.tech')
    cursor = conn.cursor()
    cursor.execute(f"""insert into fitting_other_params (working,working_descr,  STANOK,created_at, updated_at) values ('ремонт','{user_data['state_']}', {user_data['chosen_stanok']}, current_timestamp + interval'6 hours', current_timestamp + interval'6 hours')""")
    conn.commit()
    cursor.close()
    conn.close()
    await state.clear()
    await message.answer(
            text="Благодарю за заполненные данные",
            reply_markup=ReplyKeyboardRemove())


@router.message(Text(text='остановка для настройки фиттинг др'))
async def not_working(message: Message, state: FSMContext):
    await message.answer(
            text="введите описание",
            reply_markup=ReplyKeyboardRemove()
            )
    await state.set_state(SetParameterFit.state_fit_other_setting)
@router.message(SetParameterFit.state_fit_other_setting)
async def not_working(message: Message, state: FSMContext):

    await state.update_data(state_=message.text.lower())
    user_data = await state.get_data()
    conn = psycopg2.connect(dbname="neondb", user="zhanabayevasset", password="txDhFR1yl8Pi", host='ep-cool-poetry-346809.us-east-2.aws.neon.tech')
    cursor = conn.cursor()
    cursor.execute(f"""insert into fitting_other_params (working,working_descr,  STANOK,created_at, updated_at) values ('настройка', '{user_data['state_']}', {user_data['chosen_stanok']}, current_timestamp + interval'6 hours', current_timestamp + interval'6 hours')""")
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
