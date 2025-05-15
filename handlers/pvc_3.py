from aiogram import Router, F
from aiogram.filters.command import Command
from aiogram.filters.text import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards.simple_row import make_row_keyboard
from datetime import datetime, timedelta
import psycopg2
from aiogram import Bot
import os
from aiogram.types.photo_size import PhotoSize
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton,ReplyKeyboardBuilder
from aiogram.exceptions import TelegramBadRequest


#token = os.getenv('TOKEN')
token = '7491228760:AAFnb_5APIBYInpumPOgLNsF1D5xl6ItBs8'
bot = Bot(token=token)

router2 = Router()
available_answers = ['ok', 'not ok']
available_shifts = ['A','B','C','back']
available_controllers = ['Daulet', 'Adilet', 'Dinmukhammed']
available_names = ['Anton', 'Aziz', 'Egor','back']
available_tubes = ['okyanus/2,2','okyanus type 2/2,2', 'deniz type 1/4.0', 'deniz type 1/3.2', 'deniz type 2/2.2','back']
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
    choosing_pvc_length_nom = State()
    choosing_pvc_proch = State()
    choosing_pvc_finish = State()
    send_photo = State()
    send_photo_view = State()
    send_photo_view_sent = State()
    send_photo_diameter = State()
    send_photo_diameter_sent = State()
    send_photo_width_s = State()
    send_photo_width_s_sent = State()
    send_photo_control_mark = State()
    send_photo_control_mark_sent = State()
    send_photo_weight = State()
    send_photo_weight_sent = State()
    send_photo_functionality = State()
    send_photo_functionality_sent = State()
    send_photo_proch = State()
    send_photo_proch_sent = State()
    send_photo_length = State()
    send_photo_length_sent = State()
    choosing_defects = State()
    defects_descr = State()
    continue_load = State()
    carantine = State()
    def_send = State()

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
        available_tubes = ['okyanus/2.2', 'deniz type 1/4.0', 'deniz type 1/3.2', 'deniz type 2/2.2','back']
        button1 = KeyboardButton(text='okyanus/1.8',)
        button2 = KeyboardButton(text='deniz type 1/4.0')
        button3 = KeyboardButton(text='deniz type 1/3.2')
        button4 = KeyboardButton(text='deniz type 2/2.2')
        button5 = KeyboardButton(text='back')
        markup1 = ReplyKeyboardBuilder([[button1]]).row(button2).row(button3).row(button4).row(button5).as_markup()
        await message.answer(
            text="выберите бренд PVC трубы:",
            reply_markup=markup1
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
async def pvc_nom_diameter(message: Message, state: FSMContext):
    if message.text == 'back':
        await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
        await state.set_state(SetParameterPVC3.choosing_pvc_name)
    elif message.text == 'go':
        await message.answer(
            text="выберите длину:",
            reply_markup=make_row_keyboard(['250','500','1000','2000','3000'])
        )
        print('choose nom diameter')
        await state.set_state(SetParameterPVC3.choosing_pvc_length_nom)
    else:
        await state.update_data(chosen_nom_diameter=message.text.lower())
        await message.answer(
            text="выберите длину:",
            reply_markup=make_row_keyboard(['250','500','1000','2000','3000'])
        )
        print('choose nom diameter')
        await state.set_state(SetParameterPVC3.choosing_pvc_length_nom)


@router2.message(SetParameterPVC3.choosing_pvc_length_nom)
async def pvc_view(message: Message, state: FSMContext):
    if message.text == 'go':
        await message.answer(
            text="оцените внешний вид PVC трубы:",
            reply_markup=make_row_keyboard(available_answers)
        )
        print('choose view')
        await state.set_state(SetParameterPVC3.choosing_pvc_view)
    else:
        await state.update_data(chosen_length_nom=message.text.lower())
        await message.answer(
            text="оцените внешний вид PVC трубы:",
            reply_markup=make_row_keyboard(available_answers)
        )
        print('choose view')
        await state.set_state(SetParameterPVC3.choosing_pvc_view)

@router2.message(SetParameterPVC3.choosing_pvc_view)
async def get_photo_pprc_view(message: Message, state: FSMContext):
        await state.update_data(chosen_view=message.text.lower())
        await message.answer(
            text="отправьте фото",
            reply_markup=make_row_keyboard(['back'])
        )
        print('choose diameter')
        await state.set_state(SetParameterPVC3.send_photo_view)

@router2.message(SetParameterPVC3.send_photo_view)
async def get_photo_pprc_view(message: Message, state: FSMContext):
    if message.text == 'back':
        await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
        await state.set_state(SetParameterPVC3.choosing_pvc_tube)
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
        filename = 'pvc_view_' + (datetime.now() + timedelta(hours=6)).strftime('%Y-%m-%d %H:%M:%S' + '.jpg')
        await bot.download_file(file_path, filename )
        upload_file_list = [filename]
        for upload_file in upload_file_list:
            gfile = drive.CreateFile({'parents': [{'id': '1Dmbaj2-puU0mOo4s35-Ud-1aF8u-WVmK'}]})
            gfile.SetContentFile(upload_file)
            gfile.Upload()

        await message.answer(
                text="продолжить",
                reply_markup=make_row_keyboard(['yes'])
                )
        await state.set_state(SetParameterPVC3.send_photo_view_sent)


@router2.message(SetParameterPVC3.send_photo_view_sent)
async def pvc_functionality(message: Message, state: FSMContext):
    if message.text == 'go':
        await message.answer(
            text="оцените функциональность PVC трубы:",
            reply_markup=make_row_keyboard(available_answers)
        )
        print('choose functionality')
        await state.set_state(SetParameterPVC3.choosing_pvc_functionality)
    else:
        await message.answer(
            text="оцените функциональность PVC трубы:",
            reply_markup=make_row_keyboard(available_answers)
        )
        print('choose functionality')
        await state.set_state(SetParameterPVC3.choosing_pvc_functionality)


@router2.message(SetParameterPVC3.choosing_pvc_functionality)
async def get_photo_pprc_view(message: Message, state: FSMContext):
        await state.update_data(chosen_functionality=message.text.lower())
        await message.answer(
            text="отправьте видео",
            reply_markup=make_row_keyboard(['back'])
        )
        await state.set_state(SetParameterPVC3.send_photo_functionality)

@router2.message(SetParameterPVC3.send_photo_functionality)
async def get_photo_pprc_view(message: Message, state: FSMContext):
    if message.text == 'back':
        await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
        await state.set_state(SetParameterPVC3.send_photo_view_sent)
    else:
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()           
        drive = GoogleDrive(gauth)  
        file_id =  message.video.file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path
        file_path = file.file_path
        filename = 'pvc_func_' + (datetime.now() + timedelta(hours=6)).strftime('%Y-%m-%d %H:%M:%S' + '.mp4')
        await bot.download_file(file_path, filename )
        upload_file_list = [filename]
        for upload_file in upload_file_list:
            gfile = drive.CreateFile({'parents': [{'id': '1Dmbaj2-puU0mOo4s35-Ud-1aF8u-WVmK'}]})
            gfile.SetContentFile(upload_file)
            gfile.Upload()

        await message.answer(
                text="продолжить",
                reply_markup=make_row_keyboard(['yes'])
                )
        await state.set_state(SetParameterPVC3.send_photo_functionality_sent)

@router2.message(SetParameterPVC3.send_photo_functionality_sent)
async def pvc_diameter(message: Message, state: FSMContext):
    if message.text == 'go':
        await message.answer(
            text="Теперь укажите диаметр PVC трубы:",
            reply_markup=ReplyKeyboardRemove()
        )
        print('choose diameter')
        await state.set_state(SetParameterPVC3.choosing_pvc_diameter)
    else:
        
        await message.answer(
            text="Теперь укажите диаметр PVC трубы:",
            reply_markup=ReplyKeyboardRemove()
        )
        print('choose diameter')
        await state.set_state(SetParameterPVC3.choosing_pvc_diameter)

@router2.message(SetParameterPVC3.choosing_pvc_diameter)
async def get_photo_pprc_view(message: Message, state: FSMContext):
        await state.update_data(chosen_diameter=message.text.lower())
        await message.answer(
            text="отправьте фото",
            reply_markup=make_row_keyboard(['back'])
        )
        await state.set_state(SetParameterPVC3.send_photo_diameter)

@router2.message(SetParameterPVC3.send_photo_diameter)
async def get_photo_pprc_view(message: Message, state: FSMContext):
    if message.text == 'back':
        await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
        await state.set_state(SetParameterPVC3.send_photo_functionality_sent)
    else:
        
        file_id = message.photo[-1].file_id
        file_unique_id = message.photo[-1].file_unique_id

        # Сначала загружаем файл с Telegram
        try:
            file = await bot.get_file(file_id)
            file_path = file.file_path
            filename = 'pvc_diameter_' + (datetime.now() + timedelta(hours=6)).strftime('%Y-%m-%d %H:%M:%S') + '.jpg'
            await bot.download_file(file_path, filename)
        except TelegramBadRequest:
            await message.answer("Не удалось скачать файл. Попробуйте отправить заново.")
            return

        # Теперь, когда файл уже локально скачан, авторизуемся в Google
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()
        drive = GoogleDrive(gauth)

        # Загружаем файл в Google Drive
        upload_file_list = [filename]
        for upload_file in upload_file_list:
            gfile = drive.CreateFile({'parents': [{'id': '1Dmbaj2-puU0mOo4s35-Ud-1aF8u-WVmK'}]})
            gfile.SetContentFile(upload_file)
            gfile.Upload()

        await message.answer(
            text="продолжить",
            reply_markup=make_row_keyboard(['yes'])
        )
        await state.set_state(SetParameterPVC3.send_photo_diameter_sent)



@router2.message(SetParameterPVC3.send_photo_diameter_sent)
async def pvc_weight(message: Message, state: FSMContext):
    if message.text =='go':
        await message.answer(
            text="Оцените прочность PVC трубы:",
            reply_markup=make_row_keyboard(available_answers)
        )
        print('choose proch')
        await state.set_state(SetParameterPVC3.choosing_pvc_proch)
    else:
        await message.answer(
            text="Оцените прочность PVC трубы:",
            reply_markup=make_row_keyboard(available_answers)
        )
        print('choose weight')
        await state.set_state(SetParameterPVC3.choosing_pvc_proch)

@router2.message(SetParameterPVC3.choosing_pvc_proch)
async def get_photo_pprc_view(message: Message, state: FSMContext):
        await state.update_data(chosen_proch=message.text.lower())
        await message.answer(
            text="отправьте видео",
            reply_markup=make_row_keyboard(['back'])
        )
        await state.set_state(SetParameterPVC3.send_photo_proch)


@router2.message(SetParameterPVC3.send_photo_proch)
async def get_photo_pprc_view(message: Message, state: FSMContext):
    if message.text == 'back':
        await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
        await state.set_state(SetParameterPVC3.send_photo_diameter_sent)
    else:
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()           
        drive = GoogleDrive(gauth)  
        file_id =  message.video.file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path
        filename = 'pvc_strength_' + (datetime.now() + timedelta(hours=6)).strftime('%Y-%m-%d %H:%M:%S' + '.mp4')
        await bot.download_file(file_path, filename )
        upload_file_list = [filename]
        for upload_file in upload_file_list:
            gfile = drive.CreateFile({'parents': [{'id': '1Dmbaj2-puU0mOo4s35-Ud-1aF8u-WVmK'}]})
            gfile.SetContentFile(upload_file)
            gfile.Upload()

        await message.answer(
                text="продолжить",
                reply_markup=make_row_keyboard(['yes'])
                )
        await state.set_state(SetParameterPVC3.send_photo_proch_sent)



@router2.message(SetParameterPVC3.send_photo_proch_sent)
async def pvc_weight(message: Message, state: FSMContext):
    if message.text =='go':
        await message.answer(
            text="Теперь укажите вес PVC трубы:",
            reply_markup=ReplyKeyboardRemove()
        )
        print('choose weight')
        await state.set_state(SetParameterPVC3.choosing_pvc_weight)
    else:
        await message.answer(
            text="Теперь укажите вес PVC трубы:",
            reply_markup=ReplyKeyboardRemove()
        )
        print('choose weight')
        await state.set_state(SetParameterPVC3.choosing_pvc_weight)

@router2.message(SetParameterPVC3.choosing_pvc_weight)
async def get_photo_pprc_view(message: Message, state: FSMContext):
        await state.update_data(chosen_weight=message.text.lower())
        await message.answer(
            text="отправьте фото",
            reply_markup=make_row_keyboard(['back'])
        )
        await state.set_state(SetParameterPVC3.send_photo_weight)

@router2.message(SetParameterPVC3.send_photo_weight)
async def get_photo_pprc_view(message: Message, state: FSMContext):
    if message.text == 'back':
        await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
        await state.set_state(SetParameterPVC3.send_photo_proch_sent)
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
        filename = 'pvc_weight_' + (datetime.now() + timedelta(hours=6)).strftime('%Y-%m-%d %H:%M:%S' + '.jpg')
        await bot.download_file(file_path, filename )
        upload_file_list = [filename]
        for upload_file in upload_file_list:
            gfile = drive.CreateFile({'parents': [{'id': '1Dmbaj2-puU0mOo4s35-Ud-1aF8u-WVmK'}]})
            gfile.SetContentFile(upload_file)
            gfile.Upload()

        await message.answer(
                text="продолжить",
                reply_markup=make_row_keyboard(['yes'])
                )
        await state.set_state(SetParameterPVC3.send_photo_weight_sent)


@router2.message(SetParameterPVC3.send_photo_weight_sent)
async def get_photo_pprc_view(message: Message, state: FSMContext):

        await message.answer(
            text="Есть ли дефекты?",
            reply_markup=make_row_keyboard(['yes','no'])
        )
        print('choose defects')
        await state.set_state(SetParameterPVC3.choosing_defects)


@router2.message(SetParameterPVC3.choosing_defects)
async def get_photo_pprc_view(message: Message, state: FSMContext):
        await state.update_data(chosen_def=message.text.lower())
        if message.text == 'yes':
            await message.answer(
                text="Введите описание дефекта",
                reply_markup=ReplyKeyboardRemove()
            )
            print('choose defects')
            await state.set_state(SetParameterPVC3.defects_descr)
        else:
            await message.answer(
                text="продолжить",
                reply_markup=make_row_keyboard(['yes'])
            )
            print('choose defects')
            await state.set_state(SetParameterPVC3.def_send)


@router2.message(SetParameterPVC3.defects_descr)
async def get_photo_pprc_view(message: Message, state: FSMContext):
        await state.update_data(chosen_def_descr=message.text.lower())
        await message.answer(
                text="сколько штук поставлено в карантин",
                reply_markup=ReplyKeyboardRemove()
            )
        await state.set_state(SetParameterPVC3.carantine)

@router2.message(SetParameterPVC3.carantine)
async def get_photo_pprc_view(message: Message, state: FSMContext):
        await state.update_data(carantine=message.text.lower())
        await message.answer(
                text="сколько штук ушло в брак?",
                reply_markup=ReplyKeyboardRemove()
            )
        await state.set_state(SetParameterPVC3.def_send)

@router2.message(SetParameterPVC3.def_send)
async def continue_load(message: Message, state: FSMContext):
    if (datetime.now()+ timedelta(hours = 6)).hour in [2,5,8,11,14,15, 17,20,23]:
        if message.text != 'yes':
                await state.update_data(def_send=message.text.lower().replace(',', '.'))
                
        else:
                await state.update_data(def_send='')
        await message.answer(
                    text='продолжить заполнение данных',
                    reply_markup=make_row_keyboard(['yes'])
                )
        await state.set_state(SetParameterPVC3.continue_load)
    elif (datetime.now()+ timedelta(hours = 6)).hour in [0,1,3,4,6,7,9,10,12,13,15,16,18,19,21,22]:
        if message.text == 'back':
            await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
            await state.set_state(SetParameterPVC3.send_photo_weight_sent)
        else:
            await state.update_data(def_send=message.text.lower().replace(',', '.'))
            await message.answer(
                    text="перейти к передаче данных",
                    reply_markup=make_row_keyboard(available_proceeds)
            )
            await state.set_state(SetParameterPVC3.choosing_pvc_finish)

@router2.message(SetParameterPVC3.continue_load)
async def pvc_width(message: Message, state: FSMContext):
    if message.text == 'yes':
            await message.answer(
                    text="Теперь укажите толщину PVC трубы:",
                    reply_markup=ReplyKeyboardRemove()
            )
            print('choose width')
            await state.set_state(SetParameterPVC3.choosing_pvc_width)

@router2.message(SetParameterPVC3.choosing_pvc_width)
async def get_photo_pprc_view(message: Message, state: FSMContext):
        await state.update_data(chosen_width=message.text.lower())
        await message.answer(
            text="отправьте фото",
            reply_markup=make_row_keyboard(['back'])
        )
        await state.set_state(SetParameterPVC3.send_photo_width_s)

@router2.message(SetParameterPVC3.send_photo_width_s)
async def get_photo_pprc_view(message: Message, state: FSMContext):
    if message.text == 'back':
        await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
        await state.set_state(SetParameterPVC3.defects_descr)
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
        filename = 'pvc_width_' + (datetime.now() + timedelta(hours=6)).strftime('%Y-%m-%d %H:%M:%S' + '.jpg')
        await bot.download_file(file_path, filename )
        upload_file_list = [filename]
        for upload_file in upload_file_list:
            gfile = drive.CreateFile({'parents': [{'id': '1Dmbaj2-puU0mOo4s35-Ud-1aF8u-WVmK'}]})
            gfile.SetContentFile(upload_file)
            gfile.Upload()

        await message.answer(
                text="продолжить",
                reply_markup=make_row_keyboard(['yes'])
                )
        await state.set_state(SetParameterPVC3.send_photo_width_s_sent)


    
@router2.message(SetParameterPVC3.send_photo_width_s_sent)
async def pvc_length(message: Message, state: FSMContext):
    if message.text == 'go':
        await message.answer(
                text="Теперь укажите длину PVC трубы:",
                reply_markup=ReplyKeyboardRemove()
        )
        print('choose length')
        await state.set_state(SetParameterPVC3.choosing_pvc_length)
    else:
        await message.answer(
                text="Теперь укажите длину PVC трубы:",
                reply_markup=ReplyKeyboardRemove()
        )
        print('choose length')
        await state.set_state(SetParameterPVC3.choosing_pvc_length)

@router2.message(SetParameterPVC3.choosing_pvc_length)
async def get_photo_pprc_view(message: Message, state: FSMContext):
        await state.update_data(chosen_length=message.text.lower())
        await message.answer(
            text="отправьте фото",
            reply_markup=make_row_keyboard(['back'])
        )
        await state.set_state(SetParameterPVC3.send_photo_length)

@router2.message(SetParameterPVC3.send_photo_length)
async def get_photo_pprc_view(message: Message, state: FSMContext):
    if message.text == 'back':
        await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
        await state.set_state(SetParameterPVC3.send_photo_width_s_sent)
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
        filename = 'pvc_length_' + (datetime.now() + timedelta(hours=6)).strftime('%Y-%m-%d %H:%M:%S' + '.jpg')
        await bot.download_file(file_path, filename )
        upload_file_list = [filename]
        for upload_file in upload_file_list:
            gfile = drive.CreateFile({'parents': [{'id': '1Dmbaj2-puU0mOo4s35-Ud-1aF8u-WVmK'}]})
            gfile.SetContentFile(upload_file)
            gfile.Upload()

        await message.answer(
                text="продолжить",
                reply_markup=make_row_keyboard(['yes'])
                )
        await state.set_state(SetParameterPVC3.send_photo_length_sent)

@router2.message(SetParameterPVC3.send_photo_length_sent)
async def pvc_length(message: Message, state: FSMContext):
    if message.text == 'go':
        await message.answer(
                text="Оцените контрольную маркировку PVC трубы:",
                reply_markup=make_row_keyboard(available_answers)
        )
        print('choose length')
        await state.set_state(SetParameterPVC3.choosing_pvc_control_mark)
    else:
        await message.answer(
                text="Оцените контрольную маркировку PVC трубы:",
                reply_markup=make_row_keyboard(available_answers)
        )
        print('choose length')
        await state.set_state(SetParameterPVC3.choosing_pvc_control_mark)

@router2.message(SetParameterPVC3.choosing_pvc_control_mark)
async def get_photo_pprc_view(message: Message, state: FSMContext):
        await state.update_data(chosen_control_mark=message.text.lower())
        await message.answer(
            text="отправьте фото",
            reply_markup=make_row_keyboard(['back'])
        )
        await state.set_state(SetParameterPVC3.send_photo_control_mark)

@router2.message(SetParameterPVC3.send_photo_control_mark)
async def get_photo_pprc_view(message: Message, state: FSMContext):
    if message.text == 'back':
        await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
        await state.set_state(SetParameterPVC3.send_photo_length_sent)
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
        filename = 'pvc_diameter_' + (datetime.now() + timedelta(hours=6)).strftime('%Y-%m-%d %H:%M:%S' + '.jpg')
        await bot.download_file(file_path, filename )
        upload_file_list = [filename]
        for upload_file in upload_file_list:
            gfile = drive.CreateFile({'parents': [{'id': '1Dmbaj2-puU0mOo4s35-Ud-1aF8u-WVmK'}]})
            gfile.SetContentFile(upload_file)
            gfile.Upload()

        await message.answer(
                text="продолжить",
                reply_markup=make_row_keyboard(['yes'])
                )
        await state.set_state(SetParameterPVC3.send_photo_control_mark_sent)





@router2.message(SetParameterPVC3.send_photo_control_mark_sent)
async def pvc_finish(message: Message, state: FSMContext):
        if message.text == 'go':
            await message.answer(
                text="перейти к передаче данных",
                reply_markup=make_row_keyboard(available_proceeds)
            )
            await state.set_state(SetParameterPVC3.choosing_pvc_finish)
        else:
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
                text="Благодарю за заполненные данные",
                reply_markup=ReplyKeyboardRemove()
            )
            print('success 6 params')
            if ('carantine' in user_data.keys()) == False:
                user_data['carantine'] = '0'
                user_data['def_send'] = '0'
                user_data['chosen_def_descr'] = ' '
            conn = psycopg2.connect('postgresql://neondb_owner:npg_qKfatzsHP75o@ep-blue-lake-a4lt99hy-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require')
            cursor = conn.cursor()
            cursor.execute(f"""insert into pvc_params (WORKING,CONTROLLER_NAME, SHIFT, BRAND, NOMINAL_DIAMETER, nominal_length, VIEW, FUNCTIONALITY, DIAMETER, WEIGHT,WIDTH,MARK_CONTROL,LENGTH,STRENGTH, MASTER, DEFECT,DEFECT_DESCR, created_at, updated_at, carantine_num,defect_num) values (TRUE,'{user_data['chosen_controller_name']}','{user_data['chosen_smena']}','{user_data['chosen_tube']}', '{user_data['chosen_nom_diameter']}','{user_data['chosen_length_nom']}', '{user_data['chosen_view']}','{user_data['chosen_functionality']}',{user_data['chosen_diameter']}, {user_data['chosen_weight']}, {user_data['chosen_width']}, '{user_data['chosen_control_mark']}', '{user_data['chosen_length']}', '{user_data['chosen_proch']}','{user_data['chosen_name']}','{user_data['chosen_def']}', '{user_data['chosen_def_descr']}',  current_timestamp + interval'6 hours', current_timestamp + interval'6 hours','{user_data['carantine']}', '{user_data['def_send']}')""")
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
                text="Благодарю за заполненные данные",
                reply_markup=ReplyKeyboardRemove()
            )
            if ('carantine' in user_data.keys()) == False:
                user_data['carantine'] = '0'
                user_data['def_send'] = '0'
                user_data['chosen_def_descr'] = ' '
            conn = psycopg2.connect('postgresql://neondb_owner:npg_qKfatzsHP75o@ep-blue-lake-a4lt99hy-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require')
            cursor = conn.cursor()
            cursor.execute(f"""insert into pvc_params (WORKING,CONTROLLER_NAME, SHIFT, BRAND, NOMINAL_DIAMETER, nominal_length, VIEW, FUNCTIONALITY, DIAMETER, WEIGHT, MASTER, DEFECT,DEFECT_DESCR, created_at, updated_at, carantine_num, defect_num) values (TRUE, '{user_data['chosen_controller_name']}','{user_data['chosen_smena']}', '{user_data['chosen_tube']}', '{user_data['chosen_nom_diameter']}','{user_data['chosen_length_nom']}','{user_data['chosen_view']}', '{user_data['chosen_functionality']}', {user_data['chosen_diameter']},  {user_data['chosen_weight']}, '{user_data['chosen_name']}','{user_data['chosen_def']}', '{user_data['chosen_def_descr']}', current_timestamp + interval'6 hours', current_timestamp + interval'6 hours','{user_data['carantine']}', '{user_data['def_send']}')""")
            conn.commit()
            cursor.close()
            conn.close()
            await state.set_state(SetParameterPVC3.send_photo)
    else:
        await message.answer(
            text="В данный момент работы не ведутся",
            reply_markup=ReplyKeyboardRemove()
        )
