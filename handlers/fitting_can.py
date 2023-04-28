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
from aiogram.types.photo_size import PhotoSize
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from aiogram import Bot
import os
token = os.getenv('TOKEN')
bot = Bot(token=token)

router = Router()
available_answers = ['ok', 'not ok','back']
available_shifts = ['A','B','C','back']
available_controllers = ['Madi', 'Adilet', 'Magzhan']
available_masters_fitting = ['Salamat', 'Dauren', 'Anton','back']
available_tubes = ['okyanus', 'deniz','kavi','back']
available_diameters = ['50','110','back']
available_proceeds = ['yes','back']
available_stanoks = ['1','2','3','4','5','6','back']


class SetParameterFitCanal(StatesGroup):
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
    choosing_fitting_weight = State()
    send_photo = State()
    send_photo_weight = State()
    send_photo_weight_sent = State()
    send_photo_func = State()
    send_photo_func_sent = State()
    send_photo_view = State()
    send_photo_view_sent = State()
    choosing_defects = State()
    defects_descr = State()

@router.message(Text(text='работает фиттинг канализ'))
async def fitting_controller(message: Message, state: FSMContext):
    
    await message.answer(
        text="Выберите контроллера",
        reply_markup=make_row_keyboard(available_controllers)
    )
    print('choose controller canal')
    await state.set_state(SetParameterFitCanal.choosing_fitting_controller)

# @router.message(SetParameterFitCanal.choosing_fitting_controller)
# async def fitting_smena(message: Message, state: FSMContext):
#     if message.text == 'go':
        
#         await message.answer(
#             text="Выберите смену ",
#             reply_markup=make_row_keyboard(available_shifts)
#         )
#         print('choose smena canal')
#         await state.set_state(SetParameterFitCanal.choosing_fitting_smena)
#     else:
#         await state.update_data(chosen_controller_name=message.text.lower())
#         await message.answer(
#             text="Выберите смену ",
#             reply_markup=make_row_keyboard(available_shifts)
#         )
#         print('choose smena canal')
#         await state.set_state(SetParameterFitCanal.choosing_fitting_smena)



@router.message(SetParameterFitCanal.choosing_fitting_controller)
async def pprc_name(message: Message, state: FSMContext):
    # if message.text == 'back':
    #     await message.answer(
    #         text="go back",
    #         reply_markup=make_row_keyboard(['go'])
    #         )
    #     await state.set_state(SetParameterFitCanal.choosing_fitting_controller)
    # el
    if message.text == 'go':
        await message.answer(
            text="Кто является мастером на линии на текущий час ?",
            reply_markup=make_row_keyboard(available_masters_fitting)
        )
        print('choose master canal')
        await state.set_state(SetParameterFitCanal.choosing_fitting_name)
    else:
        await state.update_data(chosen_controller_name=message.text.lower())
        await message.answer(
            text="Кто является мастером на линии на текущий час ?",
            reply_markup=make_row_keyboard(available_masters_fitting)
        )
        print('choose master canal')
        await state.set_state(SetParameterFitCanal.choosing_fitting_name)


@router.message(SetParameterFitCanal.choosing_fitting_name)
async def pprc_tube(message: Message, state: FSMContext):
    if message.text == 'back':
        await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
        await state.set_state(SetParameterFitCanal.choosing_fitting_controller)
    elif message.text == 'go':
        await message.answer(
        text="Выберите бренд фиттинга:",
        reply_markup=make_row_keyboard(available_tubes)
    )
        print('choose brand canal')
        await state.set_state(SetParameterFitCanal.choosing_fitting_tube_1)
    else:
    
        await state.update_data(chosen_name=message.text.lower())
        await message.answer(
            text="Выберите бренд фиттинга:",
            reply_markup=make_row_keyboard(available_tubes)
        )
        print('choose brand canal')
        await state.set_state(SetParameterFitCanal.choosing_fitting_tube_1)

