from aiogram import Router
from aiogram.filters.text import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards.simple_row import make_row_keyboard
from datetime import datetime, timedelta
import psycopg2
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from aiogram import Bot
import os
from dotenv import load_dotenv

load_dotenv()
#token = os.getenv('TOKEN')
token = os.getenv('TOKEN')
bot = Bot(token=token)

router2 = Router()
available_answers = ['ok', 'not ok','back']
available_shifts = ['A','B','C','back']
available_controllers = ['Daulet', 'Adilet', 'Dinmukhammed']
available_names = ['Talgat','Aibar','Omirserik','back']
available_tubes = ['PE-RT','OxyPE-RT', 'Pert-Al- Pert', 'back']
available_proceeds = ['yes']

db_url = os.getenv('DATABASE_URL') or os.getenv('CONN_STR')

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
    send_photo_view = State()
    send_photo_view_sent = State()
    send_photo_diameter = State()
    send_photo_diameter_sent = State()
    send_photo_outer_diam = State()
    send_photo_outer_diam_sent = State()
    send_photo_width = State()
    send_photo_width_sent = State()
    send_photo_width_s = State()
    send_photo_width_s_sent = State()
    send_photo_control_mark = State()
    send_photo_control_mark_sent = State()
    send_photo_weight = State()
    send_photo_weight_sent = State()
    send_photo_weight_b = State()
    send_photo_weight_b_sent = State()
    choosing_defects = State()
    defects_descr = State()
    continue_load = State()
    carantine = State()
    def_send = State()

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
    if message.text != 'go':
        await state.update_data(chosen_controller_name=message.text.lower())
        await message.answer(
                    text="Выберите смену ",
                    reply_markup=make_row_keyboard(available_shifts)
            )
        print('choose smena')
        await state.set_state(SetParameterPERT.choosing_pvc_smena)
    else:
        await message.answer(
                    text="Выберите смену ",
                    reply_markup=make_row_keyboard(available_shifts)
            )
        print('choose smena')
        await state.set_state(SetParameterPERT.choosing_pvc_smena)
    

@router2.message(SetParameterPERT.choosing_pvc_smena)
async def pvc_name(message: Message, state: FSMContext):
    if message.text == 'back':
        await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
        await state.set_state(SetParameterPERT.choosing_pvc_controller)
    elif message.text == 'go':
        await message.answer(
        text="Кто является мастером на линии на текущий час ?",
                reply_markup=make_row_keyboard(available_names)
                )
        print('choose master')
        await state.set_state(SetParameterPERT.choosing_pvc_name)
    else: 
        await state.update_data(chosen_smena=message.text.lower())
        await message.answer(
        text="Кто является мастером на линии на текущий час ?",
                reply_markup=make_row_keyboard(available_names)
                )
        print('choose master')
        await state.set_state(SetParameterPERT.choosing_pvc_name)



@router2.message(SetParameterPERT.choosing_pvc_name)
async def pvc_tube(message: Message, state: FSMContext):
    if message.text == 'back':
        await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
        await state.set_state(SetParameterPERT.choosing_pvc_controller)
    elif message.text == 'go':
        await message.answer(
            text="выберите бренд:",
            reply_markup=make_row_keyboard(available_tubes)
        )
        print('choose brand')
        await state.set_state(SetParameterPERT.choosing_pvc_tube)
    else:
        await state.update_data(chosen_name=message.text.lower())
        await message.answer(
            text="выберите бренд:",
            reply_markup=make_row_keyboard(available_tubes)
        )
        print('choose brand')
        await state.set_state(SetParameterPERT.choosing_pvc_tube)

@router2.message(SetParameterPERT.choosing_pvc_tube)
async def pvc_tube(message: Message, state: FSMContext):
    if message.text == 'go':
        await message.answer(
        text="оцените внешний вид:",
        reply_markup=make_row_keyboard(available_answers)
        )
        print('choose view')
        await state.set_state(SetParameterPERT.choosing_pvc_view)
    else:
        await state.update_data(chosen_tube=message.text.lower())
        await message.answer(
            text="оцените внешний вид:",
            reply_markup=make_row_keyboard(available_answers)
        )
        print('choose view')
        await state.set_state(SetParameterPERT.choosing_pvc_view)

