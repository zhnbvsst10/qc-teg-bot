from aiogram import Router, F
from aiogram.filters.command import Command
from aiogram.filters.text import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards.simple_row import make_row_keyboard, make_row_keyboard_2
from datetime import datetime, timedelta
from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton,ReplyKeyboardBuilder
import psycopg2


router = Router()
available_answers = ['ok', 'not ok']
available_shifts = ['A','B','C']
available_controllers = ['Madi', 'Zhanibek', 'Magzhan']
available_masters_fitting = ['Salamat', 'Dauren', 'Anton']
available_tubes = ['okyanus', 'deniz','kavi']
available_diameters = ['600']
available_proceeds = ['yes']
available_stanoks = ['1','2','3','4','5','6']


class SetParameterFitOther(StatesGroup):
    choosing_fitting_type = State()
    choosing_fitting_controller = State()
    choosing_fitting_smena = State()
    choosing_fitting_line = State()
    choosing_fitting_name = State()
    choosing_tube_name = State()
    choosing_fitting_tube_1 = State()
    choosing_fitting_tube_2 = State()
    choosing_fitting_tube_3 = State()
    choosing_fitting_tube_4 = State()
    choosing_fitting_tube_5 = State()
    choosing_fitting_nom_diameter = State()
    choosing_fitting_view = State()
    choosing_fitting_functionality = State()
    choosing_fitting_finish = State()
    send_photo = State()

@router.message(Text(text='работает фиттинг канализ'))
async def fitting_controller(message: Message, state: FSMContext):
    
    await message.answer(
        text="Выберите контроллера",
        reply_markup=make_row_keyboard(available_controllers)
    )
    print('choose controller canal')
    await state.set_state(SetParameterFitOther.choosing_fitting_controller)

@router.message(SetParameterFitOther.choosing_fitting_controller)
async def fitting_smena(message: Message, state: FSMContext):
    await state.update_data(chosen_controller_name=message.text.lower())
    await message.answer(
        text="Выберите смену ",
        reply_markup=make_row_keyboard(available_shifts)
    )
    print('choose smena canal')
    await state.set_state(SetParameterFitOther.choosing_fitting_smena)


@router.message(SetParameterFitOther.choosing_fitting_smena)
async def pprc_name(message: Message, state: FSMContext):
    await state.update_data(chosen_smena=message.text.lower())
    await message.answer(
        text="Кто является мастером на линии на текущий час ?",
        reply_markup=make_row_keyboard(available_masters_fitting)
    )
    print('choose master canal')
    await state.set_state(SetParameterFitOther.choosing_fitting_name)


@router.message(SetParameterFitOther.choosing_fitting_name, F.text.in_(available_masters_fitting))
async def pprc_tube(message: Message, state: FSMContext):
    await state.update_data(chosen_name=message.text.lower())
    await message.answer(
        text="Выберите бренд фиттинга:",
        reply_markup=make_row_keyboard(available_tubes)
    )
    print('choose brand canal')
    await state.set_state(SetParameterFitOther.choosing_fitting_tube_1)

@router.message(SetParameterFitOther.choosing_fitting_tube_1)
async def pprc_tube(message: Message, state: FSMContext):
    button1 = KeyboardButton(text='Заглушка к подоконнику  ')

        
    markup1 = ReplyKeyboardBuilder([[button1]]).as_markup()
    await state.update_data(chosen_tube=message.text.lower())
    await message.answer(
        text='Выберите наименование продукции',
        reply_markup=markup1
    )
    print('choose fit name 1 canal ')
    await state.set_state(SetParameterFitOther.choosing_fitting_tube_2)


@router.message(SetParameterFitOther.choosing_fitting_tube_2)
async def pprc_tube(message: Message, state: FSMContext):

    button1 = KeyboardButton(text='600')



    markup1 = ReplyKeyboardBuilder([[button1]]).as_markup()
    await state.update_data(chosen_fit_name_1=message.text.lower())
    await message.answer(
        text='Выберите размер',
        reply_markup=markup1
    )
    print('choose fit name 3')
    await state.set_state(SetParameterFitOther.choosing_fitting_tube_3)

