from aiogram import Router, F
from aiogram.filters.command import Command
from aiogram.filters.text import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards.simple_row import make_row_keyboard
from datetime import datetime, timedelta
import psycopg2


router2 = Router()
available_answers = ['ok', 'not ok','back']
available_shifts = ['A','B','C']
available_controllers = ['Madi', 'Zhanibek', 'Magzhan']
available_names = ['Omirserik', 'Aziz', 'Kamil','back']
available_tubes = ['okyanus/1.8', 'deniz type 1/4.0', 'deniz type 1/3.2', 'deniz type 2/2.2','back']
available_diameters = ['50', '70','110','160','back']
available_proceeds = ['yes','back']


class SetParameterPVC3(StatesGroup):
    choosing_pvc_type = State()
    choosing_pvc_controller = State()
    choosing_pvc_smena = State()
    choosing_pvc_name = State()
    choosing_pvc_tube = State()
    choosing_pvc_nom_diameter = State()
    choosing_pvc_view = State()
    choosing_pvc_functionality = State()
    choosing_pvc_diameter = State()
    choosing_pvc_weight = State()
    choosing_pvc_width = State()
    choosing_pvc_control_mark = State()
    choosing_pvc_length = State()
    choosing_pvc_proch = State()
    choosing_pvc_finish = State()
    send_photo = State()

@router2.message(Text(text='работает PVC'))
async def pvc_controller(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Выберите контроллера",
        reply_markup=make_row_keyboard(available_controllers)
    )
    print('choose controller')
    await state.set_state(SetParameterPVC3.choosing_pvc_controller)

@router2.message(SetParameterPVC3.choosing_pvc_controller)
async def pvc_smena(message: Message, state: FSMContext):
    if message.text == 'go':
        await message.answer(
            text="Выберите смену ",
            reply_markup=make_row_keyboard(available_shifts)
        )
        print('choose smena canal')
        await state.set_state(SetParameterPVC3.choosing_pvc_smena)
    else:

        await state.update_data(chosen_controller_name=message.text.lower())
        await message.answer(
            text="Выберите смену ",
            reply_markup=make_row_keyboard(available_shifts)
        )
        print('choose smena')
        await state.set_state(SetParameterPVC3.choosing_pvc_smena)

@router2.message(SetParameterPVC3.choosing_pvc_smena)
async def pvc_name(message: Message, state: FSMContext):
    if message.text == 'back':
        await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
        await state.set_state(SetParameterPVC3.choosing_pvc_controller)
    elif message.text == 'go':
        await message.answer(
            text="Кто является мастером на линии на текущий час ?",
            reply_markup=make_row_keyboard(available_names)
        )
        print('choose master')
        await state.set_state(SetParameterPVC3.choosing_pvc_name)
    else:
        await state.update_data(chosen_smena=message.text.lower())
        await message.answer(
            text="Кто является мастером на линии на текущий час ?",
            reply_markup=make_row_keyboard(available_names)
        )
        print('choose master')
        await state.set_state(SetParameterPVC3.choosing_pvc_name)


@router2.message(SetParameterPVC3.choosing_pvc_name)
async def pvc_tube(message: Message, state: FSMContext):
    if message.text == 'back':
        await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
        await state.set_state(SetParameterPVC3.choosing_pvc_controller)
    elif message.text == 'go':
        await message.answer(
            text="выберите бренд PVC трубы:",
            reply_markup=make_row_keyboard(available_tubes)
        )
        print('choose brand')
        await state.set_state(SetParameterPVC3.choosing_pvc_tube)
    else:
        await state.update_data(chosen_name=message.text.lower())
        await message.answer(
            text="выберите бренд PVC трубы:",
            reply_markup=make_row_keyboard(available_tubes)
        )
        print('choose brand')
        await state.set_state(SetParameterPVC3.choosing_pvc_tube)


@router2.message(SetParameterPVC3.choosing_pvc_tube)
async def pvc_nom_diameter(message: Message, state: FSMContext):
    if message.text == 'back':
        await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
        await state.set_state(SetParameterPVC3.choosing_pvc_smena)
    elif message.text == 'go':
        await message.answer(
            text="выберите номинальный диаметр PVC трубы:",
            reply_markup=make_row_keyboard(available_diameters)
        )
        print('choose nom diameter')
        await state.set_state(SetParameterPVC3.choosing_pvc_nom_diameter)
    else:
        await state.update_data(chosen_tube=message.text.lower())
        await message.answer(
            text="выберите номинальный диаметр PVC трубы:",
            reply_markup=make_row_keyboard(available_diameters)
        )
        print('choose nom diameter')
        await state.set_state(SetParameterPVC3.choosing_pvc_nom_diameter)