@router2.message(SetParameterPERT.choosing_pvc_view)
async def get_photo_pprc_view(message: Message, state: FSMContext):
        await state.update_data(chosen_view=message.text.lower())
        await message.answer(
            text="отправьте фото",
            reply_markup=make_row_keyboard(['back'])
        )
        print('choose diameter')
        await state.set_state(SetParameterPERT.send_photo_view)

@router2.message(SetParameterPERT.send_photo_view)
async def get_photo_pprc_view(message: Message, state: FSMContext):
    if message.text == 'back':
        await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
        await state.set_state(SetParameterPERT.choosing_pvc_tube)
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
        filename = 'pert_view_' + (datetime.now() + timedelta(hours=6)).strftime('%Y-%m-%d %H:%M:%S' + '.jpg')
        await bot.download_file(file_path, filename )
        upload_file_list = [filename]
        for upload_file in upload_file_list:
            gfile = drive.CreateFile({'parents': [{'id': '1NwwKZX-0JbjnoagbHu5c5LpGCPia_rz3'}]})
            gfile.SetContentFile(upload_file)
            gfile.Upload()

        await message.answer(
                text="продолжить",
                reply_markup=make_row_keyboard(['yes'])
                )
        await state.set_state(SetParameterPERT.send_photo_view_sent)

@router2.message(SetParameterPERT.send_photo_view_sent)
async def pvc_functionality(message: Message, state: FSMContext):

    if message.text == 'go':
        await message.answer(
        text="введите наружний диаметр:",
        reply_markup=ReplyKeyboardRemove()
        )
        print('choose outer_diam')
        await state.set_state(SetParameterPERT.choosing_pvc_outer_diam)
    else:
        await message.answer(
            text="введите наружний диаметр:",
            reply_markup=ReplyKeyboardRemove()
        )
        print('choose outer_diam')
        await state.set_state(SetParameterPERT.choosing_pvc_outer_diam)

@router2.message(SetParameterPERT.choosing_pvc_outer_diam)
async def get_photo_pprc_view(message: Message, state: FSMContext):
        await state.update_data(chosen_outer_diam=message.text.lower())
        await message.answer(
            text="отправьте фото",
            reply_markup=make_row_keyboard(['back'])
        )
        print('choose diameter')
        await state.set_state(SetParameterPERT.send_photo_outer_diam)

@router2.message(SetParameterPERT.send_photo_outer_diam)
async def get_photo_pprc_view(message: Message, state: FSMContext, bot):
    if message.text == 'back':
        await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
        await state.set_state(SetParameterPERT.send_photo_view_sent)
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
        filename = 'pert_outer_diameter_' + (datetime.now() + timedelta(hours=6)).strftime('%Y-%m-%d %H:%M:%S' + '.jpg')
        await bot.download_file(file_path, filename )
        upload_file_list = [filename]
        for upload_file in upload_file_list:
            gfile = drive.CreateFile({'parents': [{'id': '1NwwKZX-0JbjnoagbHu5c5LpGCPia_rz3'}]})
            gfile.SetContentFile(upload_file)
            gfile.Upload()

        await message.answer(
                text="продолжить",
                reply_markup=make_row_keyboard(['yes'])
                )
        await state.set_state(SetParameterPERT.send_photo_outer_diam_sent)


@router2.message(SetParameterPERT.send_photo_outer_diam_sent) #F.text.in_(available_food_names))
async def pvc_diameter(message: Message, state: FSMContext):
    if message.text == 'go':
        await message.answer(
        text="введите толщину стенок:",
        reply_markup=ReplyKeyboardRemove()
        )
        print('choose width stenok')
        await state.set_state(SetParameterPERT.choosing_pvc_width_s)
    else:
        await message.answer(
            text="введите толщину стенок:",
            reply_markup=ReplyKeyboardRemove()
        )
        print('choose width stenok')
        await state.set_state(SetParameterPERT.choosing_pvc_width_s)

@router2.message(SetParameterPERT.choosing_pvc_width_s)
async def get_photo_pprc_view(message: Message, state: FSMContext):
        await state.update_data(chosen_width_s=message.text.lower())
        await message.answer(
            text="отправьте фото",
            reply_markup=make_row_keyboard(['back'])
        )
        print('choose diameter')
        await state.set_state(SetParameterPERT.send_photo_width_s)

