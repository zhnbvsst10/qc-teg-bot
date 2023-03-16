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
# from pydrive.auth import GoogleAuth
# from pydrive.drive import GoogleDrive
# from aiogram.types.photo_size import PhotoSize
# from bot import bot


router = Router()
available_answers = ['ok', 'not ok']
available_shifts = ['A','B','C']
available_controllers = ['Madi', 'Zhanibek', 'Magzhan']
available_masters_fitting = ['Salamat', 'Dauren', 'Anton']
available_tubes = ['okyanus', 'deniz','kavi']
available_diameters = ['50','110']
available_proceeds = ['yes']
available_stanoks = ['1','2','3','4','5','6']
available_fit_names_1 = ['КРЕПЛЕНИЕ ',
                            'МУФТА ',
                            'ОТВОД ',
                            'ТРОЙНИК ',
                            'БУТЫЛКА ',
                            'ХОМУТ ',
                            'ЗАГЛУШКА ',
                            'АРМАТУРА ',
                            'КОМЛПЕКТ ',
                            'РЕВИЗИЯ ',
                            'КРЫШКА ']

available_fit_names_2 = ['__ ',
'ВОДОПР ',
'ВНУТР РЕЗБ ',
'НАРУЖ ',
'ПЕРЕХОД ',
'КАНАЛИЗ ',
'КОСОЙ ',
'ПОДОКОН ',
'РЕВИЗИЙ ']


available_fit_names_4 = ['DENIZ KELEPCE',
                        'DENIZ MANSON',
                        'DENIZ RAKOR I.D',
                        'DENIZ DIRSEK',
                        'DENIZ INEGAL TE',
                        'DENIZ TE CATAL',
                        'DENIZ KORTAPA']
button1 = KeyboardButton(text='КРЕПЛЕНИЕ ')
button2 = KeyboardButton(text='МУФТА ')
button3 = KeyboardButton(text='ОТВОД ')
button4 = KeyboardButton(text='ТРОЙНИК ')
button5 = KeyboardButton(text='БУТЫЛКА ')
button6 = KeyboardButton(text='ХОМУТ ')
button7 = KeyboardButton(text='ЗАГЛУШКА ')
button8 = KeyboardButton(text='АРМАТУРА ')
button9 = KeyboardButton(text='РЕВИЗИЯ ')
button10 = KeyboardButton(text='КРЫШКА ')
# markup3 = ReplyKeyboardMarkup(keyboard=[button1, button2, button3, button4, button5, button6, button7, button8, button9, button10])
#.row(buttons=[button1, button2, button3, button4], width=10)               
markup3 = ReplyKeyboardBuilder([[button1]]).add(button2).adjust(10,repeat=True).add(button3).adjust(repeat=True).as_markup()#.add(button3).add(button4).add(button5).add(button6).add(button7).add(button8).add(button9).add(button10)
class SetParameterFit(StatesGroup):
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
    choosing_fitting_nom_diameter = State()
    choosing_fitting_view = State()
    choosing_fitting_functionality = State()
    choosing_fitting_finish = State()
    send_photo = State()

@router.message(Text(text='работает фиттинг'))
async def fitting_controller(message: Message, state: FSMContext):
    
    await message.answer(
        text="Выберите контроллера",
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
async def fitting_smena(message: Message, state: FSMContext):
    await state.update_data(chosen_stanok=message.text.lower())
    await message.answer(
        text="Выберите станок",
        reply_markup=make_row_keyboard(available_stanoks)
    )
    print('choose stanok')
    await state.set_state(SetParameterFit.choosing_fitting_line)


@router.message(SetParameterFit.choosing_fitting_line)
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
        text="Выберите бренд фиттинга:",
        reply_markup=make_row_keyboard(available_tubes)
    )
    print('choose brand')
    await state.set_state(SetParameterFit.choosing_fitting_tube_1)

