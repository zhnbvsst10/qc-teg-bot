from aiogram import Router, F
from aiogram.filters.text import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards.simple_row import make_row_keyboard
from datetime import datetime, timedelta
from aiogram.utils.keyboard import KeyboardButton,ReplyKeyboardBuilder
import psycopg2
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

router = Router()
available_answers = ['ok', 'not ok','back']
available_shifts = ['A','B','C','back']
available_controllers = ['Daulet', 'Adilet', 'Dinmukhammed']
available_masters_fitting = ['Timur', 'Abai', 'Dauren','back']
available_tubes = ['okyanus', 'deniz','kavi','back']
available_diameters = ['50','110','back']
available_proceeds = ['yes','back']
available_stanoks = ['1','2','3','4','5','6','back']

name_dict = {
    'БУТЫЛКА': [    
                'БУТЫЛКА КАНАЛИЗ 100*50 REDUK DENIZ',
                'БУТЫЛКА КАНАЛИЗ 110/50 REDUK OKYANUS',
            ],
    'МУФТА' : [
        'МУФТА * КАНАЛИЗ 110 MANSON OKYANUS PP',
        'МУФТА * КАНАЛИЗ 50 MANSON OKYANUS PP',
        'МУФТА КАНАЛИЗ 100 MANSON DENIZ',
        'МУФТА КАНАЛИЗ 50 MANSON DENIZ',
    ],
    'ОТВОД' : [
        'ОТВОД * КАНАЛИЗ 110*45 DIRSEK OKYANUS PP',
        'ОТВОД * КАНАЛИЗ 110*90 DIRSEK OKYANUS PP',
        'ОТВОД * КАНАЛИЗ 50*45 OKYANUS PP',
        'ОТВОД * КАНАЛИЗ 50*90 DIRSEK OKYANUS PP',
        'ОТВОД КАНАЛИЗ 100*45 DIRSEK DENIZ',
        'ОТВОД КАНАЛИЗ 100*45 DIRSEK DENIZ',
        'ОТВОД КАНАЛИЗ 100*90 DIRSEK DENIZ',
        'ОТВОД КАНАЛИЗ 100*90 DIRSEK DENIZ',
        'ОТВОД КАНАЛИЗ 50*45 DIRSEK DENIZ',
        'ОТВОД КАНАЛИЗ 50*45 DIRSEK DENIZ',
        'ОТВОД КАНАЛИЗ 50*90 DIRSEK DENIZ',
        'ОТВОД КАНАЛИЗ 50*90 DIRSEK DENIZ',
    ],
    'ТРОЙНИК' : [
                'ТРОЙНИК * KOCОЙ 100*50 TEK CATAL OKYANUS PP',
                'ТРОЙНИК * KOCОЙ 110*110 TEK CATAL OKYANUS PP',
                'ТРОЙНИК * ПРЯМОЙ 110*110 TE CATAL OKYANUS PP',
                'ТРОЙНИК * ПРЯМОЙ 50*50 TE CATAL OKYANUS PP',
                'ТРОЙНИК KOCОЙ 100*100 TEK CATAL DENIZ',
                'ТРОЙНИК KOCОЙ 100*50 TEK CATAL DENIZ PP',
                'ТРОЙНИК KOCОЙ 50*50 TEK CATAL DENIZ',
                'ТРОЙНИК KOCОЙ 50*50 TEK CATAL OKYANUS PP',
                'ТРОЙНИК ПРЯМОЙ 110*110*87.5 TE CATAL DENIZ',
                'ТРОЙНИК ПРЯМОЙ 100*100 TE CATAL DENIZ',
                'ТРОЙНИК ПРЯМОЙ 100*50 TE CATAL DENIZ',
                'ТРОЙНИК ПРЯМОЙ 50*50 TE CATAL DENIZ',
                'ТРОЙНИК ПРЯМОЙ 110/45 OKYANUS',

            ],
    'ХОМУТ' : [
                'ХОМУТ КАНАЛИЗ 100 KELEPCE DENIZ',
                'ХОМУТ КАНАЛИЗ 50 KELEPCE DENIZ',
            ],
    'РЕВИЗИЯ' : [
        'РЕВИЗИЯ * КАНАЛИЗ 100*100 TEMIZLEME OKYANUS PP',
        'РЕВИЗИЯ 100*100 TEMIZLEME DENIZ PP',
    ],
    'КРЕСТОВИНА' : [
        'КРЕСТОВИНА * КАНАЛИЗ 100*100*90 ISTAVROZ OKYANUS PP',
        'КРЕСТОВИНА 100*100*90 ISTAVROZ DENIZ PP',
        'КРЕСТОВИНА 110/110/45 OKYANUS',
        'КРЕСТОВИНА 110/110/45 DENIZ',

    ],
    'ЗАГЛУШКА' : [
        'ЗАГЛУШКА КАНАЛИЗ 100 KORTAPA DENIZ',
        'ЗАГЛУШКА КАНАЛИЗ 50 KORTAPA DENIZ',
    ],
    'КРЫШКА' : [
        'КРЫШКА РЕВИЗИЙ'
    ]
}
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
    continue_load = State()
    carantine = State()
    def_send = State()