@router2.message(SetParameterPERT.send_photo_width_s)
async def get_photo_pprc_view(message: Message, state: FSMContext, bot):
    if message.text == 'back':
        await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
        await state.set_state(SetParameterPERT.send_photo_outer_diam_sent)
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
        filename = 'pert_width_s_' + (datetime.now() + timedelta(hours=6)).strftime('%Y-%m-%d %H:%M:%S' + '.jpg')
        await bot.download_file(file_path, filename )
        upload_file_list = [filename]
        for upload_file in upload_file_list:
            gfile = drive.CreateFile({'parents': [{'id': '1NwwKZX-0JbjnoagbHu5c5LpGCPia_rz3'}]})
            gfile.SetContentFile(upload_file)
            gfile.Upload()

        await message.answer(
                text="продолжить",
                reply_markup=make_row_keyboard(['yes'])
                )
        await state.set_state(SetParameterPERT.send_photo_width_s_sent)
        

@router2.message(SetParameterPERT.send_photo_width_s_sent)
async def pvc_diameter(message: Message, state: FSMContext):
    if message.text == 'go':
        await message.answer(
        text="введите вес бухты:",
        reply_markup=ReplyKeyboardRemove()
        )
        print('choose weight b')
        await state.set_state(SetParameterPERT.choosing_pvc_weight_b)
    else:
        await message.answer(
            text="введите вес бухты:",
            reply_markup=ReplyKeyboardRemove()
        )
        print('choose weight b')
        await state.set_state(SetParameterPERT.choosing_pvc_weight_b)



@router2.message(SetParameterPERT.choosing_pvc_weight_b)
async def get_photo_pprc_view(message: Message, state: FSMContext):
        await state.update_data(chosen_weight_b=message.text.lower())
        await message.answer(
            text="отправьте фото",
            reply_markup=make_row_keyboard(['back'])
        )
        print('choose diameter')
        await state.set_state(SetParameterPERT.send_photo_weight_b)

@router2.message(SetParameterPERT.send_photo_weight_b)
async def get_photo_pprc_view(message: Message, state: FSMContext, bot):
    if message.text == 'back':
        await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
        await state.set_state(SetParameterPERT.send_photo_width_s_sent)
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
        filename = 'pert_weight_b_' + (datetime.now() + timedelta(hours=6)).strftime('%Y-%m-%d %H:%M:%S' + '.jpg')
        await bot.download_file(file_path, filename )
        upload_file_list = [filename]
        for upload_file in upload_file_list:
            gfile = drive.CreateFile({'parents': [{'id': '1NwwKZX-0JbjnoagbHu5c5LpGCPia_rz3'}]})
            gfile.SetContentFile(upload_file)
            gfile.Upload()

        await message.answer(
                text="продолжить",
                reply_markup=make_row_keyboard(['yes'])
                )
        await state.set_state(SetParameterPERT.send_photo_weight_b_sent)


@router2.message(SetParameterPERT.send_photo_weight_b_sent)
async def pvc_diameter(message: Message, state: FSMContext):
        await message.answer(
            text="Введите вес:",
            reply_markup=ReplyKeyboardRemove()
        )
        print('choose weight ')
        await state.set_state(SetParameterPERT.choosing_pvc_weight)

@router2.message(SetParameterPERT.choosing_pvc_weight)
async def get_photo_pprc_view(message: Message, state: FSMContext):
        await state.update_data(chosen_weight=message.text.lower())
        await message.answer(
            text="отправьте фото",
            reply_markup=make_row_keyboard(['back'])
        )
        await state.set_state(SetParameterPERT.send_photo_weight)

@router2.message(SetParameterPERT.send_photo_weight)
async def get_photo_pprc_view(message: Message, state: FSMContext, bot):
    if message.text == 'back':
        await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
        await state.set_state(SetParameterPERT.send_photo_weight_b_sent)
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
        filename = 'pert_weight_' + (datetime.now() + timedelta(hours=6)).strftime('%Y-%m-%d %H:%M:%S' + '.jpg')
        await bot.download_file(file_path, filename )
        upload_file_list = [filename]
        for upload_file in upload_file_list:
            gfile = drive.CreateFile({'parents': [{'id': '1NwwKZX-0JbjnoagbHu5c5LpGCPia_rz3'}]})
            gfile.SetContentFile(upload_file)
            gfile.Upload()

        await message.answer(
                text="продолжить",
                reply_markup=make_row_keyboard(['yes'])
                )
        await state.set_state(SetParameterPERT.send_photo_weight_sent)


