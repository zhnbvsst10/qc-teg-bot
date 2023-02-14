from aiogram import Router
from aiogram.filters.command import Command
from aiogram.filters.text import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, KeyboardButton,ReplyKeyboardMarkup
from datetime import datetime
import time

router = Router()


@router.message(Command(commands=["start"]))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    kb6 = [[KeyboardButton(text='PVC трубa'),KeyboardButton(text='PPR-C трубa') ]]
    kb = [[KeyboardButton(text='PVC труба'),KeyboardButton(text='PPR-C труба') ]]
    keyboard6 = ReplyKeyboardMarkup(keyboard=kb6,resize_keyboard=True)
    keyboard = ReplyKeyboardMarkup(keyboard=kb,resize_keyboard=True)
    for i in range(10):
        time.sleep(60 * 1)
        #await state.clear()
        if datetime.now().minute in [8,12,16]:
            await message.answer(
                text="Выберите изделие: ",
                reply_markup=keyboard
                )
        else:
            await message.answer(
                    text="Выберите изделие: ",
                    reply_markup=keyboard6
                    )
        
    # if datetime.now().hour in [8,11,14,17,20]:
    #     await message.answer(
    #             text="Выберите изделие: ",
    #             reply_markup=keyboard
    #             )
    # else:
    #     await message.answer(
    #             text="Выберите изделие: ",
    #             reply_markup=keyboard6
    #             )



@router.message(Command(commands=["cancel"]))
@router.message(Text(text="отмена", ))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Действие отменено",
        reply_markup=ReplyKeyboardRemove()
    )