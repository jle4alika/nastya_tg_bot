from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
import database.requests.get as get
router = Router()

@router.message(F.text == 'Домашнее задание 📋')
async def homework(message: Message):
    homework = await get.get_homework(message.from_user.id)
    if homework != '':
        await message.answer(homework)
    else:
        await message.answer('Домашнего задания нету, либо его не установил староста.')

