@router2.message(SetParameterPERT.send_photo_weight_sent)
async def get_photo_pprc_view(message: Message, state: FSMContext):
        await message.answer(
            text="Есть ли дефекты?",
            reply_markup=make_row_keyboard(['yes','no'])
        )
        print('choose defects')
        await state.set_state(SetParameterPERT.choosing_defects)


@router2.message(SetParameterPERT.choosing_defects)
async def get_photo_pprc_view(message: Message, state: FSMContext):
        await state.update_data(chosen_def=message.text.lower())
        if message.text == 'yes':
            await message.answer(
                text="Введите описание дефекта",
                reply_markup=ReplyKeyboardRemove()
            )
            print('choose defects')
            await state.set_state(SetParameterPERT.defects_descr)
        else:
            await message.answer(
                text="продолжить",
                reply_markup=make_row_keyboard(['yes'])
            )
            print('choose defects')
            await state.set_state(SetParameterPERT.def_send)

@router2.message(SetParameterPERT.defects_descr)
async def get_photo_pprc_view(message: Message, state: FSMContext):
        await state.update_data(chosen_def_descr=message.text.lower())
        
        await message.answer(
                text="сколько штук поставлено в карантин",
                reply_markup=ReplyKeyboardRemove()
            )
        await state.set_state(SetParameterPERT.carantine)

@router2.message(SetParameterPERT.carantine)
async def get_photo_pprc_view(message: Message, state: FSMContext):
        await state.update_data(carantine=message.text.lower())
        await message.answer(
                text="сколько штук ушло в брак?",
                reply_markup=ReplyKeyboardRemove()
            )
        await state.set_state(SetParameterPERT.def_send)

@router2.message(SetParameterPERT.def_send) #F.text.in_(available_food_names))
async def pvc_width(message: Message, state: FSMContext):
    if (datetime.now()+ timedelta(hours = 6)).hour in [2,5,8,11,14,17,20,23]:
            if message.text != 'yes':
                await state.update_data(def_send=message.text.lower().replace(',', '.'))
            else:
                await state.update_data(def_send = '')
            await message.answer(
                    text='продолжить заполнение данных',
                    reply_markup=make_row_keyboard(['yes'])
                )
            await state.set_state(SetParameterPERT.continue_load)

    elif (datetime.now()+ timedelta(hours = 6)).hour in [0,1,3,4,6,7,9,10,12,13,15,16,18,19,21,22]:
        if message.text == 'back':
            await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
            await state.set_state(SetParameterPERT.choosing_pvc_outer_diam)
        else:
            if message.text != 'yes':
                await state.update_data(def_send=message.text.lower().replace(',', '.'))
            else:
                await state.update_data(def_send = '')
            await message.answer(
                    text="перейти к передаче данных",
                    reply_markup=make_row_keyboard(available_proceeds)
            )
            await state.set_state(SetParameterPERT.choosing_pvc_finish)

        



@router2.message(SetParameterPERT.continue_load) #F.text.in_(available_food_names))
async def pvc_control_mark(message: Message, state: FSMContext):
    if message.text == 'go':
        await message.answer(
            text="оцените контрольную маркировку:",
            reply_markup=make_row_keyboard(available_answers)
        )
        print('choose control mark')
        await state.set_state(SetParameterPERT.choosing_pvc_control_mark)
    else:
        await message.answer(
                text="оцените контрольную маркировку:",
                reply_markup=make_row_keyboard(available_answers)
        )
        print('choose control mark')
        await state.set_state(SetParameterPERT.choosing_pvc_control_mark)

@router2.message(SetParameterPERT.choosing_pvc_control_mark)
async def get_photo_pprc_view(message: Message, state: FSMContext):
        await state.update_data(chosen_control_mark=message.text.lower())
        await message.answer(
            text="отправьте фото",
            reply_markup=make_row_keyboard(['back'])
        )
        print('choose diameter')
        await state.set_state(SetParameterPERT.send_photo_control_mark)

