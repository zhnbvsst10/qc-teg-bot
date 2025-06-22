from aiogram import Router, F
from aiogram.filters.text import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards.simple_row import make_row_keyboard
from datetime import datetime, timedelta
import psycopg2
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

router = Router()
available_answers = ['ok', 'not ok','back']
available_shifts = ['A','B','C','back']
available_controllers = ['Daulet', 'Adilet', 'Dinmukhammed']
available_masters_pprc = ['Talgat','Aibar','Omirserik','back']
available_tubes = ['okyanus', 'deniz','pinar','deniz PN','back']
available_diameters = ['20','25','32','40','50','63','back']
available_proceeds = ['yes','back']
available_tube_type = ['композит', 'обычный']
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
    choosing_pprc_tube_type = State()
    choosing_pprc_number_package = State()
    send_photo_num_pack = State()
    send_photo_num_pack_sent = State()
    send_photo = State()
    send_photo_view = State()
    send_photo_view_sent = State()
    send_photo_diameter = State()
    send_photo_diameter_sent = State()
    send_photo_width = State()
    send_photo_width_sent = State()
    send_photo_control_mark = State()
    send_photo_control_mark_sent = State()
    send_photo_weight = State()
    send_photo_weight_sent = State()
    choosing_defects = State()
    continue_load = State()
    defects_descr = State()
    carantine = State()
    def_send = State()

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
        await state.set_state(SetParameterPPRC.choosing_pprc_tube_type)

@router.message(SetParameterPPRC.choosing_pprc_tube_type)
async def pprc_tube(message: Message, state: FSMContext):
    if message.text == 'back':
        await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
        await state.set_state(SetParameterPPRC.choosing_pprc_smena)
    elif message.text == 'go':
        await message.answer(
            text="выберите тип PPR-C трубы:",
            reply_markup=make_row_keyboard(available_tube_type)
        )
        print('choose brand')
        await state.set_state(SetParameterPPRC.choosing_pprc_tube)
    else:
        await state.update_data(chosen_tube=message.text.lower())
        await message.answer(
            text="выберите тип PPR-C трубы:",
            reply_markup=make_row_keyboard(available_tube_type)
        )
        print('choose brand')
        await state.set_state(SetParameterPPRC.choosing_pprc_tube)

@router.message(SetParameterPPRC.choosing_pprc_tube)
async def pprc_number_package(message: Message, state: FSMContext):
    if message.text == 'back':
        await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
        await state.set_state(SetParameterPPRC.choosing_pprc_name)
    elif message.text == 'go':
        await message.answer(
            text="сколько штук в упаковке?",
            reply_markup=ReplyKeyboardRemove()
        )
        print('choose num pack')
        await state.set_state(SetParameterPPRC.choosing_pprc_number_package)
    else:
        await state.update_data(chosen_tube_type=message.text.lower())
        await message.answer(
            text="сколько штук в упаковке?",
            reply_markup=ReplyKeyboardRemove()
        )
        print('choose num pack')
        await state.set_state(SetParameterPPRC.choosing_pprc_number_package)

@router.message(SetParameterPPRC.choosing_pprc_number_package)
async def get_photo_pprc_view(message: Message, state: FSMContext):
        await state.update_data(number_package=message.text.lower())
        await message.answer(
            text="отправьте фото",
            reply_markup=make_row_keyboard(['back'])
        )
        print('choose num_pack_photo')
        await state.set_state(SetParameterPPRC.send_photo_num_pack)

   
@router.message(SetParameterPPRC.send_photo_num_pack)
async def get_photo_pprc_view(message: Message, state: FSMContext, bot):
    if message.text == 'back':
        await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
        await state.set_state(SetParameterPPRC.choosing_pprc_tube)
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
        filename = 'pprc_num_pack_' + (datetime.now() + timedelta(hours=6)).strftime('%Y-%m-%d %H:%M:%S' + '.jpg')
        await bot.download_file(file_path, filename )
        upload_file_list = [filename]
        for upload_file in upload_file_list:
            gfile = drive.CreateFile({'parents': [{'id': '1VnkFYt-wgCIyaEDoYUsOjjkYP0BzXQcE'}]})
            gfile.SetContentFile(upload_file)
            gfile.Upload()

        await message.answer(
                text="продолжить",
                reply_markup=make_row_keyboard(['yes'])
                )
        await state.set_state(SetParameterPPRC.send_photo_num_pack_sent)



