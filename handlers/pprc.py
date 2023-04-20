from aiogram import Router, F
from aiogram.filters.command import Command
from aiogram.filters.text import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards.simple_row import make_row_keyboard
from datetime import datetime, timedelta
import psycopg2
from aiogram.types.photo_size import PhotoSize
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from bot import bot

router = Router()
available_answers = ['ok', 'not ok','back']
available_shifts = ['A','B','C']
available_controllers = ['Madi', 'Zhanibek', 'Magzhan']
available_masters_pprc = ['Talgat','Aibar','Bolat','back']
available_tubes = ['okyanus', 'deniz','pinar','back']
available_diameters = ['20','25','32','40','50','63','back']
available_proceeds = ['yes','back']

class SetParameterPPRC(StatesGroup):
    choosing_pprc_type = State()
    choosing_pprc_controller = State()
    choosing_pprc_smena = State()
    choosing_pprc_name = State()
    choosing_pprc_tube = State()
    choosing_pprc_nom_diameter = State()
    choosing_pprc_view = State()
    choosing_pprc_diameter = State()
    choosing_pprc_width = State()
    choosing_pprc_weight = State()
    choosing_pprc_control_mark = State()
    choosing_pprc_finish = State()
    send_photo = State()
    send_photo_view = State()

@router.message(Text(text='работает PPR-C'))
async def pprc_controller(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Выберите контроллера",
        reply_markup=make_row_keyboard(available_controllers)
    )
    print('choose controller')
    await state.set_state(SetParameterPPRC.choosing_pprc_controller)
    
@router.message(SetParameterPPRC.choosing_pprc_controller)
async def pprc_smena(message: Message, state: FSMContext):
    if message.text == 'go':
        await message.answer(
            text="Выберите смену ",
            reply_markup=make_row_keyboard(available_shifts)
        )
        print('choose smena canal')
        await state.set_state(SetParameterPPRC.choosing_pprc_smena)
    else:
        await state.update_data(chosen_controller_name=message.text.lower())
        await message.answer(
            text="Выберите смену ",
            reply_markup=make_row_keyboard(available_shifts)
        )
        print('choose smena')
        await state.set_state(SetParameterPPRC.choosing_pprc_smena)

@router.message(SetParameterPPRC.choosing_pprc_smena)
async def pprc_name(message: Message, state: FSMContext):
    if message.text == 'back':
        await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
        await state.set_state(SetParameterPPRC.choosing_pprc_controller)
    elif message.text == 'go':
        await message.answer(
            text="Кто является мастером на линии на текущий час ?",
            reply_markup=make_row_keyboard(available_masters_pprc)
        )
        print('choose master')
        await state.set_state(SetParameterPPRC.choosing_pprc_name)
    else:
        await state.update_data(chosen_smena=message.text.lower())
        await message.answer(
            text="Кто является мастером на линии на текущий час ?",
            reply_markup=make_row_keyboard(available_masters_pprc)
        )
        print('choose master')
        await state.set_state(SetParameterPPRC.choosing_pprc_name)


@router.message(SetParameterPPRC.choosing_pprc_name)
async def pprc_tube(message: Message, state: FSMContext):
    if message.text == 'back':
        await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
        await state.set_state(SetParameterPPRC.choosing_pprc_controller)
    elif message.text == 'go':
        await message.answer(
            text="выберите бренд PPR-C трубы:",
            reply_markup=make_row_keyboard(available_tubes)
        )
        print('choose brand')
        await state.set_state(SetParameterPPRC.choosing_pprc_tube)
    else:
        await state.update_data(chosen_name=message.text.lower())
        await message.answer(
            text="выберите бренд PPR-C трубы:",
            reply_markup=make_row_keyboard(available_tubes)
        )
        print('choose brand')
        await state.set_state(SetParameterPPRC.choosing_pprc_tube)

