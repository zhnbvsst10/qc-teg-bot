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


router = Router()
available_answers = ['ok', 'not ok','back']
available_shifts = ['A','B','C']
available_controllers = ['Madi', 'Zhanibek', 'Magzhan']
available_masters_fitting = ['Salamat', 'Dauren', 'Anton','back']
available_tubes = ['okyanus', 'deniz','kavi','back']
available_diameters = ['20','25','32','40','back']
available_proceeds = ['yes','back']
available_stanoks = ['1','2','3','4','5','6','back']


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
    choosing_fitting_finish = State()
    send_photo = State()

@router.message(Text(text='работает фиттинг водопр'))
async def fitting_controller(message: Message, state: FSMContext):
    
    await message.answer(
        text="Выберите контроллера",
        reply_markup=make_row_keyboard(available_controllers)
    )
    print('choose controller')
    await state.set_state(SetParameterFit.choosing_fitting_controller)

@router.message(SetParameterFit.choosing_fitting_controller)
async def fitting_smena(message: Message, state: FSMContext):
    if message.text == 'go':
        await message.answer(
            text="Выберите смену ",
            reply_markup=make_row_keyboard(available_shifts)
        )
        print('choose smena canal')
        await state.set_state(SetParameterFit.choosing_fitting_smena)
    else:
        await state.update_data(chosen_controller_name=message.text.lower())
        await message.answer(
            text="Выберите смену ",
            reply_markup=make_row_keyboard(available_shifts)
        )
        print('choose smena')
        await state.set_state(SetParameterFit.choosing_fitting_smena)


