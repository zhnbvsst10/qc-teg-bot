from aiogram import Router, F
from aiogram.filters.command import Command
from aiogram.filters.text import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards.simple_row import make_row_keyboard
from datetime import datetime, timedelta
from aiogram.utils.keyboard import KeyboardButton,ReplyKeyboardBuilder, InlineKeyboardBuilder

import psycopg2
from aiogram.types.photo_size import PhotoSize
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from aiogram import Bot
import os

#token = os.getenv('TOKEN')
token = '6029120908:AAFJPrT_MHo4vUVEH4rCnl46UbVxT9goJ_g'
bot = Bot(token=token)

router = Router()


available_answers = ['ok', 'not ok','back']
available_shifts = ['A','B','C', 'back']
available_controllers = ['Daulet', 'Adilet', 'Dinmukhammed']
available_masters_fitting = ['Salamat', 'Dauren', 'Aibek','back']
available_tubes = ['okyanus', 'deniz','kavi','back']
available_diameters = ['20','25','32','40','back']
available_proceeds = ['yes','back']
available_stanoks = ['1','2','3','4','5','6','back']
name_dict = {
            'АРМАТУРА': [   
                'АРМАТУРА С ВНУТ РЕЗБ 20*3/4 DENIZ OYNBAS RAKOR I.D',
                'АРМАТУРА С ВНУТ РЕЗБ 20*3/4 БЕЛАЯ DENIZ OYNBAS RAK',
                'АРМАТУРА С ВНУТ РЕЗБ 40*1-1/4 DENIZ OYNBAS RAKOR I',
                'АРМАТУРА С ВНУТ РЕЗБ 40*1-1/4 БЕЛЫЙ DENIZ OYNBAS R',
                'АРМАТУРА С НАР РЕЗБ 20*3/4 DENIZ OYNBAS RAKOR D.D.',
                'АРМАТУРА С НАР РЕЗБ 20*3/4 БЕЛАЯ DENIZ OYNBAS RAKO',
                'АРМАТУРА С НАР РЕЗБ 40*1-1/4 DENIZ OYNBAS RAKOR D.',
                'АРМАТУРА С НАР РЕЗБ 40*1-1/4 БЕЛЫЙ DENIZ OYNBAS RA',
            ],
            
            'КОМПЛЕКТ': [
                'КОМПЛЕКТ 20*1/2 ДЛЯ СМЕСИТЕЛЯ DENIZ  БЕЛЫЙ',
                'КОМПЛЕКТ 20*1/2 ДЛЯ СМЕСИТЕЛЯ DENIZ  СЕРЫЙ',
            ],
            'КРЕПЛЕНИЕ': [
                'КРЕПЛЕНИЕ Q20 мм DENIZ KELEPCE',
                'КРЕПЛЕНИЕ Q20 мм БЕЛЫЙ DENIZ KELEPCE',
                'КРЕПЛЕНИЕ Q25 мм DENIZ KELEPCE',
                'КРЕПЛЕНИЕ Q25 мм БЕЛЫЙ DENIZ KELEPCE',
                'КРЕПЛЕНИЕ Q32 мм DENIZ KELEPCE',
                'КРЕПЛЕНИЕ Q32 мм БЕЛЫЙ DENIZ KELEPCE',
            ],
            'КРЕСТОВИНА': [
                'КРЕСТОВИНА 100*100*90 ISTAVROZ DENIZ PP'
            ],
            'МОСТ' : [
                'МОСТ С 20MM DENIZ',
                'МОСТ С 20MM БЕЛЫЙ DENIZ'
            ],
            'СМЕСИТЕЛЬ' : [
                'СМЕСИТЕЛЬ DENIZ D20*1/2 БЕЛЫЙ',
                'СМЕСИТЕЛЬ DENIZ D20*1/2 СЕРЫЙ',
            ],

            'МУФТА' : [
                'МУФТА ВОДОПР 20 мм DENIZ MANSON',
                'МУФТА ВОДОПР 20 мм БЕЛЫЙ DENIZ MANSON',
                'МУФТА ВОДОПР 25 мм DENIZ MANSON',
                'МУФТА ВОДОПР 25 мм БЕЛЫЙ DENIZ MANSON',
                'МУФТА ВОДОПР 32 мм DENIZ MANSON',
                'МУФТА ВОДОПР 32 мм БЕЛЫЙ DENIZ MANSON',
                'МУФТА ВОДОПР С ВНУТ РЕЗБ 20*1/2 DENIZ RAKOR I.D',
                'МУФТА ВОДОПР С ВНУТ РЕЗБ 20*1/2 БЕЛЫЙ DENIZ RAKOR I.D',
                'МУФТА ВОДОПР С ВНУТ РЕЗБ 25*1/2 БЕЛЫЙ DENIZ',
                'МУФТА ВОДОПР С ВНУТ РЕЗБ 25*1/2 СЕРЫЙ DENIZ',
                'МУФТА ВОДОПР С ВНУТ РЕЗБ 25*3/4 DENIZ RAKOR I.D',
                'МУФТА ВОДОПР С ВНУТ РЕЗБ 25*3/4 БЕЛЫЙ DENIZ RAKOR I.D',
                'МУФТА ВОДОПР С ВНУТ РЕЗБ 32*1 DENIZ RAKOR I.D',
                'МУФТА ВОДОПР С ВНУТ РЕЗБ 32*1 БЕЛЫЙ DENIZ RAKOR I.D',
                'МУФТА ВОДОПР С ВНУТ РЕЗБ 32*1/2 БЕЛЫЙ DENIZ',
                'МУФТА ВОДОПР С ВНУТ РЕЗБ 32*1/2 СЕРЫЙ DENIZ',
                'МУФТА ВОДОПР С ВНУТ РЕЗБ 32*3/4 БЕЛЫЙ DENIZ',
                'МУФТА ВОДОПР С ВНУТ РЕЗБ 32*3/4 СЕРЫЙ DENIZ',
                'МУФТА ВОДОПР С НАРУЖ РЕЗБ 20*1/2 DENIZ RAKOR D.D',
                'МУФТА ВОДОПР С НАРУЖ РЕЗБ 20*1/2 БЕЛЫЙ DENIZ RAKOR D.D',
                'МУФТА ВОДОПР С НАРУЖ РЕЗБ 25*1/2 БЕЛЫЙ DENIZ',
                'МУФТА ВОДОПР С НАРУЖ РЕЗБ 25*1/2 СЕРЫЙ DENIZ',
                'МУФТА ВОДОПР С НАРУЖ РЕЗБ 25*3/4 DENIZ RAKOR D.D',
                'МУФТА ВОДОПР С НАРУЖ РЕЗБ 25*3/4 БЕЛЫЙ DENIZ RAKOR D.D',
                'МУФТА ВОДОПР С НАРУЖ РЕЗБ 32*1 DENIZ RAKOR D.D',
                'МУФТА ВОДОПР С НАРУЖ РЕЗБ 32*1 БЕЛЫЙ DENIZ RAKOR D.D',
                'МУФТА ВОДОПР С НАРУЖ РЕЗБ 32*1/2 БЕЛЫЙ DENIZ',
                'МУФТА ВОДОПР С НАРУЖ РЕЗБ 32*1/2 СЕРЫЙ DENIZ',
                'МУФТА ВОДОПР С НАРУЖ РЕЗБ 32*3/4 БЕЛЫЙ DENIZ',
                'МУФТА ВОДОПР С НАРУЖ РЕЗБ 32*3/4 СЕРЫЙ DENIZ',
            ],
            'ОТВОД' : [
                'ОТВОД ВОДОПР 20*45 DENIZ DIRSEK',
                'ОТВОД ВОДОПР 20*45 БЕЛЫЙ DENIZ DIRSEK',
                'ОТВОД ВОДОПР 20*90 DENIZ DIRSEK',
                'ОТВОД ВОДОПР 20*90 БЕЛЫЙ DENIZ DIRSEK',
                'ОТВОД ВОДОПР 25*45 DENIZ DIRSEK',
                'ОТВОД ВОДОПР 25*45 БЕЛЫЙ DENIZ DIRSEK',
                'ОТВОД ВОДОПР 25*90 DENIZ DIRSEK',
                'ОТВОД ВОДОПР 25*90 БЕЛЫЙ DENIZ DIRSEK',
                'ОТВОД ВОДОПР 32*45 DENIZ DIRSEK',
                'ОТВОД ВОДОПР 32*45 БЕЛЫЙ DENIZ DIRSEK',
                'ОТВОД ВОДОПР 32*90 DENIZ DIRSEK',
                'ОТВОД ВОДОПР 32*90 БЕЛЫЙ DENIZ DIRSEK',
                'ОТВОД ВОДОПР 40*90 DENIZ DIRSEK',
                'ОТВОД ВОДОПР 40*90 БЕЛЫЙ DENIZ DIRSEK',
                'ОТВОД ВОДОПР С ВНУТ РЕЗБ 20*1/2 90 DENIZ DIRSEK I.D',
                'ОТВОД ВОДОПР С ВНУТ РЕЗБ 20*1/2 90 БЕЛЫЙ DENIZ DIRSEK I.D',
                'ОТВОД ВОДОПР С НАРУЖ РЕЗБ 20*1/2 90 DENIZ DIRSEK D.D',
                'ОТВОД ВОДОПР С НАРУЖ РЕЗБ 20*1/2 90 БЕЛЫЙ DENIZ DIRSEK D.',
            ],
            'РЕВИЗИЯ' : [
                'РЕВИЗИЯ 100*100 TEMIZLEME DENIZ PP'
            ],
            'ТРОЙНИК' : [
                'ТРОЙН ВОДОПР ПРЯМОЙ 20*20 мм DENIZ TE CATAL',
                'ТРОЙН ВОДОПР ПРЯМОЙ 20*20 мм БЕЛЫЙ DENIZ TE CATAL',
                'ТРОЙН ВОДОПР ПРЯМОЙ 25*25 мм DENIZ TE CATAL',
                'ТРОЙН ВОДОПР ПРЯМОЙ 25*25 мм БЕЛЫЙ DENIZ TE CATAL',
                'ТРОЙН ВОДОПР ПРЯМОЙ 32*32 мм DENIZ TE CATAL',
                'ТРОЙН ВОДОПР ПРЯМОЙ 32*32 мм БЕЛЫЙ DENIZ TE CATAL',
                'ТРОЙН ПЕРЕХОДНОЙ 25*20*25 DENIZ INEGAL TE',
                'ТРОЙН ПЕРЕХОДНОЙ 25*20*25 БЕЛЫЙ DENIZ INEGAL TE',
                'ТРОЙН ПЕРЕХОДНОЙ 32*20*32 DENIZ INEGAL TE',
                'ТРОЙН ПЕРЕХОДНОЙ 32*20*32 БЕЛЫЙ DENIZ INEGAL TE',
                'ТРОЙН ПЕРЕХОДНОЙ 32*25*32 DENIZ INEGAL TE',
                'ТРОЙН ПЕРЕХОДНОЙ 32*25*32 БЕЛЫЙ DENIZ INEGAL TE',
            ],
            
        }

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
    choosing_fitting_tube_5 = State()
    choosing_fitting_nom_diameter = State()
    choosing_fitting_view = State()
    choosing_fitting_functionality = State()
    choosing_fitting_weight = State()
    choosing_fitting_finish = State()
    send_photo = State()
    send_photo_weight = State()
    send_photo_weight_sent = State()
    send_photo_func = State()
    send_photo_func_sent = State()
    send_photo_view = State()
    send_photo_view_sent = State()
    choosing_defects = State()
    defects_descr = State()
    carantine = State()
    def_send = State()

