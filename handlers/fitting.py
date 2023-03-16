from aiogram import Router, F
from aiogram.filters.command import Command
from aiogram.filters.text import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards.simple_row import make_row_keyboard
from datetime import datetime, timedelta
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
available_fit_names = ['КРЕПЛЕНИЕ Q20 мм DENIZ KELEPCE',
'КРЕПЛЕНИЕ Q25 мм DENIZ KELEPCE',
'КРЕПЛЕНИЕ Q32 мм DENIZ KELEPCE',
'МУФТА ВОДОПР 20 мм DENIZ MANSON',
'МУФТА ВОДОПР 25 мм DENIZ MANSON',
'МУФТА ВОДОПР 32 мм DENIZ MANSON',
'МУФТА С ВНУТ РЕЗБ 20*1/2 DENIZ RAKOR I.D',
'МУФТА С ВНУТ РЕЗБ 25*3/4 DENIZ RAKOR I.D',
'МУФТА С ВНУТ РЕЗБ 32*1 DENIZ RAKOR I.D',
'МУФТА С НАРУЖ РЕЗБ 20*1/2 DENIZ RAKOR D.D',
'МУФТА С НАРУЖ РЕЗБ 25*3/4 DENIZ RAKOR D.D',
'МУФТА С НАРУЖ РЕЗБ 32*1 DENIZ RAKOR D.D',
'ОТВОД ВОДОПР 20*45 DENIZ DIRSEK',
'ОТВОД ВОДОПР 20*90 DENIZ DIRSEK',
'ОТВОД ВОДОПР 25*45 DENIZ DIRSEK',
'ОТВОД ВОДОПР 25*90 DENIZ DIRSEK',
'ОТВОД ВОДОПР 32*45 DENIZ DIRSEK',
'ОТВОД ВОДОПР 32*90 DENIZ DIRSEK',
'ОТВОД ВОДОПР 40*90 DENIZ DIRSEK',
'ТРОЙН ПЕРЕХОДНОЙ 25*20*25 DENIZ INEGAL TE',
'ТРОЙН ПЕРЕХОДНОЙ 32*20*32 DENIZ INEGAL TE',
'ТРОЙН ПЕРЕХОДНОЙ 32*25*32 DENIZ INEGAL TE',
'ТРОЙН ВОДОПР ПРЯМОЙ 20*20 мм DENIZ TE CATAL',
'ТРОЙН ВОДОПР ПРЯМОЙ 25*25 мм DENIZ TE CATAL',
'ТРОЙН ВОДОПР ПРЯМОЙ 32*32 мм DENIZ TE CATAL',
'КРЕПЛЕНИЕ Q20 мм БЕЛЫЙ DENIZ KELEPCE',
'КРЕПЛЕНИЕ Q25 мм БЕЛЫЙ DENIZ KELEPCE',
'КРЕПЛЕНИЕ Q32 мм БЕЛЫЙ DENIZ KELEPCE',
'МУФТА ВОДОПР 20 мм БЕЛЫЙ DENIZ MANSON',
'МУФТА ВОДОПР 25 мм БЕЛЫЙ DENIZ MANSON',
'МУФТА ВОДОПР 32 мм БЕЛЫЙ DENIZ MANSON',
'МУФТА С ВНУТ РЕЗБ 20*1/2 БЕЛЫЙ DENIZ RAKOR I.D',
'МУФТА С ВНУТ РЕЗБ 25*3/4 БЕЛЫЙ DENIZ RAKOR I.D',
'МУФТА С ВНУТ РЕЗБ 32*1 БЕЛЫЙ DENIZ RAKOR I.D',
'МУФТА С НАРУЖ РЕЗБ 20*1/2 БЕЛЫЙ DENIZ RAKOR D.D',
'МУФТА С НАРУЖ РЕЗБ 25*3/4 БЕЛЫЙ DENIZ RAKOR D.D',
'МУФТА С НАРУЖ РЕЗБ 32*1 БЕЛЫЙ DENIZ RAKOR D.D',
'ОТВОД ВОДОПР 20*45 БЕЛЫЙ DENIZ DIRSEK',
'ОТВОД ВОДОПР 20*90 БЕЛЫЙ DENIZ DIRSEK',
'ОТВОД ВОДОПР 25*45 БЕЛЫЙ DENIZ DIRSEK',
'ОТВОД ВОДОПР 25*90 БЕЛЫЙ DENIZ DIRSEK',
'ОТВОД ВОДОПР 32*45 БЕЛЫЙ DENIZ DIRSEK',
'ОТВОД ВОДОПР 32*90 БЕЛЫЙ DENIZ DIRSEK',
'ОТВОД ВОДОПР 40*90 БЕЛЫЙ DENIZ DIRSEK',
'ТРОЙН ПЕРЕХОДНОЙ 25*20*25 БЕЛЫЙ DENIZ INEGAL TE',
'ТРОЙН ПЕРЕХОДНОЙ 32*20*32 БЕЛЫЙ DENIZ INEGAL TE',
'ТРОЙН ПЕРЕХОДНОЙ 32*25*32 БЕЛЫЙ DENIZ INEGAL TE',
'ТРОЙН ВОДОПР ПРЯМОЙ 20*20 мм БЕЛЫЙ DENIZ TE CATAL',
'ТРОЙН ВОДОПР ПРЯМОЙ 25*25 мм БЕЛЫЙ DENIZ TE CATAL',
'ТРОЙН ВОДОПР ПРЯМОЙ 32*32 мм БЕЛЫЙ DENIZ TE CATAL',
'БУТЫЛКА КАНАЛИЗ 100*50 REDUK DENIZ',
'МУФТА КАНАЛИЗ 50 MANSON DENIZ',
'МУФТА КАНАЛИЗ 100 MANSON DENIZ',
'ОТВОД КАНАЛИЗ 50*45 DIRSEK DENIZ',
'ОТВОД КАНАЛИЗ 50*90 DIRSEK DENIZ',
'ОТВОД КАНАЛИЗ 100*45 DIRSEK DENIZ',
'ОТВОД КАНАЛИЗ 100*90 DIRSEK DENIZ',
'ТРОЙНИК KOCОЙ 50*50 TEK CATAL DENIZ',
'ТРОЙНИК KOCОЙ 100*100 TEK CATAL DENIZ',
'ТРОЙНИК ПРЯМОЙ 50*50 TE CATAL DENIZ',
'ТРОЙНИК ПРЯМОЙ 100*50 TE CATAL DENIZ',
'ТРОЙНИК ПРЯМОЙ 100*100 TE CATAL DENIZ',
'ХОМУТ КАНАЛИЗ 50 KELEPCE DENIZ',
'ХОМУТ КАНАЛИЗ 100 KELEPCE DENIZ',
'ЗАГЛУШКА КАНАЛИЗ 50 KORTAPA DENIZ',
'ЗАГЛУШКА КАНАЛИЗ 100 KORTAPA DENIZ',
'МОСТ С 20MM DENIZ',
'МОСТ С 20MM БЕЛЫЙ DENIZ',
'ЗАГЛУШКА К ПОДОКОННИКУ АНТРАЦИТ 600mm KAVI',
'ЗАГЛУШКА К ПОДОКОННИКУ МАХАГОН 600mm KAVI',
'ЗАГЛУШКА К ПОДОКОННИКУ БЕЛЫЙ 600mm KAVI',
'ЗАГЛУШКА К ПОДОКОННИКУ ЗОЛ.ДУБ 600mm KAVI',
'ЗАГЛУШКА К ПОДОКОННИКУ МОР.ДУБ 600mm KAVI',
'КОМПЛЕКТ 20*1/2 ДЛЯ СМЕСИТЕЛЯ DENIZ  БЕЛЫЙ',
'КОМПЛЕКТ 20*1/2 ДЛЯ СМЕСИТЕЛЯ DENIZ  СЕРЫЙ',
'МУФТА С НАРУЖ РЕЗБ 25*1/2 БЕЛЫЙ DENIZ',
'МУФТА С НАРУЖ РЕЗБ 25*1/2 СЕРЫЙ DENIZ',
'МУФТА С ВНУТ РЕЗБ 25*1/2 БЕЛЫЙ DENIZ',
'МУФТА С ВНУТ РЕЗБ 25*1/2 СЕРЫЙ DENIZ',
'МУФТА С НАРУЖ РЕЗБ 32*1/2 СЕРЫЙ DENIZ',
'МУФТА С ВНУТ РЕЗБ 32*1/2 СЕРЫЙ DENIZ',
'МУФТА С НАРУЖ РЕЗБ 32*3/4 СЕРЫЙ DENIZ',
'МУФТА С ВНУТ РЕЗБ 32*3/4 СЕРЫЙ DENIZ',
'МУФТА С НАРУЖ РЕЗБ 32*1/2 БЕЛЫЙ DENIZ',
'МУФТА С ВНУТ РЕЗБ 32*1/2 БЕЛЫЙ DENIZ',
'МУФТА С НАРУЖ РЕЗБ 32*3/4 БЕЛЫЙ DENIZ',
'МУФТА С ВНУТ РЕЗБ 32*3/4 БЕЛЫЙ DENIZ',
'АРМАТУРА С ВНУТ РЕЗБ 20*3/4 DENIZ OYNBAS RAKOR I.D',
'АРМАТУРА С ВНУТ РЕЗБ 20*3/4 БЕЛАЯ DENIZ OYNBAS RAK',
'АРМАТУРА С НАР РЕЗБ 20*3/4 DENIZ OYNBAS RAKOR D.D.',
'АРМАТУРА С НАР РЕЗБ 20*3/4 БЕЛАЯ DENIZ OYNBAS RAKO',
'ОТВОД С ВНУТ РЕЗБ 20*1/2 90 DENIZ DIRSEK I.D',
'ОТВОД С ВНУТ РЕЗБ 20*1/2 90 БЕЛЫЙ DENIZ DIRSEK I.D',
'ОТВОД С НАРУЖ РЕЗБ 20*1/2 90 DENIZ DIRSEK D.D',
'ОТВОД С НАРУЖ РЕЗБ 20*1/2 90 БЕЛЫЙ DENIZ DIRSEK D.',
'АРМАТУРА С ВНУТ РЕЗБ 40*1-1/4 DENIZ OYNBAS RAKOR I',
'АРМАТУРА С ВНУТ РЕЗБ 40*1-1/4 БЕЛЫЙ DENIZ OYNBAS R ',
'АРМАТУРА С НАР РЕЗБ 40*1-1/4 DENIZ OYNBAS RAKOR D.',
'АРМАТУРА С НАР РЕЗБ 40*1-1/4 БЕЛЫЙ DENIZ OYNBAS RA',
'ТРОЙНИК KOCОЙ 100*50 TEK CATAL DENIZ PP',
'РЕВИЗИЯ 100*100 TEMIZLEME DENIZ PP',
'КРЕСТОВИНА 100*100*90 ISTAVROZ DENIZ PP',
'МУФТА * КАНАЛИЗ 110 MANSON OKYANUS PP',
'ОТВОД * КАНАЛИЗ 110*45 DIRSEK OKYANUS PP',
'ОТВОД * КАНАЛИЗ 110*90 DIRSEK OKYANUS PP',
'ТРОЙНИК * KOCОЙ 110*110 TEK CATAL OKYANUS PP',
'ТРОЙНИК * ПРЯМОЙ 110*110 TE CATAL OKYANUS PP',
'ТРОЙНИК * KOCОЙ 100*50 TEK CATAL OKYANUS PP',
'РЕВИЗИЯ * КАНАЛИЗ 100*100 TEMIZLEME OKYANUS PP',
'КРЕСТОВИНА * КАНАЛИЗ 100*100*90 ISTAVROZ OKYANUS PP',
'ОТВОД * КАНАЛИЗ 50*45 OKYANUS PP',
'ОТВОД * КАНАЛИЗ 50*90 DIRSEK OKYANUS PP',
'МУФТА * КАНАЛИЗ 50 MANSON OKYANUS PP',
'ТРОЙНИК * ПРЯМОЙ 50*50 TE CATAL OKYANUS PP',
'ТРОЙНИК KOCОЙ 50*50 TEK CATAL OKYANUS PP',
'КРЫШКА РЕВИЗИЙ',]


class SetParameterFit(StatesGroup):
    choosing_fitting_type = State()
    choosing_fitting_controller = State()
    choosing_fitting_smena = State()
    choosing_fitting_line = State()
    choosing_fitting_name = State()
    choosing_tube_name = State()
    choosing_fitting_tube = State()
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
    await state.set_state(SetParameterFit.choosing_fitting_tube)

@router.message(SetParameterFit.choosing_fitting_tube, F.text.in_(available_tubes))
async def pprc_tube(message: Message, state: FSMContext):
    await state.update_data(chosen_fit_name=message.text.lower())
    await message.answer(
        text='Выберите изделие',
        reply_markup=make_row_keyboard(available_fit_names)
    )
    print('choose fit name')
    await state.set_state(SetParameterFit.choosing_tube_name)


@router.message(SetParameterFit.choosing_tube_name, F.text.in_(available_fit_names))
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