@router.message(SetParameterPPRC.send_photo_num_pack_sent)
async def pprc_nom_diameter(message: Message, state: FSMContext):
    if message.text == 'back':
        await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
        await state.set_state(SetParameterPPRC.choosing_pprc_tube_type)
    elif message.text == 'go':
        await message.answer(
            text="выберите номинальный диаметр PPR-C трубы:",
            reply_markup=make_row_keyboard(available_diameters)
        )
        print('choose nom diameter')
        await state.set_state(SetParameterPPRC.choosing_pprc_nom_diameter)
    else:
        
        await message.answer(
            text="выберите номинальный диаметр PPR-C трубы:",
            reply_markup=make_row_keyboard(available_diameters)
        )
        print('choose nom diameter')
        await state.set_state(SetParameterPPRC.choosing_pprc_nom_diameter)

@router.message(SetParameterPPRC.choosing_pprc_nom_diameter)
async def pprc_view(message: Message, state: FSMContext):

    if message.text == 'go':
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

@router.message(SetParameterPPRC.choosing_pprc_view)
async def get_photo_pprc_view(message: Message, state: FSMContext):
        await state.update_data(chosen_view=message.text.lower())
        await message.answer(
            text="отправьте фото",
            reply_markup=make_row_keyboard(['back'])
        )
        print('choose diameter')
        await state.set_state(SetParameterPPRC.send_photo_view)

    
@router.message(SetParameterPPRC.send_photo_view)
async def get_photo_pprc_view(message: Message, state: FSMContext, bot):
    if message.text == 'back':
        await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
        await state.set_state(SetParameterPPRC.choosing_pprc_nom_diameter)
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
        filename = 'pprc_view_' + (datetime.now() + timedelta(hours=6)).strftime('%Y-%m-%d %H:%M:%S' + '.jpg')
        await bot.download_file(file_path, filename )
        upload_file_list = [filename]
        for upload_file in upload_file_list:
            gfile = drive.CreateFile({'parents': [{'id': '1VnkFYt-wgCIyaEDoYUsOjjkYP0BzXQcE'}]})
            gfile.SetContentFile(upload_file)
            gfile.Upload()

        await message.answer(
                text="продолжить",
                reply_markup=make_row_keyboard(['yes'])
                )
        await state.set_state(SetParameterPPRC.send_photo_view_sent)

@router.message(SetParameterPPRC.send_photo_view_sent)
async def pprc_diameter(message: Message, state: FSMContext):
    if message.text == 'go':
        await message.answer(
            text="Теперь укажите диаметр PPR-C трубы:",
            reply_markup=ReplyKeyboardRemove()
        )
        print('choose diameter')
        await state.set_state(SetParameterPPRC.choosing_pprc_diameter)
    else:
        await message.answer(
            text="Теперь укажите диаметр PPR-C трубы:",
            reply_markup=ReplyKeyboardRemove()
        )
        print('choose diameter')
        await state.set_state(SetParameterPPRC.choosing_pprc_diameter)

@router.message(SetParameterPPRC.choosing_pprc_diameter)
async def get_photo_pprc_view(message: Message, state: FSMContext):
        await state.update_data(chosen_diameter=message.text.lower())
        await message.answer(
            text="отправьте фото",
            reply_markup=make_row_keyboard(['back'])
        )
        print('choose diameter')
        await state.set_state(SetParameterPPRC.send_photo_diameter)

@router.message(SetParameterPPRC.send_photo_diameter)
async def get_photo_pprc_view(message: Message, state: FSMContext, bot):
    if message.text == 'back':
        await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
        await state.set_state(SetParameterPPRC.send_photo_view_sent)
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
        filename = 'pprc_diameter_' + (datetime.now() + timedelta(hours=6)).strftime('%Y-%m-%d %H:%M:%S' + '.jpg')
        await bot.download_file(file_path, filename )
        upload_file_list = [filename]
        for upload_file in upload_file_list:
            gfile = drive.CreateFile({'parents': [{'id': '1VnkFYt-wgCIyaEDoYUsOjjkYP0BzXQcE'}]})
            gfile.SetContentFile(upload_file)
            gfile.Upload()

        await message.answer(
                text="продолжить",
                reply_markup=make_row_keyboard(['yes'])
                )
        await state.set_state(SetParameterPPRC.send_photo_diameter_sent)



