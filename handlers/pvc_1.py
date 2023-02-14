from aiogram import Router, F
from aiogram.filters.command import Command
from aiogram.filters.text import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards.simple_row import make_row_keyboard
from datetime import datetime
import psycopg2

router = Router()


class SetParameter(StatesGroup):
    choosing_pvc_name = State()
    choosing_pvc_tube = State()
    choosing_pvc_nom_diameter = State()
    choosing_pvc_view = State()
    choosing_pvc_functionality = State()
    choosing_pvc_diameter = State()
    choosing_pvc_weight = State()

available_answers = ['ok', 'not ok']
available_names = ['Adlet', 'Arhat']
available_tubes = ['okyanus', 'deniz']
available_diameters = ['50', '70','110','160']

@router.message(Text(text='PVC труба'))
#@router.message(Command(commands=["pvc_3_params"]))
async def pvc_name(message: Message, state: FSMContext):
    await message.answer(
        text="Кто является мастером на линии на текущий час ?",
        reply_markup=make_row_keyboard(available_names)
    )
    await state.set_state(SetParameter.choosing_pvc_name)


@router.message(SetParameter.choosing_pvc_name, F.text.in_(available_names))
async def pvc_tube(message: Message, state: FSMContext):
    await state.update_data(chosen_name=message.text.lower())
    await message.answer(
        text="выберите бренд PVC трубы:",
        reply_markup=make_row_keyboard(available_tubes)
    )
    await state.set_state(SetParameter.choosing_pvc_tube)

@router.message(SetParameter.choosing_pvc_tube, F.text.in_(available_tubes))
async def pvc_nom_diameter(message: Message, state: FSMContext):
    await state.update_data(chosen_tube=message.text.lower())
    await message.answer(
        text="выберите номинальный диаметр PVC трубы:",
        reply_markup=make_row_keyboard(available_diameters)
    )
    await state.set_state(SetParameter.choosing_pvc_nom_diameter)

@router.message(SetParameter.choosing_pvc_nom_diameter, F.text.in_(available_diameters))
async def pvc_view(message: Message, state: FSMContext):
    await state.update_data(chosen_nom_diameter=message.text.lower())
    await message.answer(
        text="оцените внешний вид PVC трубы:",
        reply_markup=make_row_keyboard(available_answers)
    )
    await state.set_state(SetParameter.choosing_pvc_view)

@router.message(SetParameter.choosing_pvc_view, F.text.in_(available_answers))
async def pvc_functionality(message: Message, state: FSMContext):
    await state.update_data(chosen_view=message.text.lower())
    await message.answer(
        text="оцените функциональность PVC трубы:",
        reply_markup=make_row_keyboard(available_answers)
    )
    await state.set_state(SetParameter.choosing_pvc_functionality)

@router.message(SetParameter.choosing_pvc_functionality, F.text.in_(available_answers)) #F.text.in_(available_food_names))
async def pvc_diameter(message: Message, state: FSMContext):
    await state.update_data(chosen_functionality=message.text.lower())
    await message.answer(
        text="Теперь укажите диаметр PVC трубы:",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(SetParameter.choosing_pvc_diameter)

# @router.message(SetParameter.choosing_pvc_functionality)
# async def pvc_diameter_chosen_incorrectly(message: Message):
#     await message.answer(
#         text="Я не знаю такого диаметра.\n\n"
#              "Пожалуйста, выберите значение между 40 и 170 мм",
#     )

@router.message(SetParameter.choosing_pvc_diameter) #F.text.in_(available_food_names))
async def pvc_weight(message: Message, state: FSMContext):
    await state.update_data(chosen_diameter=message.text.lower())
    await message.answer(
        text="Теперь укажите вес PVC трубы:",
    )
    await state.set_state(SetParameter.choosing_pvc_weight)

# @router.message(SetParameter.choosing_pvc_diameter)
# async def pvc_weight_chosen_incorrectly(message: Message):
#     await message.answer(
#         text="Я не знаю такого веса.\n\n"
#              "Пожалуйста, выберите значение между 0.05 и 4.50 гр",
#     )

@router.message(SetParameter.choosing_pvc_weight)
async def pvc_chosen_1(message: Message, state: FSMContext):
    user_data = await state.get_data()
    #await message.answer(text=" ".join([str(i[1]) for i in user_data.items()]) + " " + message.text.lower())
    await state.clear()
    conn = psycopg2.connect(dbname="neondb", user="zhanabayevasset", password="txDhFR1yl8Pi", host='ep-cool-poetry-346809.us-east-2.aws.neon.tech')
    cursor = conn.cursor()
    cursor.execute(f"""insert into pvc_params (BRAND, NOMINAL_DIAMETER, VIEW, FUNCTIONALITY, DIAMETER, WEIGHT, MASTER, created_at, updated_at) values ( '{user_data['chosen_tube']}', '{user_data['chosen_nom_diameter']}','{user_data['chosen_view']}', '{user_data['chosen_functionality']}', {user_data['chosen_diameter']}, {message.text.lower()}, '{user_data['chosen_name']}', current_timestamp, current_timestamp)""")
    conn.commit()
    cursor.close()
    conn.close()

  