@router.message(Text(text='работает фиттинг водопр'))
async def fitting_controller(message: Message, state: FSMContext):
    
    await message.answer(
        text="Выберите контроллера",
        reply_markup=make_row_keyboard(available_controllers)
    )
    print('choose controller')
    await state.set_state(SetParameterFit.choosing_fitting_controller)

@router.message(SetParameterFit.choosing_fitting_controller)
async def pprc_name(message: Message, state: FSMContext):
    if message.text == 'go':
        await message.answer(
            text="Кто является мастером на линии на текущий час ?",
            reply_markup=make_row_keyboard(available_masters_fitting)
        )
        print('choose master')
        await state.set_state(SetParameterFit.choosing_fitting_name)
    else:
        await state.update_data(chosen_controller_name=message.text.lower())
        await message.answer(
            text="Кто является мастером на линии на текущий час ?",
            reply_markup=make_row_keyboard(available_masters_fitting)
        )
        print('choose master')
        await state.set_state(SetParameterFit.choosing_fitting_name)


@router.message(SetParameterFit.choosing_fitting_name)
async def pprc_tube(message: Message, state: FSMContext):
    if message.text == 'back':
        await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
        await state.set_state(SetParameterFit.choosing_fitting_controller)
    elif message.text == 'go':
        await message.answer(
            text="Выберите бренд фиттинга:",
            reply_markup=make_row_keyboard(available_tubes)
        )
        print('choose brand')
        await state.set_state(SetParameterFit.choosing_fitting_tube_1)
    else:
        await state.update_data(chosen_name=message.text.lower())
        await message.answer(
            text="Выберите бренд фиттинга:",
            reply_markup=make_row_keyboard(available_tubes)
        )
        print('choose brand')
        await state.set_state(SetParameterFit.choosing_fitting_tube_1)

