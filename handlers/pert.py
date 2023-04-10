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
available_answers = ['ok', 'not ok']
available_shifts = ['A','B','C']
available_controllers = ['Madi', 'Zhanibek', 'Magzhan']
available_names = ['Talgat','Aibar','Bolat']
available_tubes = ['PE-RT','OxyPE-RT']
available_proceeds = ['yes']


class SetParameterPERT(StatesGroup):
    choosing_pvc_type = State()
    choosing_pvc_controller = State()
    choosing_pvc_smena = State()
    choosing_pvc_name = State()
    choosing_pvc_tube = State()
    choosing_pvc_mark_control = State()
    choosing_pvc_view = State()
    choosing_pvc_weight = State()
    choosing_pvc_width = State()
    choosing_pvc_outer_diam = State()
    choosing_pvc_weight_b = State()
    choosing_pvc_width_s = State()
    choosing_pvc_finish = State()
    choosing_pvc_control_mark = State()
    send_photo = State()

@router2.message(Text(text='работает pert'))
async def pvc_controller(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Выберите контроллера",
        reply_markup=make_row_keyboard(available_controllers)
    )
    print('choose controller')
    await state.set_state(SetParameterPERT.choosing_pvc_controller)

@router2.message(SetParameterPERT.choosing_pvc_controller)
async def pvc_smena(message: Message, state: FSMContext):
    await state.update_data(chosen_controller_name=message.text.lower())
    await message.answer(
        text="Выберите смену ",
        reply_markup=make_row_keyboard(available_shifts)
    )
    print('choose smena')
    await state.set_state(SetParameterPERT.choosing_pvc_smena)

@router2.message(SetParameterPERT.choosing_pvc_smena)
async def pvc_name(message: Message, state: FSMContext):
    await state.update_data(chosen_smena=message.text.lower())
    await message.answer(
        text="Кто является мастером на линии на текущий час ?",
        reply_markup=make_row_keyboard(available_names)
    )
    print('choose master')
    await state.set_state(SetParameterPERT.choosing_pvc_name)


@router2.message(SetParameterPERT.choosing_pvc_name, F.text.in_(available_names))
async def pvc_tube(message: Message, state: FSMContext):
    await state.update_data(chosen_name=message.text.lower())
    await message.answer(
        text="выберите бренд:",
        reply_markup=make_row_keyboard(available_tubes)
    )
    print('choose brand')
    await state.set_state(SetParameterPERT.choosing_pvc_tube)

@router2.message(SetParameterPERT.choosing_pvc_tube, F.text.in_(available_tubes))
async def pvc_tube(message: Message, state: FSMContext):
    await state.update_data(chosen_tube=message.text.lower())
    await message.answer(
        text="оцените внешний вид:",
        reply_markup=make_row_keyboard(available_answers)
    )
    print('choose view')
    await state.set_state(SetParameterPERT.choosing_pvc_view)

@router2.message(SetParameterPERT.choosing_pvc_view)
async def pvc_functionality(message: Message, state: FSMContext):
    await state.update_data(chosen_view=message.text.lower())
    await message.answer(
        text="введите наружний диаметр:",
        reply_markup=ReplyKeyboardRemove()
    )
    print('choose outer_diam')
    await state.set_state(SetParameterPERT.choosing_pvc_outer_diam)

@router2.message(SetParameterPERT.choosing_pvc_outer_diam) #F.text.in_(available_food_names))
async def pvc_diameter(message: Message, state: FSMContext):
    await state.update_data(chosen_outer_diam = message.text.lower())
    await message.answer(
        text="введите толщину стенок:",
        reply_markup=ReplyKeyboardRemove()
    )
    print('choose width stenok')
    await state.set_state(SetParameterPERT.choosing_pvc_width_s)

@router2.message(SetParameterPERT.choosing_pvc_width_s) #F.text.in_(available_food_names))
async def pvc_diameter(message: Message, state: FSMContext):
    await state.update_data(chosen_width_s=message.text.lower())
    await message.answer(
        text="введите вес бухты:",
        reply_markup=ReplyKeyboardRemove()
    )
    print('choose weight b')
    await state.set_state(SetParameterPERT.choosing_pvc_weight_b)