@router.message(SetParameterFitCanal.choosing_fitting_tube_1)
async def pprc_tube(message: Message, state: FSMContext):
    if message.text == 'back':
        await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
        await state.set_state(SetParameterFitCanal.choosing_fitting_smena)
    elif message.text == 'go':
        button1 = KeyboardButton(text='КРЕСТОВИНА ')
        button2 = KeyboardButton(text='МУФТА ')
        button3 = KeyboardButton(text='ОТВОД ')
        button4 = KeyboardButton(text='ТРОЙНИК ')
        button5 = KeyboardButton(text='РЕВИЗИЯ ')
        button6 = KeyboardButton(text='ЗАГЛУШКА ')
        button7 = KeyboardButton(text='ХОМУТ ')
        button8 = KeyboardButton(text='БУТЫЛКА ')
        button9 = KeyboardButton(text='КРЫШКА РЕВИЗИИ ')
        button10 = KeyboardButton(text='back')
            
        markup1 = ReplyKeyboardBuilder([[button1]]).row(button2).row(button3).row(button4).row(button5).row(button6).row(button7).row(button8).row(button9).row(button10).as_markup()
        
        await message.answer(
            text='Выберите наименование продукции',
            reply_markup=markup1
        )
        print('choose fit name 1 canal ')
        await state.set_state(SetParameterFitCanal.choosing_fitting_tube_2)
    else:
            button1 = KeyboardButton(text='КРЕСТОВИНА ')
            button2 = KeyboardButton(text='МУФТА ')
            button3 = KeyboardButton(text='ОТВОД ')
            button4 = KeyboardButton(text='ТРОЙНИК ')
            button5 = KeyboardButton(text='РЕВИЗИЯ ')
            button6 = KeyboardButton(text='ЗАГЛУШКА ')
            button7 = KeyboardButton(text='ХОМУТ ')
            button8 = KeyboardButton(text='БУТЫЛКА ')
            button9 = KeyboardButton(text='КРЫШКА РЕВИЗИИ ')
            button10 = KeyboardButton(text='back')
                
            markup1 = ReplyKeyboardBuilder([[button1]]).row(button2).row(button3).row(button4).row(button5).row(button6).row(button7).row(button8).row(button9).row(button10).as_markup()
            await state.update_data(chosen_tube=message.text.lower())
            await message.answer(
                text='Выберите наименование продукции',
                reply_markup=markup1
            )
            print('choose fit name 1 canal ')
            await state.set_state(SetParameterFitCanal.choosing_fitting_tube_2)


@router.message(SetParameterFitCanal.choosing_fitting_tube_2)
async def pprc_tube(message: Message, state: FSMContext):
    if message.text == 'back':
        await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
        await state.set_state(SetParameterFitCanal.choosing_fitting_name)
    elif message.text == 'go':
        button1 = KeyboardButton(text='110')
        button2 = KeyboardButton(text='50')
        button3 = KeyboardButton(text='50*45')
        button4 = KeyboardButton(text='50*90')
        button5 = KeyboardButton(text='110*45')    
        button6 = KeyboardButton(text='110*90')
        button7 = KeyboardButton(text='50*50') 

        button8 = KeyboardButton(text='110*50')
        button9 = KeyboardButton(text='110*110')
        button10 = KeyboardButton(text='110*110*90')
        button11 = KeyboardButton(text='back')


        markup1 = ReplyKeyboardBuilder([[button1]]).row(button2).row(button3).row(button4).row(button5).row(button6).row(button7).row(button8).row(button9).row(button10).row(button11).as_markup()
        
        await message.answer(
            text='Выберите размер',
            reply_markup=markup1
        )
        print('choose fit name 3')
        await state.set_state(SetParameterFitCanal.choosing_fitting_tube_3)
    else:
        button1 = KeyboardButton(text='110')
        button2 = KeyboardButton(text='50')
        button3 = KeyboardButton(text='50*45')
        button4 = KeyboardButton(text='50*90')
        button5 = KeyboardButton(text='110*45')    
        button6 = KeyboardButton(text='110*90')
        button7 = KeyboardButton(text='50*50') 
        button8 = KeyboardButton(text='110*50')
        button9 = KeyboardButton(text='110*110')
        button10 = KeyboardButton(text='110*110*90')
        button11 = KeyboardButton(text='back')

        markup1 = ReplyKeyboardBuilder([[button1]]).row(button2).row(button3).row(button4).row(button5).row(button6).row(button7).row(button8).row(button9).row(button10).row(button11).as_markup()
        await state.update_data(chosen_fit_name_1=message.text.lower())
        await message.answer(
            text='Выберите размер',
            reply_markup=markup1
        )
        print('choose fit name 3')
        await state.set_state(SetParameterFitCanal.choosing_fitting_tube_3)