@router.message(SetParameterFit.choosing_fitting_tube_1)
async def pprc_tube(message: Message, state: FSMContext):
    if message.text == 'back':
        await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
        await state.set_state(SetParameterFit.choosing_fitting_smena)
    elif message.text == 'go':
        button1 = KeyboardButton(text='КРЕПЛЕНИЕ')
        button2 = KeyboardButton(text='МУФТА')
        button3 = KeyboardButton(text='ОТВОД')
        button4 = KeyboardButton(text='ТРОЙНИК')
        button5 = KeyboardButton(text='МОСТ')
        button6 = KeyboardButton(text='АРМАТУРА')
        button7 = KeyboardButton(text='back')
            
        markup1 = ReplyKeyboardBuilder([[button1]]).row(button2).row(button3).row(button4).row(button5).row(button6).row(button7).as_markup()
        await message.answer(
            text='Выберите наименование продукции',
            reply_markup=markup1
        )
        print('choose fit name 1')
        await state.set_state(SetParameterFit.choosing_fitting_tube_2)
    else:
        button1 = KeyboardButton(text='КРЕПЛЕНИЕ')
        button2 = KeyboardButton(text='МУФТА')
        button3 = KeyboardButton(text='ОТВОД')
        button4 = KeyboardButton(text='ТРОЙНИК')
        button5 = KeyboardButton(text='МОСТ')
        button6 = KeyboardButton(text='АРМАТУРА')
        button7 = KeyboardButton(text='back')
            
        markup1 = ReplyKeyboardBuilder([[button1]]).row(button2).row(button3).row(button4).row(button5).row(button6).row(button7).as_markup()
        await state.update_data(chosen_tube=message.text.lower())
        await message.answer(
            text='Выберите наименование продукции',
            reply_markup=markup1
        )
        print('choose fit name 1')
        await state.set_state(SetParameterFit.choosing_fitting_tube_2)