@router.message(SetParameterPPRC.choosing_pprc_tube)
async def pprc_nom_diameter(message: Message, state: FSMContext):
    if message.text == 'back':
        await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
        await state.set_state(SetParameterPPRC.choosing_pprc_smena)
    elif message.text == 'go':
        await message.answer(
            text="выберите номинальный диаметр PPR-C трубы:",
            reply_markup=make_row_keyboard(available_diameters)
        )
        print('choose nom diameter')
        await state.set_state(SetParameterPPRC.choosing_pprc_nom_diameter)
    else:
        await state.update_data(chosen_tube=message.text.lower())
        await message.answer(
            text="выберите номинальный диаметр PPR-C трубы:",
            reply_markup=make_row_keyboard(available_diameters)
        )
        print('choose nom diameter')
        await state.set_state(SetParameterPPRC.choosing_pprc_nom_diameter)

@router.message(SetParameterPPRC.choosing_pprc_nom_diameter)
async def pprc_view(message: Message, state: FSMContext):
    if message.text == 'back':
        await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
        await state.set_state(SetParameterPPRC.choosing_pprc_name)
    elif message.text == 'go':
        await message.answer(
            text="оцените внешний вид PPR-C трубы:",
            reply_markup=make_row_keyboard(available_answers)
        )
        print('choose view')
        await state.set_state(SetParameterPPRC.choosing_pprc_view)
    else:
        await state.update_data(chosen_nom_diameter=message.text.lower())
        await message.answer(
            text="оцените внешний вид PPR-C трубы:",
            reply_markup=make_row_keyboard(available_answers)
        )
        print('choose view')
        await state.set_state(SetParameterPPRC.choosing_pprc_view)

@router.message(SetParameterPPRC.choosing_pprc_view, F.content_type.in_({'photo'}))
async def get_photo_pprc_view(message: Message, state: FSMContext):
    
    await message.answer(
            text="отправьте фото",
            reply_markup=make_row_keyboard(available_answers)
        )
    print('choose view photo')

    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()           
    drive = GoogleDrive(gauth)  
    file_id =  message.photo[-1].file_id
    file_unique_id = message.photo[-1].file_unique_id
    PhotoSize(file_id=file_id, file_unique_id=file_unique_id, width='1920', height='1080')
    file = await bot.get_file(file_id)
    file_path = file.file_path
    filename = 'pprc_' + (datetime.now() + timedelta(hours=6)).strftime('%Y-%m-%d %H:%M:%S' + '.jpg')
    await bot.download_file(file_path, filename )
    upload_file_list = [filename]
    for upload_file in upload_file_list:
        gfile = drive.CreateFile({'parents': [{'id': '1VnkFYt-wgCIyaEDoYUsOjjkYP0BzXQcE'}]})#1VHMD2m_CBy6zGobYF6YPCJtyhYQdoHGS#'1yaz2rotCLCAfzusoOujCe7gW1Ec1fFqU'
        gfile.SetContentFile(upload_file)
        gfile.Upload()
    await state.set_state(SetParameterPPRC.send_photo_view)


@router.message(SetParameterPPRC.send_photo_view)
async def pprc_diameter(message: Message, state: FSMContext):
    if message.text == 'back':
        await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
        await state.set_state(SetParameterPPRC.choosing_pprc_tube)
    elif message.text == 'go':
        await state.update_data(chosen_view=message.text.lower())
        await message.answer(
            text="Теперь укажите диаметр PPR-C трубы:",
            reply_markup=ReplyKeyboardRemove()
        )
        print('choose diameter')
        await state.set_state(SetParameterPPRC.choosing_pprc_diameter)
    else:
        await state.update_data(chosen_view=message.text.lower())
        await message.answer(
            text="Теперь укажите диаметр PPR-C трубы:",
            reply_markup=ReplyKeyboardRemove()
        )
        print('choose diameter')
        await state.set_state(SetParameterPPRC.choosing_pprc_diameter)