@router2.message(SetParameterPVC3.choosing_pvc_nom_diameter)
async def pvc_view(message: Message, state: FSMContext):
    if message.text == 'back':
        await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
        await state.set_state(SetParameterPVC3.choosing_pvc_name)
    elif message.text == 'go':
        await message.answer(
            text="оцените внешний вид PVC трубы:",
            reply_markup=make_row_keyboard(available_answers)
        )
        print('choose view')
        await state.set_state(SetParameterPVC3.choosing_pvc_view)
    else:
        await state.update_data(chosen_nom_diameter=message.text.lower())
        await message.answer(
            text="оцените внешний вид PVC трубы:",
            reply_markup=make_row_keyboard(available_answers)
        )
        print('choose view')
        await state.set_state(SetParameterPVC3.choosing_pvc_view)


@router2.message(SetParameterPVC3.choosing_pvc_view)
async def pvc_functionality(message: Message, state: FSMContext):
    if message.text == 'back':
        await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
        await state.set_state(SetParameterPVC3.choosing_pvc_tube)
    elif message.text == 'go':
        await message.answer(
            text="оцените функциональность PVC трубы:",
            reply_markup=make_row_keyboard(available_answers)
        )
        print('choose functionality')
        await state.set_state(SetParameterPVC3.choosing_pvc_functionality)
    else:
        await state.update_data(chosen_view=message.text.lower())
        await message.answer(
            text="оцените функциональность PVC трубы:",
            reply_markup=make_row_keyboard(available_answers)
        )
        print('choose functionality')
        await state.set_state(SetParameterPVC3.choosing_pvc_functionality)


@router2.message(SetParameterPVC3.choosing_pvc_functionality) #F.text.in_(available_food_names))
async def pvc_diameter(message: Message, state: FSMContext):
    if message.text == 'back':
        await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
        await state.set_state(SetParameterPVC3.choosing_pvc_nom_diameter)
    elif message.text == 'go':
        await message.answer(
            text="Теперь укажите диаметр PVC трубы:",
            reply_markup=ReplyKeyboardRemove()
        )
        print('choose diameter')
        await state.set_state(SetParameterPVC3.choosing_pvc_diameter)
    else:
        await state.update_data(chosen_functionality=message.text.lower())
        await message.answer(
            text="Теперь укажите диаметр PVC трубы:",
            reply_markup=ReplyKeyboardRemove()
        )
        print('choose diameter')
        await state.set_state(SetParameterPVC3.choosing_pvc_diameter)

@router2.message(SetParameterPVC3.choosing_pvc_diameter) #F.text.in_(available_food_names))
async def pvc_weight(message: Message, state: FSMContext):
    if message.text == 'back':
        await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
        await state.set_state(SetParameterPVC3.choosing_pvc_view)
    elif message.text =='go':
        await message.answer(
            text="Теперь укажите вес PVC трубы:",
            reply_markup=ReplyKeyboardRemove()
        )
        print('choose weight')
        await state.set_state(SetParameterPVC3.choosing_pvc_weight)
    else:
        await state.update_data(chosen_diameter=message.text.lower().replace(',', '.'))
        await message.answer(
            text="Теперь укажите вес PVC трубы:",
            reply_markup=ReplyKeyboardRemove()
        )
        print('choose weight')
        await state.set_state(SetParameterPVC3.choosing_pvc_weight)


