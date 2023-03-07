from aiogram import Router, F
from aiogram.filters.command import Command
from aiogram.filters.text import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards.simple_row import make_row_keyboard
from datetime import datetime, timedelta
import psycopg2


router = Router()
available_answers = ['ok', 'not ok']
available_shifts = ['A','B','C']
available_controllers = ['Madi', 'Zhanibek', 'Magzhan']
available_masters_fitting = ['Salamat', 'Dauren', 'Anton']
available_tubes = ['okyanus', 'deniz']
available_diameters = ['50','110']
available_proceeds = ['yes']


class SetParameterFit(StatesGroup):
    choosing_fitting_type = State()
    choosing_fitting_controller = State()
    choosing_fitting_smena = State()
    choosing_fitting_name = State()
    choosing_fitting_tube = State()
    choosing_fitting_nom_diameter = State()
    choosing_fitting_view = State()
    choosing_fitting_functionality = State()
    choosing_fitting_finish = State()

@router.message(Text(text='работает фиттинг'))
async def fitting_controller(message: Message, state: FSMContext):
    await message.answer(
        text="Введите ФИО контроллера",
        reply_markup=make_row_keyboard(available_controllers)
    )
    print('choose controller')
    await state.set_state(SetParameterFit.choosing_fitting_controller)

@router.message(SetParameterFit.choosing_fitting_controller)
async def fitting_smena(message: Message, state: FSMContext):
    await state.update_data(chosen_controller_name=message.text.lower())
    await message.answer(
        text="Выберите смену ",
        reply_markup=make_row_keyboard(available_shifts)
    )
    print('choose smena')
    await state.set_state(SetParameterFit.choosing_fitting_smena)

@router.message(SetParameterFit.choosing_fitting_smena)
async def pprc_name(message: Message, state: FSMContext):
    await state.update_data(chosen_smena=message.text.lower())
    await message.answer(
        text="Кто является мастером на линии на текущий час ?",
        reply_markup=make_row_keyboard(available_masters_fitting)
    )
    print('choose master')
    await state.set_state(SetParameterFit.choosing_fitting_name)


@router.message(SetParameterFit.choosing_fitting_name, F.text.in_(available_masters_fitting))
async def pprc_tube(message: Message, state: FSMContext):
    await state.update_data(chosen_name=message.text.lower())
    await message.answer(
        text="выберите бренд фиттинга:",
        reply_markup=make_row_keyboard(available_tubes)
    )
    print('choose brand')
    await state.set_state(SetParameterFit.choosing_fitting_tube)

@router.message(SetParameterFit.choosing_fitting_tube, F.text.in_(available_tubes))
async def pprc_nom_diameter(message: Message, state: FSMContext):
    await state.update_data(chosen_tube=message.text.lower())
    await message.answer(
        text="выберите номинальный диаметр фиттинга:",
        reply_markup=make_row_keyboard(available_diameters)
    )
    print('choose nom diameter')
    await state.set_state(SetParameterFit.choosing_fitting_nom_diameter)

@router.message(SetParameterFit.choosing_fitting_nom_diameter, F.text.in_(available_diameters))
async def pprc_view(message: Message, state: FSMContext):
    await state.update_data(chosen_nom_diameter=message.text.lower())
    await message.answer(
        text="оцените внешний вид фиттинга:",
        reply_markup=make_row_keyboard(available_answers)
    )
    print('choose view')
    await state.set_state(SetParameterFit.choosing_fitting_view)

@router.message(SetParameterFit.choosing_fitting_view, F.text.in_(available_answers))
async def pprc_functionality(message: Message, state: FSMContext):
    await state.update_data(chosen_view=message.text.lower())
    await message.answer(
        text="оцените внешний функциональность фиттинга:",
        reply_markup=make_row_keyboard(available_answers)
    )
    print('choose view')
    await state.set_state(SetParameterFit.choosing_fitting_functionality)

@router.message(SetParameterFit.choosing_fitting_functionality)
async def pprc_finish(message: Message, state: FSMContext):
    await state.update_data(chosen_functionality=message.text.lower())
    await message.answer(
            text="перейти к передаче данных",
            reply_markup=make_row_keyboard(available_proceeds)
    )
    await state.set_state(SetParameterFit.choosing_fitting_finish)


@router.message(SetParameterFit.choosing_fitting_finish, F.text.in_(available_proceeds))
async def fitting_chosen(message: Message, state: FSMContext):
   
    user_data = await state.get_data()
        #await message.answer(text=" ".join([str(i[1]) for i in user_data.items()]) + " " + message.text.lower())
    await state.clear()
    await message.answer(
            text="Благодарю за заполненные данные. Отправьте фото подтверждение",
            reply_markup=ReplyKeyboardRemove()
    )
    print('success fitting')
    conn = psycopg2.connect(dbname="neondb", user="zhanabayevasset", password="txDhFR1yl8Pi", host='ep-cool-poetry-346809.us-east-2.aws.neon.tech')
    cursor = conn.cursor()
    cursor.execute(f"""insert into fitting_params (WORKING,CONTROLLER_NAME, SHIFT, BRAND, NOMINAL_DIAMETER, VIEW, FUNCTIONALITY, MASTER, created_at, updated_at) values (TRUE,'{user_data['chosen_controller_name']}','{user_data['chosen_smena']}','{user_data['chosen_tube']}', '{user_data['chosen_nom_diameter']}', '{user_data['chosen_view']}',{user_data['chosen_functionality']},  '{user_data['chosen_name']}',  current_timestamp + interval'6 hours', current_timestamp + interval'6 hours')""")
    conn.commit()
    cursor.close()
    conn.close()