@router2.message(SetParameterPERT.send_photo_control_mark)
async def get_photo_pprc_view(message: Message, state: FSMContext, bot):
    if message.text == 'back':
        await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
        await state.set_state(SetParameterPERT.continue_load)
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
        filename = 'pert_control_mark_' + (datetime.now() + timedelta(hours=6)).strftime('%Y-%m-%d %H:%M:%S' + '.jpg')
        await bot.download_file(file_path, filename )
        upload_file_list = [filename]
        for upload_file in upload_file_list:
            gfile = drive.CreateFile({'parents': [{'id': '1NwwKZX-0JbjnoagbHu5c5LpGCPia_rz3'}]})
            gfile.SetContentFile(upload_file)
            gfile.Upload()

        await message.answer(
                text="продолжить",
                reply_markup=make_row_keyboard(['yes'])
                )
        await state.set_state(SetParameterPERT.send_photo_control_mark_sent)



    
@router2.message(SetParameterPERT.send_photo_control_mark_sent)
async def pvc_length(message: Message, state: FSMContext):
    if message.text == 'back':
        await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
        await state.set_state(SetParameterPERT.choosing_pvc_weight_b)
    else:
        await message.answer(
                text="перейти к передаче данных",
                reply_markup=make_row_keyboard(available_proceeds)
            )
        await state.set_state(SetParameterPERT.choosing_pvc_finish)






@router2.message(SetParameterPERT.choosing_pvc_finish)
async def pvc_chosen(message: Message, state: FSMContext):
    if (datetime.now()+ timedelta(hours = 6)).hour in [2,5,8,11,14,17,20,23]:
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
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor()
        cursor.execute(f"""insert into pert_params (WORKING,CONTROLLER_NAME, SHIFT, BRAND, VIEW, 
                                                    OUTER_DIAMETER, WIDTH_ST, WEIGHT_B, WEIGHT, MARK_CONTROL,
                                                     MASTER,DEFECT,DEFECT_DESCR,  created_at, updated_at, carantine_num, defect_num) values 
                                                (TRUE,'{user_data['chosen_controller_name']}','{user_data['chosen_smena']}','{user_data['chosen_tube']}',  
                                                            '{user_data['chosen_view']}','{user_data['chosen_outer_diam']}',{user_data['chosen_width_s']}, 
                                                            {user_data['chosen_weight_b']}, {user_data['chosen_weight']}, '{user_data['chosen_control_mark']}', '{user_data['chosen_name']}',
                                                            '{user_data['chosen_def']}', '{user_data['chosen_def_descr']}',
                                                              current_timestamp + interval'6 hours', current_timestamp + interval'6 hours', '{user_data['carantine']}', '{user_data['def_send']}')""")
        conn.commit()
        cursor.close()
        conn.close()
        await state.set_state(SetParameterPERT.send_photo)
    elif (datetime.now()+ timedelta(hours = 6)).hour in [0,1,3,4,6,7,9,10,12,13,15,16,18,19,21,22]:
        print('sucess 3 params')
        user_data = await state.get_data()
        await message.answer(
            text="Благодарю за заполненные данные",
            reply_markup=ReplyKeyboardRemove()
        )
        if ('carantine' in user_data.keys()) == False:
                user_data['carantine'] = '0'
                user_data['def_send'] = '0'
                user_data['chosen_def_descr'] = ' '
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor()
        cursor.execute(f"""insert into pert_params (WORKING,CONTROLLER_NAME, SHIFT, BRAND, VIEW, 
                                                    OUTER_DIAMETER, WIDTH_ST, WEIGHT_B, WEIGHT,
                                                     MASTER,DEFECT,DEFECT_DESCR,  created_at, updated_at, carantine_num, defect_num) values 
                                                (TRUE,'{user_data['chosen_controller_name']}','{user_data['chosen_smena']}','{user_data['chosen_tube']}',  
                                                            '{user_data['chosen_view']}','{user_data['chosen_outer_diam']}',{user_data['chosen_width_s']}, 
                                                            {user_data['chosen_weight_b']}, {user_data['chosen_weight']}, '{user_data['chosen_name']}','{user_data['chosen_def']}', '{user_data['chosen_def_descr']}',
                                                              current_timestamp + interval'6 hours', current_timestamp + interval'6 hours', '{user_data['carantine']}', '{user_data['def_send']}')""")
        conn.commit()
        cursor.close()
        conn.close()
        await state.set_state(SetParameterPERT.send_photo)
    else:
        await message.answer(
            text="В данный момент работы не ведутся",
            reply_markup=ReplyKeyboardRemove()
        )