@router.message(SetParameterPPRC.send_photo_diameter_sent) 
async def pprc_width(message: Message, state: FSMContext):
    if message.text == 'go':
        await message.answer(
            text="Теперь укажите толщину PPR-C трубы:",
            reply_markup=ReplyKeyboardRemove()
        )
        print('choose diameter')
        await state.set_state(SetParameterPPRC.choosing_pprc_width)
    else:
        await message.answer(
            text="Теперь укажите толщину PPR-C трубы:",
            reply_markup=ReplyKeyboardRemove()
        )
        print('choose width')
        await state.set_state(SetParameterPPRC.choosing_pprc_width)

@router.message(SetParameterPPRC.choosing_pprc_width)
async def get_photo_pprc_view(message: Message, state: FSMContext):
        await state.update_data(chosen_width=message.text.lower())
        await message.answer(
            text="отправьте фото",
            reply_markup=make_row_keyboard(['back'])
        )
        print('choose diameter')
        await state.set_state(SetParameterPPRC.send_photo_width)

@router.message(SetParameterPPRC.send_photo_width)
async def get_photo_pprc_view(message: Message, state: FSMContext, bot):
    if message.text == 'back':
        await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
        await state.set_state(SetParameterPPRC.send_photo_diameter_sent)
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
        filename = 'pprc_width_' + (datetime.now() + timedelta(hours=6)).strftime('%Y-%m-%d %H:%M:%S' + '.jpg')
        await bot.download_file(file_path, filename )
        upload_file_list = [filename]
        for upload_file in upload_file_list:
            gfile = drive.CreateFile({'parents': [{'id': '1VnkFYt-wgCIyaEDoYUsOjjkYP0BzXQcE'}]})
            gfile.SetContentFile(upload_file)
            gfile.Upload()

        await message.answer(
                text="продолжить",
                reply_markup=make_row_keyboard(['yes'])
                )
        await state.set_state(SetParameterPPRC.send_photo_width_sent)


@router.message(SetParameterPPRC.send_photo_width_sent) 
async def pprc_weight(message: Message, state: FSMContext):
        await message.answer(
            text="Теперь укажите вес PPR-C трубы:",
            reply_markup=ReplyKeyboardRemove()
        )
        print('choose weight')
        await state.set_state(SetParameterPPRC.choosing_pprc_weight)

@router.message(SetParameterPPRC.choosing_pprc_weight)
async def get_photo_pprc_view(message: Message, state: FSMContext):
        await state.update_data(chosen_weight=message.text.lower())
        await message.answer(
            text="отправьте фото",
            reply_markup=make_row_keyboard(['back'])
        )
        print('choose diameter')
        await state.set_state(SetParameterPPRC.send_photo_weight)

