import datetime

import asyncio

from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
import database.requests.get as get
import database.requests.add as add
import keyboards.inline as kb
from aiogram.filters.command import Command
from aiogram.enums import ParseMode


router = Router()


@router.message(F.text == 'Расписание 📌')
async def schedule(message: Message):
    schedule = await get.group_schedule(message.from_user.id)
    if schedule:
        await message.answer('Расписание:')
        await message.answer(schedule)
    else:
        await message.answer('Расписание не установлено старостой.')

@router.message(F.text.lower() == 'расписание')
async def schedule(message: Message):
    schedule = await get.group_schedule(message.from_user.id)
    if schedule:
        await message.answer('Расписание:')
        await message.answer(schedule)
    else:
        await message.answer('Расписание не установлено старостой.')