@router.message(SetParameterFit.choosing_fitting_tube_2)
async def pprc_tube(message: Message, state: FSMContext):
    if message.text == 'back':
        await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
        await state.set_state(SetParameterFit.choosing_fitting_name)
    else:
        builder = ReplyKeyboardBuilder()
        for index in range(len(name_dict[message.text])):
            builder.button(text=f"{name_dict[message.text][index]}", callback_data = f"{name_dict[message.text][index]}")
        builder.button(text=f"back", callback_data = f"back")
        builder.adjust(1,1)
        await state.update_data(chosen_fit_name=message.text.lower())
        await message.answer(
            text='Выбрите',
            reply_markup=builder.as_markup()
        )
        print('choose fit name 3')
        await state.set_state(SetParameterFit.choosing_fitting_tube_3)


@router.message(SetParameterFit.choosing_fitting_tube_3)
async def pprc_view(message: Message, state: FSMContext):
    if message.text == 'back':
        await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
        await state.set_state(SetParameterFit.choosing_fitting_tube_1)
    elif message.text == 'go':
        await message.answer(
            text="оцените внешний вид фиттинга:",
            reply_markup=make_row_keyboard(available_answers)
        )
        print('choose view')
        await state.set_state(SetParameterFit.choosing_fitting_view)
    else:
        await state.update_data(chosen_fit_name=message.text.lower())
        await message.answer(
            text="оцените внешний вид фиттинга:",
            reply_markup=make_row_keyboard(available_answers)
        )
        print('choose view')
        await state.set_state(SetParameterFit.choosing_fitting_view)