@router.message(SetParameterFit.choosing_fitting_tube_1)
async def pprc_tube(message: Message, state: FSMContext):
    await state.update_data(chosen_fit_name_1=message.text.lower())
    await message.answer(
        text='Выберите изделие (1 слово)',
        reply_markup=markup3#make_row_keyboard_2(available_fit_names_1)
    )
    print('choose fit name 1')
    await state.set_state(SetParameterFit.choosing_fitting_tube_2)

@router.message(SetParameterFit.choosing_fitting_tube_1)
async def pprc_tube(message: Message, state: FSMContext):
    await state.update_data(chosen_fit_name_2=message.text.lower())
    await message.answer(
        text='Выберите изделие (2 слово)',
        reply_markup=make_row_keyboard(available_fit_names_2)
    )
    print('choose fit name 2')
    await state.set_state(SetParameterFit.choosing_fitting_tube_3)

@router.message(SetParameterFit.choosing_fitting_tube_1)
async def pprc_tube(message: Message, state: FSMContext):
    await state.update_data(chosen_fit_name_3=message.text.lower())
    await message.answer(
        text='Выберите изделие (3 слово)',
        # reply_markup=make_row_keyboard(available_fit_names)
    )
    print('choose fit name 3')
    await state.set_state(SetParameterFit.choosing_fitting_tube_4)

@router.message(SetParameterFit.choosing_fitting_tube_4)
async def pprc_tube(message: Message, state: FSMContext):
    await state.update_data(chosen_fit_name_4=message.text.lower())
    await message.answer(
        text='Выберите изделие (4 слово)',
        reply_markup=make_row_keyboard(available_fit_names_4)
    )
    print('choose fit name_4')
    await state.set_state(SetParameterFit.choosing_tube_name)

@router.message(SetParameterFit.choosing_tube_name)
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
    await message.answer(text=" ".join([str(i[1]) for i in user_data.items()]) + " " + message.text.lower())
    await state.clear()
    await message.answer(
            text="Благодарю за заполненные данные. Отправьте фото подтверждение",
            reply_markup=ReplyKeyboardRemove()
    )
    print('success fitting')
    conn = psycopg2.connect(dbname="neondb", user="zhanabayevasset", password="txDhFR1yl8Pi", host='ep-cool-poetry-346809.us-east-2.aws.neon.tech')
    cursor = conn.cursor()
    cursor.execute(f"""insert into fitting_params (WORKING,CONTROLLER_NAME, SHIFT, STANOK, FITTING_NAME, BRAND, NOMINAL_DIAMETER, VIEW, FUNCTIONALITY, MASTER, created_at, updated_at) values (TRUE,'{user_data['chosen_controller_name']}','{user_data['chosen_smena']}', '{user_data['chosen_stanok']}', '{user_data['chosen_fit_name']}',  '{user_data['chosen_tube']}', '{user_data['chosen_nom_diameter']}', '{user_data['chosen_view']}','{user_data['chosen_functionality']}',  '{user_data['chosen_name']}',  current_timestamp + interval'6 hours', current_timestamp + interval'6 hours')""")
    conn.commit()
    cursor.close()
    conn.close()
    await state.set_state(SetParameterFit.send_photo)

# @router.message(SetParameterFit.send_photo, F.content_type.in_({'photo'}))
# async def pvc_photo(message: Message, state: FSMContext):
#     gauth = GoogleAuth()
#     gauth.LocalWebserverAuth()  
#     await state.clear()         
#     drive = GoogleDrive(gauth)  
#     file_id =  message.photo[-1].file_id
#     file_unique_id = message.photo[-1].file_unique_id
#     PhotoSize(file_id=file_id, file_unique_id=file_unique_id, width='1920', height='1080')
#     file = await bot.get_file(file_id)
#     file_path = file.file_path
#     filename = 'fitting_' + (datetime.now() + timedelta(hours=6)).strftime('%Y-%m-%d %H:%M:%S' + '.jpg')
#     await bot.download_file(file_path, filename )
#     upload_file_list = [filename]
#     for upload_file in upload_file_list:
#         gfile = drive.CreateFile({'parents': [{'id': '1yaz2rotCLCAfzusoOujCe7gW1Ec1fFqU'}]})
#         gfile.SetContentFile(upload_file)
#         gfile.Upload()