@router.message(SetParameterFitCanal.choosing_fitting_tube_3)
async def pprc_tube(message: Message, state: FSMContext):
    if message.text == 'back':
        await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
        await state.set_state(SetParameterFitCanal.choosing_fitting_tube_1)
    elif message.text == 'go':

        button1 = KeyboardButton(text='прямой')
        button2 = KeyboardButton(text='косой')
        button3 = KeyboardButton(text='back')
        markup1 = ReplyKeyboardBuilder([[button1]]).row(button2).row(button3).as_markup()
        await message.answer(
            text='Выберите тип продукции',
            reply_markup=markup1
        )
        print('choose fit name 3')
        await state.set_state(SetParameterFitCanal.choosing_fitting_tube_4)
    else:
        button1 = KeyboardButton(text='прямой')
        button2 = KeyboardButton(text='косой')
        button3 = KeyboardButton(text='back')
        markup1 = ReplyKeyboardBuilder([[button1]]).row(button2).row(button3).as_markup()
        await state.update_data(chosen_fit_name_2=message.text.lower())
        await message.answer(
            text='Выберите тип продукции',
            reply_markup=markup1
        )
        print('choose fit name 3')
        await state.set_state(SetParameterFitCanal.choosing_fitting_tube_4)


@router.message(SetParameterFitCanal.choosing_fitting_tube_4)
async def pprc_tube(message: Message, state: FSMContext):
    if message.text == 'back':
        await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
        await state.set_state(SetParameterFitCanal.choosing_fitting_tube_2)
    elif message.text == 'go':
        button1 = KeyboardButton(text='PP')
        button2 = KeyboardButton(text='PVC')
        button3 = KeyboardButton(text='back')
        markup1 = ReplyKeyboardBuilder([[button1]]).row(button2).row(button3).as_markup()
        await message.answer(
            text='Выберите тип сырья ',
            reply_markup=markup1
        )
        print('choose fit name_4')
        await state.set_state(SetParameterFitCanal.choosing_fitting_tube_5)
    else:
        button1 = KeyboardButton(text='PP')
        button2 = KeyboardButton(text='PVC')
        button3 = KeyboardButton(text='back')
        markup1 = ReplyKeyboardBuilder([[button1]]).row(button2).row(button3).as_markup()
        await state.update_data(chosen_fit_name_3=message.text.lower())
        await message.answer(
            text='Выберите тип сырья ',
            reply_markup=markup1
        )
        print('choose fit name_4')
        await state.set_state(SetParameterFitCanal.choosing_fitting_tube_5)