@router.message(SetParameterPPRC.send_photo_weight)
async def get_photo_pprc_view(message: Message, state: FSMContext, bot):
    if message.text == 'back':
        await message.answer(
        text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
        await state.set_state(SetParameterPPRC.send_photo_width_sent)
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
        filename = 'pprc_weight_' + (datetime.now() + timedelta(hours=6)).strftime('%Y-%m-%d %H:%M:%S' + '.jpg')
        await bot.download_file(file_path, filename )
        upload_file_list = [filename]
        for upload_file in upload_file_list:
            gfile = drive.CreateFile({'parents': [{'id': '1VnkFYt-wgCIyaEDoYUsOjjkYP0BzXQcE'}]})
            gfile.SetContentFile(upload_file)
            gfile.Upload()

        await message.answer(
                text="продолжить",
                reply_markup=make_row_keyboard(['yes'])
                )
        await state.set_state(SetParameterPPRC.send_photo_weight_sent)




@router.message(SetParameterPPRC.send_photo_weight_sent)
async def get_photo_pprc_view(message: Message, state: FSMContext):
        ##await state.update_data(chosen_weight=message.text.lower())
        await message.answer(
            text="Есть ли дефекты?",
            reply_markup=make_row_keyboard(['yes','no'])
        )
        print('choose defects')
        await state.set_state(SetParameterPPRC.choosing_defects)

@router.message(SetParameterPPRC.choosing_defects)
async def get_photo_pprc_view(message: Message, state: FSMContext):
        await state.update_data(chosen_def=message.text.lower())
        if message.text == 'yes':
            await message.answer(
                text="Введите описание дефекта",
                reply_markup=ReplyKeyboardRemove()
            )
            print('choose defects')
            await state.set_state(SetParameterPPRC.defects_descr)
        else:
            await message.answer(
                text="продолжить",
                reply_markup=make_row_keyboard(['yes'])
            )
            print('choose defects')
            await state.set_state(SetParameterPPRC.def_send)

@router.message(SetParameterPPRC.defects_descr)
async def get_photo_pprc_view(message: Message, state: FSMContext):
        await state.update_data(chosen_def=message.text.lower())
        if message.text != 'yes':
                await state.update_data(chosen_def_descr=message.text.lower().replace(',', '.'))
        else:
                await state.update_data(chosen_def_descr='')
        await message.answer(
                text="сколько штук поставлено в карантин",
                reply_markup=ReplyKeyboardRemove()
            )
        await state.set_state(SetParameterPPRC.carantine)

@router.message(SetParameterPPRC.carantine)
async def get_photo_pprc_view(message: Message, state: FSMContext):
        await state.update_data(carantine=message.text.lower())
        await message.answer(
                text="сколько штук ушло в брак?",
                reply_markup=ReplyKeyboardRemove()
            )
        await state.set_state(SetParameterPPRC.def_send)

@router.message(SetParameterPPRC.def_send)
async def continue_load(message: Message, state: FSMContext):
    if (datetime.now()+ timedelta(hours = 6)).hour in [2,5,8,11,14,15, 17,20,23]:
        await state.update_data(def_send=message.text.lower().replace(',', '.'))
        await message.answer(
                    text='продолжить заполнение данных',
                    reply_markup=make_row_keyboard(['yes'])
                )
        await state.set_state(SetParameterPPRC.continue_load)
                
                
    elif (datetime.now()+ timedelta(hours = 6)).hour in [0,1,3,4,6,7,9,10,12,13,15,16,18,19,21,22]:
        if message.text == 'back':
            await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
            await state.set_state(SetParameterPPRC.send_photo_diameter_sent)
        else:
            await state.update_data(def_send=message.text.lower().replace(',', '.'))
            await message.answer(
                    text="перейти к передаче данных",
                    reply_markup=make_row_keyboard(available_proceeds)
            )
            await state.set_state(SetParameterPPRC.choosing_pprc_finish)



@router.message(SetParameterPPRC.continue_load)
async def pprc_control_mark(message: Message, state: FSMContext):
    if message.text == 'yes':
        await message.answer(
                        text="Оцените контрольную маркировку PPR-C трубы:",
                        reply_markup=make_row_keyboard(available_answers)
                )
        print('choose control mark')
        await state.set_state(SetParameterPPRC.choosing_pprc_control_mark)

   
@router.message(SetParameterPPRC.choosing_pprc_control_mark)
async def get_photo_pprc_view(message: Message, state: FSMContext):
        await state.update_data(chosen_control_mark=message.text.lower().replace(',', '.'))
        await message.answer(
            text="отправьте фото",
            reply_markup=make_row_keyboard(['back'])
        )
        print('choose diameter')
        await state.set_state(SetParameterPPRC.send_photo_control_mark)

@router.message(SetParameterPPRC.send_photo_control_mark)
async def get_photo_pprc_view(message: Message, state: FSMContext, bot):
    if message.text == 'back':
        await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
        await state.set_state(SetParameterPPRC.continue_load)
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
        filename = 'pprc_control_mark_' + (datetime.now() + timedelta(hours=6)).strftime('%Y-%m-%d %H:%M:%S' + '.jpg')
        await bot.download_file(file_path, filename )
        upload_file_list = [filename]
        for upload_file in upload_file_list:
            gfile = drive.CreateFile({'parents': [{'id': '1VnkFYt-wgCIyaEDoYUsOjjkYP0BzXQcE'}]})
            gfile.SetContentFile(upload_file)
            gfile.Upload()

        await message.answer(
                text="продолжить",
                reply_markup=make_row_keyboard(['yes'])
                )
        await state.set_state(SetParameterPPRC.send_photo_control_mark_sent)



@router.message(SetParameterPPRC.send_photo_control_mark_sent)
async def pprc_finish(message: Message, state: FSMContext):
    # if (datetime.now()+ timedelta(hours = 6)).hour in [2,5,8,11,14,15, 17,20,23]:
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
            
            await message.answer(
                text="перейти к передаче данных",
                reply_markup=make_row_keyboard(available_proceeds)
            )
            await state.set_state(SetParameterPPRC.choosing_pprc_finish)

@router.message(SetParameterPPRC.choosing_pprc_finish, F.text.in_(available_proceeds))
async def pprc_chosen(message: Message, state: FSMContext):
    if (datetime.now()+ timedelta(hours = 6)).hour in [2,5,8,11,14,15, 17,20,23]:
        if message.text == 'back':
            await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
            await state.set_state(SetParameterPPRC.choosing_pprc_control_mark)
        else:
            user_data = await state.get_data()
            if ('chosen_def_descr' in user_data.keys()) == False:
                user_data['chosen_def_descr'] = ''
            await state.clear()
            await message.answer(
                text="Благодарю за заполненные данные",
                reply_markup=ReplyKeyboardRemove()
            )
            print('success 5 params')
            if ('carantine' in user_data.keys()) == False:
                user_data['carantine'] = '0'
                user_data['def_send'] = '0'
                user_data['chosen_def_descr'] = ' '
            
            conn = psycopg2.connect('postgresql://neondb_owner:npg_qKfatzsHP75o@ep-blue-lake-a4lt99hy-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require')
            cursor = conn.cursor()
            cursor.execute(f"""insert into pprc_params (WORKING,CONTROLLER_NAME, SHIFT, BRAND, NOMINAL_DIAMETER, VIEW, DIAMETER,WEIGHT, WIDTH,MARK_CONTROL, MASTER, DEFECT,DEFECT_DESCR,  created_at, updated_at, tube_type, number_package, carantine_num, defect_num) values ('работает','{user_data['chosen_controller_name']}','{user_data['chosen_smena']}','{user_data['chosen_tube']}', '{user_data['chosen_nom_diameter']}', '{user_data['chosen_view']}',{user_data['chosen_diameter']}, {user_data['chosen_weight']},{user_data['chosen_width']}, '{user_data['chosen_control_mark']}', '{user_data['chosen_name']}', '{user_data['chosen_def']}', '{user_data['chosen_def_descr']}', current_timestamp + interval'6 hours', current_timestamp + interval'6 hours', '{user_data['chosen_tube_type']}', '{user_data['number_package']}', '{user_data['carantine']}', '{user_data['def_send']}' )""")
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
            if ('chosen_def_descr' in user_data.keys()) == False:
                user_data['chosen_def_descr'] = ''
            await state.clear()
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
            cursor.execute(f"""insert into pprc_params (WORKING,CONTROLLER_NAME, SHIFT, BRAND, NOMINAL_DIAMETER, VIEW, DIAMETER, WEIGHT, WIDTH, MASTER, DEFECT,DEFECT_DESCR, created_at, updated_at, tube_type, number_package, carantine_num, defect_num) values ('работает', '{user_data['chosen_controller_name']}','{user_data['chosen_smena']}', '{user_data['chosen_tube']}', '{user_data['chosen_nom_diameter']}','{user_data['chosen_view']}',  {user_data['chosen_diameter']},  {user_data['chosen_weight']},{user_data['chosen_width']}, '{user_data['chosen_name']}', '{user_data['chosen_def']}', '{user_data['chosen_def_descr']}',current_timestamp + interval'6 hours', current_timestamp + interval'6 hours', '{user_data['chosen_tube_type']}', '{user_data['number_package']}','{user_data['carantine']}', '{user_data['def_send']}')""")
            conn.commit()
            cursor.close()
            conn.close()
            await state.set_state(SetParameterPPRC.send_photo)
    else:
        await message.answer(
            text="В данный момент работы не ведутся",
            reply_markup=ReplyKeyboardRemove()
        )