@router.message(SetParameterFit.choosing_fitting_smena)
async def pprc_name(message: Message, state: FSMContext):
    if message.text == 'back':
        await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
        await state.set_state(SetParameterFit.choosing_fitting_controller)
    elif message.text == 'go':
        await message.answer(
            text="Кто является мастером на линии на текущий час ?",
            reply_markup=make_row_keyboard(available_masters_fitting)
        )
        print('choose master')
        await state.set_state(SetParameterFit.choosing_fitting_name)
    else:
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
        button1 = KeyboardButton(text='КРЕПЛЕНИЕ ')
        button2 = KeyboardButton(text='МУФТА ')
        button3 = KeyboardButton(text='ОТВОД ')
        button4 = KeyboardButton(text='ТРОЙНИК ')
        button5 = KeyboardButton(text='МОСТ ')
        button6 = KeyboardButton(text='АРМАТУРА ')
        button7 = KeyboardButton(text='back')
            
        markup1 = ReplyKeyboardBuilder([[button1]]).row(button2).row(button3).row(button4).row(button5).row(button6).row(button7).as_markup()
        await message.answer(
            text='Выберите наименование продукции',
            reply_markup=markup1
        )
        print('choose fit name 1')
        await state.set_state(SetParameterFit.choosing_fitting_tube_2)
    else:
        button1 = KeyboardButton(text='КРЕПЛЕНИЕ ')
        button2 = KeyboardButton(text='МУФТА ')
        button3 = KeyboardButton(text='ОТВОД ')
        button4 = KeyboardButton(text='ТРОЙНИК ')
        button5 = KeyboardButton(text='МОСТ ')
        button6 = KeyboardButton(text='АРМАТУРА ')
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
    elif message.text == 'go':
        button1 = KeyboardButton(text='Q20')
        button2 = KeyboardButton(text='Q25')
        button3 = KeyboardButton(text='Q32')
        button4 = KeyboardButton(text='Q40')
    
        button5 = KeyboardButton(text='20*45')    
        button6 = KeyboardButton(text='20*90')
        button7 = KeyboardButton(text='25*45') 

        button8 = KeyboardButton(text='25*90')
        button9 = KeyboardButton(text='32*45')
        button10 = KeyboardButton(text='32*90')
        button11 = KeyboardButton(text='40*90')  

        button12 = KeyboardButton(text='20*20*20')
        button13 = KeyboardButton(text='25*25*25')
        button14 = KeyboardButton(text='32*32*32') 
        button15 = KeyboardButton(text='25*20*25')

        button16 = KeyboardButton(text='32*20*32')
        button17 = KeyboardButton(text='32*25*32')
        button18 = KeyboardButton(text='back')

        markup1 = ReplyKeyboardBuilder([[button1]]).row(button2).row(button3).row(button4).row(button5).row(button6).row(button7).row(button8).row(button9).row(button10).row(button11).row(button12).row(button13).row(button14).row(button15).row(button16).row(button17).row(button18).as_markup()
        await message.answer(
            text='Выберите размер',
            reply_markup=markup1
        )
        print('choose fit name 3')
        await state.set_state(SetParameterFit.choosing_fitting_tube_3)
    else:
        button1 = KeyboardButton(text='Q20')
        button2 = KeyboardButton(text='Q25')
        button3 = KeyboardButton(text='Q32')
        button4 = KeyboardButton(text='Q40')
    
        button5 = KeyboardButton(text='20*45')    
        button6 = KeyboardButton(text='20*90')
        button7 = KeyboardButton(text='25*45') 

        button8 = KeyboardButton(text='25*90')
        button9 = KeyboardButton(text='32*45')
        button10 = KeyboardButton(text='32*90')
        button11 = KeyboardButton(text='40*90')  

        button12 = KeyboardButton(text='20*20*20')
        button13 = KeyboardButton(text='25*25*25')
        button14 = KeyboardButton(text='32*32*32') 
        button15 = KeyboardButton(text='25*20*25')

        button16 = KeyboardButton(text='32*20*32')
        button17 = KeyboardButton(text='32*25*32')
        button18 = KeyboardButton(text='back')

        markup1 = ReplyKeyboardBuilder([[button1]]).row(button2).row(button3).row(button4).row(button5).row(button6).row(button7).row(button8).row(button9).row(button10).row(button11).row(button12).row(button13).row(button14).row(button15).row(button16).row(button17).row(button18).as_markup()
        await state.update_data(chosen_fit_name_1=message.text.lower())
        await message.answer(
            text='Выберите размер',
            reply_markup=markup1
        )
        print('choose fit name 3')
        await state.set_state(SetParameterFit.choosing_fitting_tube_3)

@router.message(SetParameterFit.choosing_fitting_tube_3)
async def pprc_tube(message: Message, state: FSMContext):
    if message.text == 'back':
        await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
        await state.set_state(SetParameterFit.choosing_fitting_tube_1)
    elif message.text == 'go':
        button1 = KeyboardButton(text='без резб')
        button2 = KeyboardButton(text='внутр резб')
        button3 = KeyboardButton(text='нар резб')
        button4 = KeyboardButton(text='прямой')
        button5 = KeyboardButton(text='переходной')    
        button6 = KeyboardButton(text='back')
        markup1 = ReplyKeyboardBuilder([[button1]]).row(button2).row(button3).row(button4).row(button5).row(button6).as_markup()
        await message.answer(
            text='Выберите тип продукции',
            reply_markup=markup1
        )
        print('choose fit name 3')
        await state.set_state(SetParameterFit.choosing_fitting_tube_4)
    else:
        button1 = KeyboardButton(text='без резб')
        button2 = KeyboardButton(text='внутр резб')
        button3 = KeyboardButton(text='нар резб')
        button4 = KeyboardButton(text='прямой')
        button5 = KeyboardButton(text='переходной')    
        button6 = KeyboardButton(text='back')
        markup1 = ReplyKeyboardBuilder([[button1]]).row(button2).row(button3).row(button4).row(button5).row(button6).as_markup()
        await state.update_data(chosen_fit_name_2=message.text.lower())
        await message.answer(
            text='Выберите тип продукции',
            reply_markup=markup1
        )
        print('choose fit name 3')
        await state.set_state(SetParameterFit.choosing_fitting_tube_4)