@router.message(SetParameterPPRC.choosing_pprc_diameter) 
async def pprc_width(message: Message, state: FSMContext):
    if message.text == 'back':
        await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
        await state.set_state(SetParameterPPRC.choosing_pprc_nom_diameter)
    elif message.text == 'go':
        await message.answer(
            text="Теперь укажите толщину PPR-C трубы:",
            reply_markup=ReplyKeyboardRemove()
        )
        print('choose width')
        await state.set_state(SetParameterPPRC.choosing_pprc_width)
    else:
        await state.update_data(chosen_diameter=message.text.lower().replace(',', '.'))
        await message.answer(
            text="Теперь укажите толщину PPR-C трубы:",
            reply_markup=ReplyKeyboardRemove()
        )
        print('choose width')
        await state.set_state(SetParameterPPRC.choosing_pprc_width)


@router.message(SetParameterPPRC.choosing_pprc_width) #F.text.in_(available_food_names))
async def pprc_control_mark(message: Message, state: FSMContext):
    if (datetime.now()+ timedelta(hours = 6)).hour in [2,5,8,11,14,17,20,23]:
        if message.text == 'back':
            await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
            await state.set_state(SetParameterPPRC.choosing_pprc_view)
        elif message.text == 'go':
            await message.answer(
                    text="Оцените контрольную маркировку PPR-C трубы:",
                    reply_markup=make_row_keyboard(available_answers)
            )
            print('choose control mark')
            await state.set_state(SetParameterPPRC.choosing_pprc_control_mark)
        else:
            await state.update_data(chosen_width=message.text.lower().replace(',', '.'))
            await message.answer(
                    text="Оцените контрольную маркировку PPR-C трубы:",
                    reply_markup=make_row_keyboard(available_answers)
            )
            print('choose control mark')
            await state.set_state(SetParameterPPRC.choosing_pprc_control_mark)

    elif (datetime.now()+ timedelta(hours = 6)).hour in [0,1,3,4,6,7,9,10,12,13,15,16,18,19,21,22]:
        if message.text == 'back':
            await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
            await state.set_state(SetParameterPPRC.choosing_pprc_view)
        elif message.text == 'go':
            await message.answer(
                    text="перейти к передаче данных",
                    reply_markup=make_row_keyboard(available_proceeds)
            )
            await state.set_state(SetParameterPPRC.choosing_pprc_finish)
        else:
            await state.update_data(chosen_width=message.text.lower().replace(',', '.'))
            await message.answer(
                    text="перейти к передаче данных",
                    reply_markup=make_row_keyboard(available_proceeds)
            )
            await state.set_state(SetParameterPPRC.choosing_pprc_finish)
    else:
        await message.answer(
            text="В данный момент работы не ведутся",
            reply_markup=ReplyKeyboardRemove()
        )

@router.message(SetParameterPPRC.choosing_pprc_control_mark) 
async def pprc_weight(message: Message, state: FSMContext):
    if message.text == 'back':
            await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
            await state.set_state(SetParameterPPRC.choosing_pprc_diameter)
    elif message.text == 'go':
        await message.answer(
            text="Теперь укажите вес PPR-C трубы:",
            reply_markup=ReplyKeyboardRemove()
        )
        print('choose weight')
        await state.set_state(SetParameterPPRC.choosing_pprc_weight)
    else:
        await state.update_data(chosen_control_mark=message.text.lower().replace(',', '.'))
        await message.answer(
            text="Теперь укажите вес PPR-C трубы:",
            reply_markup=ReplyKeyboardRemove()
        )
        print('choose weight')
        await state.set_state(SetParameterPPRC.choosing_pprc_weight)