@router.message(SetParameterFitCanal.choosing_fitting_tube_5)
async def pprc_nom_diameter(message: Message, state: FSMContext):
    if message.text == 'back':
        await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
        await state.set_state(SetParameterFitCanal.choosing_fitting_tube_3)
    elif message.text == 'go':
        await message.answer(
            text="выберите номинальный диаметр фиттинга:",
            reply_markup=make_row_keyboard(available_diameters)
        )
        print('choose nom diameter')
        await state.set_state(SetParameterFitCanal.choosing_fitting_nom_diameter)
    else:
        await state.update_data(chosen_fit_name_4=message.text.lower())
        await message.answer(
            text="выберите номинальный диаметр фиттинга:",
            reply_markup=make_row_keyboard(available_diameters)
        )
        print('choose nom diameter')
        await state.set_state(SetParameterFitCanal.choosing_fitting_nom_diameter)

@router.message(SetParameterFitCanal.choosing_fitting_nom_diameter)
async def pprc_view(message: Message, state: FSMContext):
    if message.text == 'back':
        await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
        await state.set_state(SetParameterFitCanal.choosing_fitting_tube_4)
    elif message.text == 'go':
        
        await message.answer(
            text="оцените внешний вид фиттинга:",
            reply_markup=make_row_keyboard(available_answers)
        )
        print('choose view')
        await state.set_state(SetParameterFitCanal.choosing_fitting_view)
    else:
        await state.update_data(chosen_nom_diameter=message.text.lower())
        await message.answer(
            text="оцените внешний вид фиттинга:",
            reply_markup=make_row_keyboard(available_answers)
        )
        print('choose view')
        await state.set_state(SetParameterFitCanal.choosing_fitting_view)


@router.message(SetParameterFitCanal.choosing_fitting_view)
async def get_photo_pprc_view(message: Message, state: FSMContext):
        await state.update_data(chosen_view=message.text.lower())
        await message.answer(
            text="отправьте фото",
            reply_markup=make_row_keyboard(['back'])
        )
        print('choose diameter')
        await state.set_state(SetParameterFitCanal.send_photo_view)

@router.message(SetParameterFitCanal.send_photo_view)
async def get_photo_pprc_view(message: Message, state: FSMContext, bot):
    if message.text == 'back':
        await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
        await state.set_state(SetParameterFitCanal.choosing_fitting_nom_diameter)
    else:
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()           
        drive = GoogleDrive(gauth)  
        file_id =  message.photo[-1].file_id
        print(message.photo[-1])
        file_unique_id = message.photo[-1].file_unique_id
        PhotoSize(file_id=file_id, file_unique_id=file_unique_id, width='1920', height='1080')
        file = await bot.get_file(file_id)
        file_path = file.file_path
        filename = 'fitting_canal_view_' + (datetime.now() + timedelta(hours=6)).strftime('%Y-%m-%d %H:%M:%S' + '.jpg')
        await bot.download_file(file_path, filename )
        upload_file_list = [filename]
        for upload_file in upload_file_list:
            gfile = drive.CreateFile({'parents': [{'id': '1ARI8PS_-W0lqY9OXW3l_CmsXuk-c5reK'}]})
            gfile.SetContentFile(upload_file)
            gfile.Upload()

        await message.answer(
                text="продолжить",
                reply_markup=make_row_keyboard(['yes'])
                )
        await state.set_state(SetParameterFitCanal.send_photo_view_sent)


@router.message(SetParameterFitCanal.send_photo_view_sent)
async def pprc_functionality(message: Message, state: FSMContext):
    if message.text == 'go':
        await message.answer(
            text="оцените функциональность фиттинга:",
            reply_markup=make_row_keyboard(available_answers)
        )
        print('choose func')
        await state.set_state(SetParameterFitCanal.choosing_fitting_functionality)
    else:
        await message.answer(
            text="оцените функциональность фиттинга:",
            reply_markup=make_row_keyboard(available_answers)
        )
        print('choose func')
        await state.set_state(SetParameterFitCanal.choosing_fitting_functionality)

@router.message(SetParameterFitCanal.choosing_fitting_functionality)
async def get_photo_pprc_view(message: Message, state: FSMContext):
        await state.update_data(chosen_functionality=message.text.lower())
        await message.answer(
            text="отправьте видео",
            reply_markup=make_row_keyboard(['back'])
        )
        print('choose diameter')
        await state.set_state(SetParameterFitCanal.send_photo_func)