@router.message(SetParameterFit.choosing_fitting_view)
async def get_photo_pprc_view(message: Message, state: FSMContext):
        await state.update_data(chosen_view=message.text.lower())
        await message.answer(
            text="отправьте фото",
            reply_markup=make_row_keyboard(['back'])
        )
        print('choose diameter')
        await state.set_state(SetParameterFit.send_photo_view)

@router.message(SetParameterFit.send_photo_view)
async def get_photo_pprc_view(message: Message, state: FSMContext, bot):
    if message.text == 'back':
        await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
        await state.set_state(SetParameterFit.choosing_fitting_nom_diameter)
    else:
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()           
        drive = GoogleDrive(gauth)  
        file_id =  message.photo[-1].file_id
        print(message.photo[-1])
        file_unique_id = message.photo[-1].file_unique_id
        #PhotoSize(file_id=file_id, file_unique_id=file_unique_id)
        file = await bot.get_file(file_id)
        file_path = file.file_path
        filename = 'fitting_vodop_view_' + (datetime.now() + timedelta(hours=6)).strftime('%Y-%m-%d %H:%M:%S' + '.jpg')
        await bot.download_file(file_path, filename )
        upload_file_list = [filename]
        for upload_file in upload_file_list:
            gfile = drive.CreateFile({'parents': [{'id': '1VHMD2m_CBy6zGobYF6YPCJtyhYQdoHGS'}]})
            gfile.SetContentFile(upload_file)
            gfile.Upload()

        await message.answer(
                text="продолжить",
                reply_markup=make_row_keyboard(['yes'])
                )
        await state.set_state(SetParameterFit.send_photo_view_sent)



@router.message(SetParameterFit.send_photo_view_sent)
async def pprc_functionality(message: Message, state: FSMContext):
    if message.text == 'go':
        await message.answer(
            text="Введите вес фиттинга:",
            reply_markup=ReplyKeyboardRemove()
        )
        print('choose func')
        await state.set_state(SetParameterFit.choosing_fitting_weight)
    else:
        await message.answer(
            text="Введите вес фиттинга:",
            reply_markup=ReplyKeyboardRemove()
        )
        print('choose func')
        await state.set_state(SetParameterFit.choosing_fitting_weight)

@router.message(SetParameterFit.choosing_fitting_weight)
async def get_photo_pprc_view(message: Message, state: FSMContext):
        await state.update_data(chosen_weight=message.text.lower())
        await message.answer(
            text="отправьте фото",
            reply_markup=make_row_keyboard(['back'])
        )
        print('choose diameter')
        await state.set_state(SetParameterFit.send_photo_weight)

@router.message(SetParameterFit.send_photo_weight)
async def get_photo_pprc_view(message: Message, state: FSMContext, bot):
    if message.text == 'back':
        await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
        await state.set_state(SetParameterFit.send_photo_view_sent)
    else:
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()           
        drive = GoogleDrive(gauth)  
        file_id =  message.photo[-1].file_id
        print(message.photo[-1])
        file_unique_id = message.photo[-1].file_unique_id
        #PhotoSize(file_id=file_id, file_unique_id=file_unique_id)
        file = await bot.get_file(file_id)
        file_path = file.file_path
        filename = 'fitting_vodop_weight_' + (datetime.now() + timedelta(hours=6)).strftime('%Y-%m-%d %H:%M:%S' + '.jpg')
        await bot.download_file(file_path, filename )
        upload_file_list = [filename]
        for upload_file in upload_file_list:
            gfile = drive.CreateFile({'parents': [{'id': '1VHMD2m_CBy6zGobYF6YPCJtyhYQdoHGS'}]})
            gfile.SetContentFile(upload_file)
            gfile.Upload()

        await message.answer(
                text="продолжить",
                reply_markup=make_row_keyboard(['yes'])
                )
        await state.set_state(SetParameterFit.send_photo_weight_sent)