@router.message(SetParameterPPRC.choosing_pprc_weight)
async def pprc_finish(message: Message, state: FSMContext):
    if (datetime.now()+ timedelta(hours = 6)).hour in [2,5,8,11,14,17,20,23]:
        if message.text == 'back':
            await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
            await state.set_state(SetParameterPPRC.choosing_pprc_width)
        elif message.text == 'go':
            await message.answer(
                text="перейти к передаче данных",
                reply_markup=make_row_keyboard(available_proceeds)
            )
            await state.set_state(SetParameterPPRC.choosing_pprc_finish)
        else:
            await state.update_data(chosen_weight=message.text.lower())
            await message.answer(
                text="перейти к передаче данных",
                reply_markup=make_row_keyboard(available_proceeds)
            )
            await state.set_state(SetParameterPPRC.choosing_pprc_finish)

@router.message(SetParameterPPRC.choosing_pprc_finish, F.text.in_(available_proceeds))
async def pprc_chosen(message: Message, state: FSMContext):
    if (datetime.now()+ timedelta(hours = 6)).hour in [2,5,8,11,14,17,20,23]:
        if message.text == 'back':
            await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
            await state.set_state(SetParameterPPRC.choosing_pprc_control_mark)
        else:
            user_data = await state.get_data()
            await state.clear()
            await message.answer(
                text="Благодарю за заполненные данные. Отправьте фото подтверждение",
                reply_markup=ReplyKeyboardRemove()
            )
            print('success 5 params')
            conn = psycopg2.connect(dbname="neondb", user="zhanabayevasset", password="txDhFR1yl8Pi", host='ep-cool-poetry-346809.us-east-2.aws.neon.tech')
            cursor = conn.cursor()
            cursor.execute(f"""insert into pprc_params (WORKING,CONTROLLER_NAME, SHIFT, BRAND, NOMINAL_DIAMETER, VIEW, DIAMETER, WEIGHT,WIDTH,MARK_CONTROL, MASTER, created_at, updated_at) values (TRUE,'{user_data['chosen_controller_name']}','{user_data['chosen_smena']}','{user_data['chosen_tube']}', '{user_data['chosen_nom_diameter']}', '{user_data['chosen_view']}',{user_data['chosen_diameter']}, {user_data['chosen_weight']}, {user_data['chosen_width']}, '{user_data['chosen_control_mark']}', '{user_data['chosen_name']}',  current_timestamp + interval'6 hours', current_timestamp + interval'6 hours')""")
            conn.commit()
            cursor.close()
            conn.close()
            await state.set_state(SetParameterPPRC.send_photo)
    elif (datetime.now()+ timedelta(hours = 6)).hour in [0,1,3,4,6,7,9,10,12,13,15,16,18,19,21,22]:
        if message.text == 'back':
            await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
            await state.set_state(SetParameterPPRC.choosing_pprc_diameter)
        else:
            print('sucess 3 params')
            user_data = await state.get_data()
            await state.clear()
            await message.answer(
                text="Благодарю за заполненные данные. Отправьте фото подтверждение",
                reply_markup=ReplyKeyboardRemove()
            )
            
            conn = psycopg2.connect(dbname="neondb", user="zhanabayevasset", password="txDhFR1yl8Pi", host='ep-cool-poetry-346809.us-east-2.aws.neon.tech')
            cursor = conn.cursor()
            cursor.execute(f"""insert into pprc_params (WORKING,CONTROLLER_NAME, SHIFT, BRAND, NOMINAL_DIAMETER, VIEW, DIAMETER, WIDTH, MASTER, created_at, updated_at) values (TRUE, '{user_data['chosen_controller_name']}','{user_data['chosen_smena']}', '{user_data['chosen_tube']}', '{user_data['chosen_nom_diameter']}','{user_data['chosen_view']}',  {user_data['chosen_diameter']},{user_data['chosen_width']}, '{user_data['chosen_name']}', current_timestamp + interval'6 hours', current_timestamp + interval'6 hours')""")
            conn.commit()
            cursor.close()
            conn.close()
            await state.set_state(SetParameterPPRC.send_photo)
    else:
        await message.answer(
            text="В данный момент работы не ведутся",
            reply_markup=ReplyKeyboardRemove()
        )