@router.message(SetParameterFitOther.choosing_fitting_tube_3)
async def pprc_tube(message: Message, state: FSMContext):

    button1 = KeyboardButton(text='антрацит')
    button2 = KeyboardButton(text='белый')
    button3 = KeyboardButton(text='зол дуб')
    button4 = KeyboardButton(text='махагон')
    button5 = KeyboardButton(text='мор дую')

   


    markup1 = ReplyKeyboardBuilder([[button1]]).row(button2).row(button3).row(button4).row(button5).as_markup()
    await state.update_data(chosen_fit_name_2=message.text.lower())
    await message.answer(
        text='Выберите цвет',
        reply_markup=markup1
    )
    print('choose fit name 3')
    await state.set_state(SetParameterFitOther.choosing_fitting_tube_4)



@router.message(SetParameterFitOther.choosing_fitting_tube_4)
async def pprc_nom_diameter(message: Message, state: FSMContext):
    await state.update_data(chosen_fit_name_4=message.text.lower())
    await message.answer(
        text="выберите номинальный диаметр фиттинга:",
        reply_markup=make_row_keyboard(available_diameters)
    )
    print('choose nom diameter')
    await state.set_state(SetParameterFitOther.choosing_fitting_nom_diameter)

@router.message(SetParameterFitOther.choosing_fitting_nom_diameter, F.text.in_(available_diameters))
async def pprc_view(message: Message, state: FSMContext):
    await state.update_data(chosen_nom_diameter=message.text.lower())
    await message.answer(
        text="оцените внешний вид фиттинга:",
        reply_markup=make_row_keyboard(available_answers)
    )
    print('choose view')
    await state.set_state(SetParameterFitOther.choosing_fitting_view)

@router.message(SetParameterFitOther.choosing_fitting_view, F.text.in_(available_answers))
async def pprc_functionality(message: Message, state: FSMContext):
    await state.update_data(chosen_view=message.text.lower())
    await message.answer(
        text="оцените функциональность фиттинга:",
        reply_markup=make_row_keyboard(available_answers)
    )
    print('choose func')
    await state.set_state(SetParameterFitOther.choosing_fitting_functionality)

@router.message(SetParameterFitOther.choosing_fitting_functionality)
async def pprc_finish(message: Message, state: FSMContext):
    await state.update_data(chosen_functionality=message.text.lower())
    await message.answer(
            text="перейти к передаче данных",
            reply_markup=make_row_keyboard(available_proceeds)
    )
    await state.set_state(SetParameterFitOther.choosing_fitting_finish)


@router.message(SetParameterFitOther.choosing_fitting_finish, F.text.in_(available_proceeds))
async def fitting_chosen(message: Message, state: FSMContext):
   
    user_data = await state.get_data()
    await message.answer(text=" ".join([str(i[1]) for i in user_data.items()]) + " " + message.text.lower())
    await state.clear()
    await message.answer(
            text="Благодарю за заполненные данные. Отправьте фото подтверждение",
            reply_markup=ReplyKeyboardRemove()
    )
    print('success fitting')

    user_data['chosen_fit_name'] = user_data['chosen_fit_name_1'] + ' ' + user_data['chosen_fit_name_2'] + ' ' + user_data['chosen_fit_name_3'] + ' ' + user_data['chosen_fit_name_4'] 
    conn = psycopg2.connect(dbname="neondb", user="zhanabayevasset", password="txDhFR1yl8Pi", host='ep-cool-poetry-346809.us-east-2.aws.neon.tech')
    cursor = conn.cursor()
    cursor.execute(f"""insert into fitting_canal_params (WORKING,CONTROLLER_NAME,  STANOK,SHIFT, FITTING_NAME, BRAND, NOMINAL_SIZE, VIEW, FUNCTIONALITY, MASTER, created_at, updated_at,COLOR values (TRUE,'{user_data['chosen_controller_name']}', '{user_data['chosen_stanok']}','{user_data['chosen_smena']}', '{user_data['chosen_fit_name']}',  '{user_data['chosen_tube']}', '{user_data['chosen_nom_diameter']}', '{user_data['chosen_view']}','{user_data['chosen_functionality']}',  '{user_data['chosen_name']}',  current_timestamp + interval'6 hours', current_timestamp + interval'6 hours',  '{user_data['chosen_fit_name_4']}')""")
    conn.commit()
    cursor.close()
    conn.close()
    await state.set_state(SetParameterFitOther.send_photo)