@router.message(SetParameterFitCanal.send_photo_func)
async def get_photo_pprc_view(message: Message, state: FSMContext, bot):
    if message.text == 'back':
        await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
        await state.set_state(SetParameterFitCanal.send_photo_view_sent)
    else:
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()           
        drive = GoogleDrive(gauth)  
        file_id =  message.video.file_id
        # file_unique_id = message.photo[-1].file_unique_id
        # PhotoSize(file_id=file_id, file_unique_id=file_unique_id, width='1920', height='1080')
        file = await bot.get_file(file_id)
        file_path = file.file_path
        filename = 'fitting_canal_func' + (datetime.now() + timedelta(hours=6)).strftime('%Y-%m-%d %H:%M:%S' + '.mp4')
        await bot.download_file(file_path, filename )
        upload_file_list = [filename]
        for upload_file in upload_file_list:
            gfile = drive.CreateFile({'parents': [{'id': '1ARI8PS_-W0lqY9OXW3l_CmsXuk-c5reK'}]})
            gfile.SetContentFile(upload_file)
            gfile.Upload()

        await message.answer(
                text="продолжить",
                reply_markup=make_row_keyboard(['yes'])
                )
        await state.set_state(SetParameterFitCanal.send_photo_func_sent)


@router.message(SetParameterFitCanal.send_photo_func_sent)
async def pprc_functionality(message: Message, state: FSMContext):
    if message.text == 'go':
        await message.answer(
            text="Введите вес фиттинга:",
            reply_markup=ReplyKeyboardRemove()
        )
        print('choose func')
        await state.set_state(SetParameterFitCanal.choosing_fitting_weight)
    else:
        await message.answer(
            text="Введите вес фиттинга:",
            reply_markup=ReplyKeyboardRemove()
        )
        print('choose func')
        await state.set_state(SetParameterFitCanal.choosing_fitting_weight)

@router.message(SetParameterFitCanal.choosing_fitting_weight)
async def get_photo_pprc_view(message: Message, state: FSMContext):
        await state.update_data(chosen_weight=message.text.lower())
        await message.answer(
            text="отправьте фото",
            reply_markup=make_row_keyboard(['back'])
        )
        print('choose diameter')
        await state.set_state(SetParameterFitCanal.send_photo_weight)

@router.message(SetParameterFitCanal.send_photo_weight)
async def get_photo_pprc_view(message: Message, state: FSMContext, bot):
    if message.text == 'back':
        await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
        await state.set_state(SetParameterFitCanal.send_photo_func_sent)
    else:
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()           
        drive = GoogleDrive(gauth)  
        file_id =  message.photo[-1].file_id
        print(message.photo[-1])
        file_unique_id = message.photo[-1].file_unique_id
        PhotoSize(file_id=file_id, file_unique_id=file_unique_id, width='1920', height='1080')
        file = await bot.get_file(file_id)
        file_path = file.file_path
        filename = 'fitting_canal_weight_' + (datetime.now() + timedelta(hours=6)).strftime('%Y-%m-%d %H:%M:%S' + '.jpg')
        await bot.download_file(file_path, filename )
        upload_file_list = [filename]
        for upload_file in upload_file_list:
            gfile = drive.CreateFile({'parents': [{'id': '1ARI8PS_-W0lqY9OXW3l_CmsXuk-c5reK'}]})
            gfile.SetContentFile(upload_file)
            gfile.Upload()

        await message.answer(
                text="продолжить",
                reply_markup=make_row_keyboard(['yes'])
                )
        await state.set_state(SetParameterFitCanal.send_photo_weight_sent)