@router.message(Text(text='работает фиттинг канализ'))
async def fitting_controller(message: Message, state: FSMContext):
    
    await message.answer(
        text="Выберите контроллера",
        reply_markup=make_row_keyboard(available_controllers)
    )
    print('choose controller canal')
    await state.set_state(SetParameterFitCanal.choosing_fitting_controller)


# @router.message(SetParameterFitCanal.choosing_fitting_controller)
# async def pprc_name(message: Message, state: FSMContext):
#     await state.update_data(chosen_controller_name=message.text.lower())
#     await message.answer(
#             text="Выберите станок?",
#             reply_markup=make_row_keyboard(available_stanoks)
#         )
#     print('choose stanok')
#     await state.set_state(SetParameterFitCanal.choosing_fitting_line)

@router.message(SetParameterFitCanal.choosing_fitting_controller)
async def pprc_name(message: Message, state: FSMContext):
    if message.text == 'go':
        await message.answer(
            text="Кто является мастером на линии на текущий час ?",
            reply_markup=make_row_keyboard(available_masters_fitting)
        )
        print('choose master canal')
        await state.set_state(SetParameterFitCanal.choosing_fitting_name)
    else:
        # await state.update_data(chosen_stanok=message.text.lower())
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
        button9 = KeyboardButton(text='КРЫШКА')
        button10 = KeyboardButton(text='back')
            
        markup1 = ReplyKeyboardBuilder([[button1]]).row(button2).row(button3).row(button4).row(button5).row(button6).row(button7).row(button8).row(button9).row(button10).as_markup()
        
        await message.answer(
            text='Выберите наименование продукции',
            reply_markup=markup1
        )
        print('choose fit name 1 canal ')
        await state.set_state(SetParameterFitCanal.choosing_fitting_tube_2)
    else:
            button1 = KeyboardButton(text='КРЕСТОВИНА')
            button2 = KeyboardButton(text='МУФТА')
            button3 = KeyboardButton(text='ОТВОД')
            button4 = KeyboardButton(text='ТРОЙНИК')
            button5 = KeyboardButton(text='РЕВИЗИЯ')
            button6 = KeyboardButton(text='ЗАГЛУШКА')
            button7 = KeyboardButton(text='ХОМУТ')
            button8 = KeyboardButton(text='БУТЫЛКА')
            button9 = KeyboardButton(text='КРЫШКА')
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
    else:
        builder = ReplyKeyboardBuilder()
        for index in range(len(name_dict[message.text])):
            builder.button(text=f"{name_dict[message.text][index]}", callback_data = f"{name_dict[message.text][index]}")
        builder.button(text=f"back", callback_data = f"back")
        builder.adjust(1,1)
        await state.update_data(chosen_fit_name_1=message.text.lower())
        await message.answer(
            text='Выбрите',
            reply_markup=builder.as_markup()
        )
        print('choose fit name 3')
        await state.set_state(SetParameterFitCanal.choosing_fitting_tube_3)

@router.message(SetParameterFitCanal.choosing_fitting_tube_3)
async def pprc_nom_diameter(message: Message, state: FSMContext):
    if message.text == 'back':
        await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
        await state.set_state(SetParameterFitCanal.choosing_fitting_tube_1)
    elif message.text == 'go':
        await message.answer(
            text="выберите номинальный диаметр фиттинга:",
            reply_markup=make_row_keyboard(available_diameters)
        )
        print('choose nom diameter')
        await state.set_state(SetParameterFitCanal.choosing_fitting_nom_diameter)
    else:
        await state.update_data(chosen_fit_name=message.text.lower())
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
        await state.set_state(SetParameterFitCanal.choosing_fitting_tube_2)
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
        #PhotoSize(file_id=file_id, file_unique_id=file_unique_id)
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
        await state.set_state(SetParameterFitCanal.send_photo_view_sent)
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
            await state.set_state(SetParameterFitCanal.def_send)

@router.message(SetParameterFitCanal.defects_descr)
async def get_photo_pprc_view(message: Message, state: FSMContext):
        await state.update_data(chosen_def_descr=message.text.lower())
        await message.answer(
                text="сколько штук поставлено в карантин",
                reply_markup=ReplyKeyboardRemove()
            )
        await state.set_state(SetParameterFitCanal.carantine)

@router.message(SetParameterFitCanal.carantine)
async def get_photo_pprc_view(message: Message, state: FSMContext):
        await state.update_data(carantine=message.text.lower())
        await message.answer(
                text="сколько штук ушло в брак?",
                reply_markup=ReplyKeyboardRemove()
            )
        await state.set_state(SetParameterFitCanal.def_send)