@router2.message(SetParameterPERT.choosing_pvc_weight_b) #F.text.in_(available_food_names))
async def pvc_width(message: Message, state: FSMContext):
    if (datetime.now()+ timedelta(hours = 6)).hour in [2,5,8,11,14,17,20,23]:
        await state.update_data(chosen_weight_b=message.text.lower().replace(',', '.'))
        await message.answer(
            text="Теперь укажите вес:",
            reply_markup=ReplyKeyboardRemove()
        )
        print('choose weight')
        await state.set_state(SetParameterPERT.choosing_pvc_weight)
    elif (datetime.now()+ timedelta(hours = 6)).hour in [0,1,3,4,6,7,9,10,12,13,15,16,18,19,21,22]:
        await state.update_data(chosen_weight_b=message.text.lower().replace(',', '.'))
        await message.answer(
                 text="перейти к передаче данных",
                 reply_markup=make_row_keyboard(available_proceeds)
         )
        await state.set_state(SetParameterPERT.choosing_pvc_finish)
    else:
        await message.answer(
            text="В данный момент работы не ведутся",
            reply_markup=ReplyKeyboardRemove()
        )
@router2.message(SetParameterPERT.choosing_pvc_weight) #F.text.in_(available_food_names))
async def pvc_control_mark(message: Message, state: FSMContext):
    await state.update_data(chosen_weight=message.text.lower().replace(',', '.'))
    await message.answer(
            text="оцените контрольную маркировку:",
            reply_markup=make_row_keyboard(available_answers)
    )
    print('choose control mark')
    await state.set_state(SetParameterPERT.choosing_pvc_control_mark)
    
@router2.message(SetParameterPERT.choosing_pvc_control_mark) #F.text.in_(available_food_names))
async def pvc_length(message: Message, state: FSMContext):
    await state.update_data(chosen_control_mark=message.text.lower())
    await message.answer(
            text="перейти к передаче данных",
            reply_markup=make_row_keyboard(available_proceeds)
        )
    await state.set_state(SetParameterPERT.choosing_pvc_finish)






@router2.message(SetParameterPERT.choosing_pvc_finish, F.text.in_(available_proceeds))
async def pvc_chosen(message: Message, state: FSMContext):
    if (datetime.now()+ timedelta(hours = 6)).hour in [2,5,8,11,14,17,20,23]:
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
        cursor.execute(f"""insert into pert_params (WORKING,CONTROLLER_NAME, SHIFT, BRAND, VIEW, 
                                                    OUTER_DIAMETER, WIDTH_ST, WEIGHT_B, WEIGHT, MARK_CONTROL,
                                                     MASTER, created_at, updated_at) values 
                                                (TRUE,'{user_data['chosen_controller_name']}','{user_data['chosen_smena']}','{user_data['chosen_tube']}',  
                                                            '{user_data['chosen_view']}','{user_data['choosing_outer_diam']}',{user_data['chosen_width_s']}, 
                                                            {user_data['chosen_weight_b']}, {user_data['chosen_weight']}, '{user_data['chosen_control_mark']}', '{user_data['chosen_name']}',
                                                              current_timestamp + interval'6 hours', current_timestamp + interval'6 hours')""")
        conn.commit()
        cursor.close()
        conn.close()
        await state.set_state(SetParameterPERT.send_photo)
    elif (datetime.now()+ timedelta(hours = 6)).hour in [0,1,3,4,6,7,9,10,12,13,15,16,18,19,21,22]:
        print('sucess 3 params')
        user_data = await state.get_data()
        # await state.clear()
        await message.answer(
            text="Благодарю за заполненные данные. Отправьте фото подтверждение",
            reply_markup=ReplyKeyboardRemove()
        )
        
        conn = psycopg2.connect(dbname="neondb", user="zhanabayevasset", password="txDhFR1yl8Pi", host='ep-cool-poetry-346809.us-east-2.aws.neon.tech')
        cursor = conn.cursor()
        cursor.execute(f"""insert into pert_params (WORKING,CONTROLLER_NAME, SHIFT, BRAND, VIEW, 
                                                    OUTER_DIAMETER, WIDTH_ST, WEIGHT_B, 
                                                     MASTER, created_at, updated_at) values 
                                                (TRUE,'{user_data['chosen_controller_name']}','{user_data['chosen_smena']}','{user_data['chosen_tube']}',  
                                                            '{user_data['chosen_view']}','{user_data['choosing_outer_diam']}',{user_data['chosen_width_s']}, 
                                                            {user_data['chosen_weight_b']},  '{user_data['chosen_name']}',
                                                              current_timestamp + interval'6 hours', current_timestamp + interval'6 hours')""")
        conn.commit()
        cursor.close()
        conn.close()
        await state.set_state(SetParameterPERT.send_photo)
    else:
        await message.answer(
            text="В данный момент работы не ведутся",
            reply_markup=ReplyKeyboardRemove()
        )