@router.message(SetParameterFit.choosing_fitting_tube_4)
async def pprc_tube(message: Message, state: FSMContext):
    if message.text == 'back':
        await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
        await state.set_state(SetParameterFit.choosing_fitting_tube_2)
    elif message.text == 'go':
        button1 = KeyboardButton(text='_')
        button2 = KeyboardButton(text='1')
        button3 = KeyboardButton(text='1/2')
        button4 = KeyboardButton(text='1/4')
        button5 = KeyboardButton(text='3/4')
        button6 = KeyboardButton(text='back')
        markup1 = ReplyKeyboardBuilder([[button1]]).row(button2).row(button3).row(button4).row(button5).row(button6).as_markup()
        await message.answer(
            text='Выберите шаг ',
            reply_markup=markup1
        )
        print('choose fit name_4')
        await state.set_state(SetParameterFit.choosing_fitting_tube_5)
    else:
        button1 = KeyboardButton(text='_')
        button2 = KeyboardButton(text='1')
        button3 = KeyboardButton(text='1/2')
        button4 = KeyboardButton(text='1/4')
        button5 = KeyboardButton(text='3/4')
        button6 = KeyboardButton(text='back')
        markup1 = ReplyKeyboardBuilder([[button1]]).row(button2).row(button3).row(button4).row(button5).row(button6).as_markup()
        await state.update_data(chosen_fit_name_3=message.text.lower())
        await message.answer(
            text='Выберите шаг ',
            reply_markup=markup1
        )
        print('choose fit name_4')
        await state.set_state(SetParameterFit.choosing_fitting_tube_5)

@router.message(SetParameterFit.choosing_fitting_tube_5)
async def pprc_tube(message: Message, state: FSMContext):
    if message.text == 'back':
        await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
        await state.set_state(SetParameterFit.choosing_fitting_tube_3)
    elif message.text == 'go':
        button1 = KeyboardButton(text='белый')
        button2 = KeyboardButton(text='серый')
        button3 = KeyboardButton(text='back')

        markup1 = ReplyKeyboardBuilder([[button1]]).row(button2).row(button3).as_markup()
        await message.answer(
            text='Выберите изделие (5 слово)',
            reply_markup=markup1
        )
        print('choose fit name_4')
        await state.set_state(SetParameterFit.choosing_tube_name)
    else:
        button1 = KeyboardButton(text='белый')
        button2 = KeyboardButton(text='серый')
        button3 = KeyboardButton(text='back')

        markup1 = ReplyKeyboardBuilder([[button1]]).row(button2).row(button3).as_markup()
        await state.update_data(chosen_fit_name_4=message.text.lower())
        await message.answer(
            text='Выберите изделие (5 слово)',
            reply_markup=markup1
        )
        print('choose fit name_4')
        await state.set_state(SetParameterFit.choosing_tube_name)

@router.message(SetParameterFit.choosing_tube_name)
async def pprc_nom_diameter(message: Message, state: FSMContext):
    if message.text == 'back':
        await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
        await state.set_state(SetParameterFit.choosing_fitting_tube_4)
    elif message.text == 'go':
        await message.answer(
            text="выберите номинальный диаметр фиттинга:",
            reply_markup=make_row_keyboard(available_diameters)
        )
        print('choose nom diameter')
        await state.set_state(SetParameterFit.choosing_fitting_nom_diameter)
    else:
        await state.update_data(chosen_fit_name_5=message.text.lower())
        await message.answer(
            text="выберите номинальный диаметр фиттинга:",
            reply_markup=make_row_keyboard(available_diameters)
        )
        print('choose nom diameter')
        await state.set_state(SetParameterFit.choosing_fitting_nom_diameter)