@router.message(SetParameterFitCanal.send_photo_weight_sent)
async def get_photo_pprc_view(message: Message, state: FSMContext):
        await message.answer(
            text="Есть ли дефекты?",
            reply_markup=make_row_keyboard(['yes','no'])
        )
        print('choose defects')
        await state.set_state(SetParameterFitCanal.choosing_defects)


@router.message(SetParameterFitCanal.choosing_defects)
async def get_photo_pprc_view(message: Message, state: FSMContext):
        await state.update_data(chosen_def=message.text.lower())
        if message.text == 'yes':
            await message.answer(
                text="Введите описание дефекта",
                reply_markup=ReplyKeyboardRemove()
            )
            print('choose defects')
            await state.set_state(SetParameterFitCanal.defects_descr)
        else:
            await message.answer(
                text="продолжить",
                reply_markup=make_row_keyboard(['yes'])
            )
            print('choose defects')
            await state.set_state(SetParameterFitCanal.defects_descr)



@router.message(SetParameterFitCanal.defects_descr)
async def pprc_finish(message: Message, state: FSMContext):
    if message.text == 'go':
        await message.answer(
                text="перейти к передаче данных",
                reply_markup=make_row_keyboard(available_proceeds)
        )
        await state.set_state(SetParameterFitCanal.choosing_fitting_finish)
    else:
        if message.text != 'yes':
                await state.update_data(chosen_def_descr=message.text.lower().replace(',', '.'))
        else:
                await state.update_data(chosen_def_descr='')
        await message.answer(
                text="перейти к передаче данных",
                reply_markup=make_row_keyboard(available_proceeds)
        )
        await state.set_state(SetParameterFitCanal.choosing_fitting_finish)


@router.message(SetParameterFitCanal.choosing_fitting_finish, F.text.in_(available_proceeds))
async def fitting_chosen(message: Message, state: FSMContext):
    if message.text == 'back':
        await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
        await state.set_state(SetParameterFitCanal.choosing_fitting_view)
    else:

        user_data = await state.get_data()
        await message.answer(text=" ".join([str(i[1]) for i in user_data.items()]) + " " + message.text.lower())
        await state.clear()
        await message.answer(
                text="Благодарю за заполненные данные",
                reply_markup=ReplyKeyboardRemove()
        )
        print('success fitting')

        user_data['chosen_fit_name'] = user_data['chosen_fit_name_1'] + ' ' + user_data['chosen_fit_name_2'] + ' ' + user_data['chosen_fit_name_3'] + ' ' + user_data['chosen_fit_name_4'] 
        conn = psycopg2.connect(dbname="neondb", user="zhanabayevasset", password="txDhFR1yl8Pi", host='ep-cool-poetry-346809.us-east-2.aws.neon.tech')
        cursor = conn.cursor()
        cursor.execute(f"""insert into fitting_canal_params (WORKING,CONTROLLER_NAME,  STANOK,SHIFT, FITTING_NAME, BRAND, NOMINAL_DIAMETER, VIEW, FUNCTIONALITY, MASTER, WEIGHT,DEFECT,DEFECT_DESCR, created_at, updated_at,TYPE_SYR,PRODUCT_TYPE) values (TRUE,'{user_data['chosen_controller_name']}', '{user_data['chosen_stanok']}','{user_data['chosen_smena']}', '{user_data['chosen_fit_name']}',  '{user_data['chosen_tube']}', '{user_data['chosen_nom_diameter']}', '{user_data['chosen_view']}','{user_data['chosen_functionality']}',  '{user_data['chosen_name']}','{user_data['chosen_weight']}', '{user_data['chosen_def']}', '{user_data['chosen_def_descr']}',  current_timestamp + interval'6 hours', current_timestamp + interval'6 hours',  '{user_data['chosen_fit_name_4']}', '{user_data['chosen_fit_name_3']}')""")
        conn.commit()
        cursor.close()
        conn.close()
        await state.set_state(SetParameterFitCanal.send_photo)