@router.message(SetParameterFitCanal.def_send)
async def pprc_finish(message: Message, state: FSMContext):
    if ((datetime.now() + timedelta(hours=6)).hour) in [0,2,4,6,8,10,12,14,16,18,20,22,24]:
        if message.text == 'go':
            await message.answer(
                    text="перейти к передаче данных",
                    reply_markup=make_row_keyboard(available_proceeds)
            )
            await state.set_state(SetParameterFitCanal.choosing_fitting_finish)
        else:
            if message.text != 'yes':
                await state.update_data(def_send=message.text.lower().replace(',', '.'))
            else:
                await state.update_data(def_send = '')
            await message.answer(
                    text="перейти к передаче данных",
                    reply_markup=make_row_keyboard(available_proceeds)
            )
            await state.set_state(SetParameterFitCanal.choosing_fitting_finish)
    else:
        if message.text != 'yes':
                await state.update_data(def_send=message.text.lower().replace(',', '.'))
        else:
                await state.update_data(def_send = '')
            
        await message.answer(
            text="продолжить заполнение данных",
            reply_markup=make_row_keyboard(['yes'])
        )
        await  state.set_state(SetParameterFitCanal.continue_load)


@router.message(SetParameterFitCanal.continue_load)
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
        await state.set_state(SetParameterFitCanal.continue_load)
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
        await state.set_state(SetParameterFitCanal.choosing_fitting_finish)



@router.message(SetParameterFitCanal.choosing_fitting_finish, F.text.in_(available_proceeds))
async def fitting_chosen(message: Message, state: FSMContext):
    if (datetime.now() + timedelta(hours=6)).hour in [0,2,4,6,8,10,12,14,16,18,20,22,24]:
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
            
            if ('carantine' in user_data.keys()) == False:
                user_data['carantine'] = '0'
                user_data['def_send'] = '0'
                user_data['chosen_def_descr'] = ' '
            #user_data['chosen_fit_name'] = user_data['chosen_fit_name_1'] + ' ' + user_data['chosen_fit_name_2'] + ' ' + user_data['chosen_fit_name_3'] + ' ' + user_data['chosen_fit_name_4'] 
            conn = psycopg2.connect(dbname="neondb", user="zhanabayevasset", password="txDhFR1yl8Pi", host='ep-cool-poetry-346809.us-east-2.aws.neon.tech')
            cursor = conn.cursor()
            cursor.execute(f"""insert into fitting_canal_params (WORKING,CONTROLLER_NAME,  STANOK,SHIFT, FITTING_NAME, BRAND, NOMINAL_DIAMETER, VIEW, MASTER, WEIGHT,DEFECT,DEFECT_DESCR, created_at, updated_at, carantine_num, defect_num) values (TRUE,'{user_data['chosen_controller_name']}', '{user_data['chosen_stanok']}','{user_data['chosen_smena']}', '{user_data['chosen_fit_name']}',  '{user_data['chosen_tube']}', '{user_data['chosen_nom_diameter']}', '{user_data['chosen_view']}', '{user_data['chosen_name']}','{user_data['chosen_weight']}', '{user_data['chosen_def']}', '{user_data['chosen_def_descr']}',  current_timestamp + interval'6 hours', current_timestamp + interval'6 hours','{user_data['carantine']}', '{user_data['def_send']}')""")
            conn.commit()
            cursor.close()
            conn.close()
            print('success fitting')
            await state.set_state(SetParameterFitCanal.send_photo)
    else:
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
            
            if ('carantine' in user_data.keys()) == False:
                user_data['carantine'] = '0'
                user_data['def_send'] = '0'
                user_data['chosen_def_descr'] = ' '
            #user_data['chosen_fit_name'] = user_data['chosen_fit_name_1'] + ' ' + user_data['chosen_fit_name_2'] + ' ' + user_data['chosen_fit_name_3'] + ' ' + user_data['chosen_fit_name_4'] 
            conn = psycopg2.connect(dbname="neondb", user="zhanabayevasset", password="txDhFR1yl8Pi", host='ep-cool-poetry-346809.us-east-2.aws.neon.tech')
            cursor = conn.cursor()
            cursor.execute(f"""insert into fitting_canal_params (WORKING,CONTROLLER_NAME,  STANOK,SHIFT, FITTING_NAME, BRAND, NOMINAL_DIAMETER, VIEW, FUNCTIONALITY, MASTER, WEIGHT,DEFECT,DEFECT_DESCR, created_at, updated_at, carantine_num, defect_num) values (TRUE,'{user_data['chosen_controller_name']}', '{user_data['chosen_stanok']}','{user_data['chosen_smena']}', '{user_data['chosen_fit_name']}',  '{user_data['chosen_tube']}', '{user_data['chosen_nom_diameter']}', '{user_data['chosen_view']}','{user_data['chosen_functionality']}',  '{user_data['chosen_name']}','{user_data['chosen_weight']}', '{user_data['chosen_def']}', '{user_data['chosen_def_descr']}',  current_timestamp + interval'6 hours', current_timestamp + interval'6 hours', '{user_data['carantine']}', '{user_data['def_send']}')""")
            conn.commit()
            cursor.close()
            conn.close()
            print('success fitting')
            await state.set_state(SetParameterFitCanal.send_photo)