@router.message(SetParameterFit.choosing_fitting_nom_diameter)
async def pprc_view(message: Message, state: FSMContext):
    if message.text == 'back':
        await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
        await state.set_state(SetParameterFit.choosing_fitting_tube_5)
    elif message.text == 'go':
        await message.answer(
            text="оцените внешний вид фиттинга:",
            reply_markup=make_row_keyboard(available_answers)
        )
        print('choose view')
        await state.set_state(SetParameterFit.choosing_fitting_view)
    else:
        await state.update_data(chosen_nom_diameter=message.text.lower())
        await message.answer(
            text="оцените внешний вид фиттинга:",
            reply_markup=make_row_keyboard(available_answers)
        )
        print('choose view')
        await state.set_state(SetParameterFit.choosing_fitting_view)

@router.message(SetParameterFit.choosing_fitting_view, F.text.in_(available_answers))
async def pprc_functionality(message: Message, state: FSMContext):
    if message.text == 'back':
        await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
        await state.set_state(SetParameterFit.choosing_tube_name)
    elif message.text == 'go':
        await message.answer(
            text="оцените функциональность фиттинга:",
            reply_markup=make_row_keyboard(available_answers)
        )
        print('choose func')
        await state.set_state(SetParameterFit.choosing_fitting_functionality)
    else:
        await message.answer(
            text="оцените функциональность фиттинга:",
            reply_markup=make_row_keyboard(available_answers)
        )
        print('choose func')
        await state.set_state(SetParameterFit.choosing_fitting_functionality)

@router.message(SetParameterFit.choosing_fitting_functionality)
async def pprc_finish(message: Message, state: FSMContext):
    if message.text == 'back':
        await message.answer(
            text="go back",
            reply_markup=make_row_keyboard(['go'])
            )
        await state.set_state(SetParameterFit.choosing_fitting_nom_diameter)
    elif message.text == 'go':
        await message.answer(
                text="перейти к передаче данных",
                reply_markup=make_row_keyboard(available_proceeds)
        )
        await state.set_state(SetParameterFit.choosing_fitting_finish)
    else:
        await state.update_data(chosen_functionality=message.text.lower())
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
                text="Благодарю за заполненные данные. Отправьте фото подтверждение",
                reply_markup=ReplyKeyboardRemove()
        )
        print('success fitting')

        user_data['chosen_fit_name'] = user_data['chosen_fit_name_1'] + ' ' + user_data['chosen_fit_name_2'] + ' ' + user_data['chosen_fit_name_3'] + ' ' + user_data['chosen_fit_name_4'] + ' ' + user_data['chosen_fit_name_5']  
        conn = psycopg2.connect(dbname="neondb", user="zhanabayevasset", password="txDhFR1yl8Pi", host='ep-cool-poetry-346809.us-east-2.aws.neon.tech')
        cursor = conn.cursor()
        cursor.execute(f"""insert into fitting_vodop_params (WORKING,CONTROLLER_NAME,  STANOK,SHIFT, FITTING_NAME, BRAND, NOMINAL_DIAMETER, VIEW, FUNCTIONALITY, MASTER, created_at, updated_at,COLOR,STEP,PRODUCT_TYPE) values (TRUE,'{user_data['chosen_controller_name']}', '{user_data['chosen_stanok']}','{user_data['chosen_smena']}', '{user_data['chosen_fit_name']}',  '{user_data['chosen_tube']}', '{user_data['chosen_nom_diameter']}', '{user_data['chosen_view']}','{user_data['chosen_functionality']}',  '{user_data['chosen_name']}',  current_timestamp + interval'6 hours', current_timestamp + interval'6 hours', '{user_data['chosen_fit_name_5']}', '{user_data['chosen_fit_name_4']}', '{user_data['chosen_fit_name_3']}')""")
        conn.commit()
        cursor.close()
        conn.close()
        await state.set_state(SetParameterFit.send_photo)