@router.message(SetParameterFit.send_photo_weight_sent)
async def get_photo_pprc_view(message: Message, state: FSMContext):
        await message.answer(
            text="Есть ли дефекты?",
            reply_markup=make_row_keyboard(['yes','no'])
        )
        print('choose defects')
        await state.set_state(SetParameterFit.choosing_defects)


@router.message(SetParameterFit.choosing_defects)
async def get_photo_pprc_view(message: Message, state: FSMContext):
        await state.update_data(chosen_def=message.text.lower())
        if message.text == 'yes':
            await message.answer(
                text="Введите описание дефекта",
                reply_markup=ReplyKeyboardRemove()
            )
            print('choose defects')
            await state.set_state(SetParameterFit.defects_descr)
        else:
            await message.answer(
                text="продолжить",
                reply_markup=make_row_keyboard(['yes'])
            )
            print('choose defects')
            await state.set_state(SetParameterFit.def_send)

@router.message(SetParameterFit.defects_descr)
async def get_photo_pprc_view(message: Message, state: FSMContext):
        await state.update_data(chosen_def_descr=message.text.lower())
        await message.answer(
                text="сколько штук поставлено в карантин",
                reply_markup=ReplyKeyboardRemove()
            )
        await state.set_state(SetParameterFit.carantine)

@router.message(SetParameterFit.carantine)
async def get_photo_pprc_view(message: Message, state: FSMContext):
        await state.update_data(carantine=message.text.lower())
        await message.answer(
                text="сколько штук ушло в брак?",
                reply_markup=ReplyKeyboardRemove()
            )
        await state.set_state(SetParameterFit.def_send)

# 1VHMD2m_CBy6zGobYF6YPCJtyhYQdoHGS
@router.message(SetParameterFit.def_send)
async def pprc_finish(message: Message, state: FSMContext):
    if message.text == 'go':
        await message.answer(
                text="перейти к передаче данных",
                reply_markup=make_row_keyboard(available_proceeds)
        )
        await state.set_state(SetParameterFit.choosing_fitting_finish)
    else:
        await state.update_data(def_send=message.text.lower())
        await message.answer(
                text="перейти к передаче данных",
                reply_markup=make_row_keyboard(available_proceeds)
        )
        await state.set_state(SetParameterFit.choosing_fitting_finish)



@router.message(SetParameterFit.choosing_fitting_finish, F.text.in_(available_proceeds))
async def fitting_chosen(message: Message, state: FSMContext):
    if message.text == 'back':
        await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
        await state.set_state(SetParameterFit.choosing_fitting_view)
    else:

        user_data = await state.get_data()
        await message.answer(text=" ".join([str(i[1]) for i in user_data.items()]) + " " + message.text.lower())
        await state.clear()
        await message.answer(
                text="Благодарю за заполненные данные",
                reply_markup=ReplyKeyboardRemove()
        )
        print('success fitting')
        if ('carantine' in user_data.keys()) == False:
                user_data['carantine'] = '0'
                user_data['def_send'] = '0'
                user_data['chosen_def_descr'] = ' '

        conn = psycopg2.connect(dbname="neondb", user="zhanabayevasset", password="txDhFR1yl8Pi", host='ep-cool-poetry-346809.us-east-2.aws.neon.tech')
        cursor = conn.cursor()
        cursor.execute(f"""insert into fitting_vodop_params (WORKING,CONTROLLER_NAME,  STANOK,SHIFT, FITTING_NAME, BRAND,  VIEW,  MASTER,WEIGHT,DEFECT,DEFECT_DESCR, created_at, updated_at, carantine_num, defect_num) values (TRUE,'{user_data['chosen_controller_name']}', '{user_data['chosen_stanok']}','{user_data['chosen_smena']}', '{user_data['chosen_fit_name']}',  '{user_data['chosen_tube']}',  '{user_data['chosen_view']}','{user_data['chosen_name']}','{user_data['chosen_weight']}', '{user_data['chosen_def']}', '{user_data['chosen_def_descr']}', current_timestamp + interval'6 hours', current_timestamp + interval'6 hours', '{user_data['carantine']}', '{user_data['def_send']}')""")
        conn.commit()
        cursor.close()
        conn.close()
        await state.set_state(SetParameterFit.send_photo)