@router2.message(SetParameterPVC3.choosing_pvc_weight) #F.text.in_(available_food_names))
async def pvc_width(message: Message, state: FSMContext):
    if (datetime.now()+ timedelta(hours = 6)).hour in [2,5,8,11,14,17,20,23]:
        if message.text == 'back':
            await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
            await state.set_state(SetParameterPVC3.choosing_pvc_functionality)
        elif message.text == 'go':
            await message.answer(
                    text="Теперь укажите толщину PVC трубы:",
                    reply_markup=ReplyKeyboardRemove()
            )
            print('choose width')
            await state.set_state(SetParameterPVC3.choosing_pvc_width)
        else:
            await state.update_data(chosen_weight=message.text.lower().replace(',', '.'))
            await message.answer(
                    text="Теперь укажите толщину PVC трубы:",
                    reply_markup=ReplyKeyboardRemove()
            )
            print('choose width')
            await state.set_state(SetParameterPVC3.choosing_pvc_width)
    elif (datetime.now()+ timedelta(hours = 6)).hour in [0,1,3,4,6,7,9,10,12,13,15,16,18,19,21,22]:
        if message.text == 'back':
            await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
            await state.set_state(SetParameterPVC3.choosing_pvc_functionality)
        elif message.text == 'go':
            await message.answer(
                    text="перейти к передаче данных",
                    reply_markup=make_row_keyboard(available_proceeds)
            )
            await state.set_state(SetParameterPVC3.choosing_pvc_finish)
        else:
            await state.update_data(chosen_weight=message.text.lower().replace(',', '.'))
            await message.answer(
                    text="перейти к передаче данных",
                    reply_markup=make_row_keyboard(available_proceeds)
            )
            await state.set_state(SetParameterPVC3.choosing_pvc_finish)
    else:
        await message.answer(
            text="В данный момент работы не ведутся",
            reply_markup=ReplyKeyboardRemove()
        )
@router2.message(SetParameterPVC3.choosing_pvc_width) #F.text.in_(available_food_names))
async def pvc_control_mark(message: Message, state: FSMContext):
    if message.text == 'back':
            await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
            await state.set_state(SetParameterPVC3.choosing_pvc_diameter)
    elif message.text == 'go':
        await message.answer(
                text="оцените контрольную маркировку PVC трубы:",
                reply_markup=make_row_keyboard(available_answers)
        )
        print('choose control mark')
        await state.set_state(SetParameterPVC3.choosing_pvc_control_mark)
    else:
        await state.update_data(chosen_width=message.text.lower().replace(',', '.'))
        await message.answer(
                text="оцените контрольную маркировку PVC трубы:",
                reply_markup=make_row_keyboard(available_answers)
        )
        print('choose control mark')
        await state.set_state(SetParameterPVC3.choosing_pvc_control_mark)
    
@router2.message(SetParameterPVC3.choosing_pvc_control_mark) #F.text.in_(available_food_names))
async def pvc_length(message: Message, state: FSMContext):
    if message.text == 'back':
            await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
            await state.set_state(SetParameterPVC3.choosing_pvc_weight)
    elif message.text == 'go':
        await message.answer(
                text="Теперь укажите длину PVC трубы:",
                reply_markup=ReplyKeyboardRemove()
        )
        print('choose length')
        await state.set_state(SetParameterPVC3.choosing_pvc_length)
    else:
        await state.update_data(chosen_control_mark=message.text.lower())
        await message.answer(
                text="Теперь укажите длину PVC трубы:",
                reply_markup=ReplyKeyboardRemove()
        )
        print('choose length')
        await state.set_state(SetParameterPVC3.choosing_pvc_length)

@router2.message(SetParameterPVC3.choosing_pvc_length) 
async def pvc_proch(message: Message, state: FSMContext):
    if message.text == 'back':
            await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
            await state.set_state(SetParameterPVC3.choosing_pvc_width)
    elif message.text == 'go':
        await message.answer(
                text="оцените прочность PVC трубы:",
                reply_markup=make_row_keyboard(available_answers)
        )
        print('choose prochnost')
        await state.set_state(SetParameterPVC3.choosing_pvc_proch)
    else:
        await state.update_data(chosen_length=message.text.lower().replace(',', '.'))
        await message.answer(
                text="оцените прочность PVC трубы:",
                reply_markup=make_row_keyboard(available_answers)
        )
        print('choose prochnost')
        await state.set_state(SetParameterPVC3.choosing_pvc_proch)

@router2.message(SetParameterPVC3.choosing_pvc_proch)
async def pvc_finish(message: Message, state: FSMContext):
    if (datetime.now()+ timedelta(hours = 6)).hour in [2,5,8,11,14,17,20,23]:
        if message.text == 'back':
            await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
            await state.set_state(SetParameterPVC3.choosing_pvc_control_mark)
        elif message.text == 'go':
            await message.answer(
                text="перейти к передаче данных",
                reply_markup=make_row_keyboard(available_proceeds)
            )
            await state.set_state(SetParameterPVC3.choosing_pvc_finish)
        else:
            await state.update_data(chosen_proch=message.text.lower())
            await message.answer(
                text="перейти к передаче данных",
                reply_markup=make_row_keyboard(available_proceeds)
            )
            await state.set_state(SetParameterPVC3.choosing_pvc_finish)




@router2.message(SetParameterPVC3.choosing_pvc_finish, F.text.in_(available_proceeds))
async def pvc_chosen(message: Message, state: FSMContext):
    if (datetime.now()+ timedelta(hours = 6)).hour in [2,5,8,11,14,17,20,23]:
        if message.text == 'back':
            await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
            await state.set_state(SetParameterPVC3.choosing_pvc_length)
        else:
            user_data = await state.get_data()
            await message.answer(text=" ".join([str(i[1]) for i in user_data.items()]) + " " + message.text.lower())
            await state.clear()
            await message.answer(
                text="Благодарю за заполненные данные. Отправьте фото подтверждение",
                reply_markup=ReplyKeyboardRemove()
            )
            print('success 6 params')
            conn = psycopg2.connect(dbname="neondb", user="zhanabayevasset", password="txDhFR1yl8Pi", host='ep-cool-poetry-346809.us-east-2.aws.neon.tech')
            cursor = conn.cursor()
            cursor.execute(f"""insert into pvc_params (WORKING,CONTROLLER_NAME, SHIFT, BRAND, NOMINAL_DIAMETER, VIEW, FUNCTIONALITY, DIAMETER, WEIGHT,WIDTH,MARK_CONTROL,LENGTH,STRENGTH, MASTER, created_at, updated_at) values (TRUE,'{user_data['chosen_controller_name']}','{user_data['chosen_smena']}','{user_data['chosen_tube']}', '{user_data['chosen_nom_diameter']}', '{user_data['chosen_view']}','{user_data['chosen_functionality']}',{user_data['chosen_diameter']}, {user_data['chosen_weight']}, {user_data['chosen_width']}, '{user_data['chosen_control_mark']}', '{user_data['chosen_length']}', '{user_data['chosen_proch']}','{user_data['chosen_name']}',  current_timestamp + interval'6 hours', current_timestamp + interval'6 hours')""")
            conn.commit()
            cursor.close()
            conn.close()
            await state.set_state(SetParameterPVC3.send_photo)
    elif (datetime.now()+ timedelta(hours = 6)).hour in [0,1,3,4,6,7,9,10,12,13,15,16,18,19,21,22]:
        if message.text == 'back':
            await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
            await state.set_state(SetParameterPVC3.choosing_pvc_diameter)
        else:

            print('sucess 3 params')
            user_data = await state.get_data()
            # await state.clear()
            await message.answer(
                text="Благодарю за заполненные данные. Отправьте фото подтверждение",
                reply_markup=ReplyKeyboardRemove()
            )
            
            conn = psycopg2.connect(dbname="neondb", user="zhanabayevasset", password="txDhFR1yl8Pi", host='ep-cool-poetry-346809.us-east-2.aws.neon.tech')
            cursor = conn.cursor()
            cursor.execute(f"""insert into pvc_params (WORKING,CONTROLLER_NAME, SHIFT, BRAND, NOMINAL_DIAMETER, VIEW, FUNCTIONALITY, DIAMETER, WEIGHT, MASTER, created_at, updated_at) values (TRUE, '{user_data['chosen_controller_name']}','{user_data['chosen_smena']}', '{user_data['chosen_tube']}', '{user_data['chosen_nom_diameter']}','{user_data['chosen_view']}', '{user_data['chosen_functionality']}', {user_data['chosen_diameter']},  {user_data['chosen_weight']}, '{user_data['chosen_name']}', current_timestamp + interval'6 hours', current_timestamp + interval'6 hours')""")
            conn.commit()
            cursor.close()
            conn.close()
            await state.set_state(SetParameterPVC3.send_photo)
    else:
        await message.answer(
            text="В данный момент работы не ведутся",
            reply_markup=ReplyKeyboardRemove()
        )
