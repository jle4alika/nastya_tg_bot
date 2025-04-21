import asyncio

from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters.command import CommandStart, Command
from aiogram.fsm.context import FSMContext
import database.requests.get as get
import database.requests.add as add
import database.requests.others as set
from aiogram.fsm.state import State, StatesGroup
from aiogram.enums import ParseMode
import keyboards.inline as kb
import keyboards.reply as kbr
from aiogram.types import FSInputFile
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

import qrcode
import re
import os
from dotenv import load_dotenv, find_dotenv
from pyrogram import Client
from pyrogram.raw.functions.contacts import ResolveUsername


load_dotenv(find_dotenv())

router = Router()

pyrogram_client = Client(
    "michael",
    api_id=25172187,
    api_hash="c163275c64658d29c719f13786a92cbb",
    bot_token=os.getenv('TOKEN'),
    in_memory=False
)
async def resolve_username_to_user_id(username: str) -> int | None:
    try:
        await pyrogram_client.start()
    finally:
        r = await pyrogram_client.invoke(ResolveUsername(username=username))
        if r.users:
            return r.users[0].id


class Reg(StatesGroup):
    faculty = State()
    group = State()

class Settings(StatesGroup):
    edit_name = State()
    schedule = State()
    homework_edit = State()
    homework_add_and_edit = State()
    new_headman = State()
    new_deputy = State()
    mail = State()


@router.message(CommandStart())
async def start(message: Message, bot: Bot):
    user_bool = await get.get_user_bool(message.from_user.id)
    user_group = await get.get_user_group(message.from_user.id)
    if not user_bool or user_group == 0:
        await message.answer(
            '🎓 Привет, студент! Добро пожаловать в наш бот! Здесь ты можешь найти помощь с учебой, задать вопросы и получить советы. Чем могу помочь сегодня? 📚✨')
        start_command = message.text
        username = message.from_user.username
        referrer_id = str(start_command[7:])
        if str(referrer_id) != '':
            if str(referrer_id) != str(message.from_user.id):
                await set.set_user(message.from_user.id, int(referrer_id))
                await add.add_group_member(referrer_id)
                title = await get.get_group_title(referrer_id)
                await message.answer(f'Вы успешно вступили в группу {title} 📚✨',
                                     reply_markup=kbr.user_main)
                await bot.send_message(referrer_id, f'В группу вступил новый пользователь @{username}')
            else:
                await message.answer('<ins>Нельзя</ins> регистрироваться по собственной ссылке!', parse_mode=ParseMode.HTML)
        else:
            await message.answer('\n\nВыбери одну из опций, чтобы начать:'
                                 '\n\n🎓 <b>Я студент</b> — доступ к расписанию и домашней работе.'
                                 '\n🧑‍🏫 <b>Я староста</b> — управление группой и важные обновления',
                                 reply_markup=kb.user,
                                 parse_mode=ParseMode.HTML)
    else:
        user = await get.get_group_headman(message.from_user.id)
        deputy = await get.get_group_deputy(message.from_user.id)
        if user == message.from_user.id or deputy == message.from_user.id:
            await message.answer(
                '🎓 Привет, студент! Добро пожаловать в наш бот! Здесь ты можешь найти помощь с учебой, задать вопросы и получить советы. Чем могу помочь сегодня? 📚✨',
            reply_markup=kbr.main)
        else:
            await message.answer(
                '🎓 Привет, студент! Добро пожаловать в наш бот! Здесь ты можешь найти помощь с учебой, задать вопросы и получить советы. Чем могу помочь сегодня? 📚✨',
            reply_markup=kbr.user_main)

@router.callback_query(F.data == 'student')
async def student(callback: CallbackQuery):
    await callback.message.answer(
        'Чтобы получить доступ к группе, пожалуйста, <b>свяжись со старостой</b> и попроси у него ссылку или отсканируй QR-код. 📲'
        '\n\nУдачи в учебе! 🍀',
        parse_mode=ParseMode.HTML)
    await asyncio.sleep(1)
    await callback.message.answer('🌟<b> Не забудьте подписаться на наш канал с новостями! </b>🌟'
                                  '\n\nЧтобы всегда быть в курсе последних обновлений и новостей о нашем боте, подписывайтесь на наш канал: @vankavstanka_altgtu_news (https://t.me/vankavstanka_altgtu_news).'
                                  '\n\nБудьте первыми, кто узнает о новых функциях и улучшениях! 🚀'
                                  '\n\nСпасибо, что вы с нами! ❤️',
                                  parse_mode=ParseMode.HTML,
                                  reply_markup=kb.news)

@router.callback_query(F.data == 'headman')
async def headman(callback: CallbackQuery):
    await set.set_user(callback.from_user.id)
    await callback.message.answer('При добавлении группы ты сможешь:'
                                  '\n\n• Изменять расписание 🗓️'
                                  '\n\n• Добавлять домашнюю работу 📚'
                                  '\n\n• Делать рассылку своим одногруппникам 🚀',
                                  reply_markup=kb.start)

@router.callback_query(F.data == 'new_group')
async def new_group(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('<b>▎Пожалуйста, введите информацию о <ins>вашем факультете</ins></b>',
                                  parse_mode=ParseMode.HTML)
    await state.set_state(Reg.faculty)

@router.message(Reg.faculty)
async def faculty(message: Message, state: FSMContext):
    await state.update_data(faculty=message.text)
    await message.answer('<b>▎Пожалуйста, введите название <ins>вашей группы</ins></b>',
                         parse_mode=ParseMode.HTML)
    await state.set_state(Reg.group)


@router.message(Reg.group)
async def group(message: Message, state: FSMContext):
    counter = 0
    for title in await get.get_groups_titles():
        if title == message.text:
            counter += 1
    if counter == 0:
        await state.update_data(group=message.text)
        data = await state.get_data()
        await message.answer(f'Вы создали группу {data["group"]} ✨', reply_markup=kbr.main)
        await state.clear()
        await set.set_group(message.from_user.id, data["group"], data["faculty"])
        await set.set_user_group(message.from_user.id, message.from_user.id)
        await add.add_group_member(message.from_user.id)
        await asyncio.sleep(1)

        headman = await get.get_group_headman(message.from_user.id)
        link = f'https://t.me/vanka_altgtu_bot?start={headman}'

        if os.path.exists(rf"qr-codes\{headman}.jpg"):
            qr = FSInputFile(f"qr-codes/{headman}.jpg")

        else:
            # имя конечного файла
            filename = f"qr-codes/{headman}.jpg"
            # генерируем qr-код
            img = qrcode.make(link)
            # сохраняем img в файл
            img.save(filename)
            qr = FSInputFile(f"qr-codes/{headman}.jpg")
        await message.answer_photo( photo=qr,
                                    caption=f'Привет, {message.from_user.first_name}! 👋'
                                            '\n\nНадеюсь, у тебя всё хорошо!'
                                            '\n\nЯ подготовил(а) QR-код и ссылку для вступления в нашу группу. Пожалуйста, поделись ими с новыми участниками, чтобы они могли легко присоединиться!'
                                            f'\n\n🔗 Ссылка для вступления:\n{link}'
                                            f'\n\nЕсли у тебя возникнут вопросы или понадобится помощь, дай знать!'
                                            f'\n\nСпасибо за твою работу! 💪')

        await asyncio.sleep(1)
    else:
        await message.answer('Данная группа уже зарегистрированна.\nВведите другое название группы, либо обратитесь к старосте.')


@router.message(F.text == 'Настройки ⚙️')
async def settings(message: Message):
    headman = await get.get_group_headman(message.from_user.id)
    deputy = await get.get_group_deputy(message.from_user.id)
    if headman == message.from_user.id:
        await message.answer('Добро пожаловать в Настройки ⚙️! \n'
                             'Как вы видите, вы можете передать права старосты, назначить заместителя, назначить домашнее задание, назначить расписание и сделать рассылку свои одногруппникам',
                             reply_markup=kb.headman_settings)
    elif deputy == message.from_user.id:
        await message.answer('Добро пожаловать в Настройки ⚙️! \n'
                             'Как вы видите, вы можете назначить домашнее задание и сделать рассылку свои одногруппникам',
                             reply_markup=kb.deputy_settings)
    else:
        await message.answer('Добро пожаловать в Настройки ⚙️! \n'
                             'Как вы видите, вы можете покинуть группу',
                             reply_markup=kb.user_settings)


@router.callback_query(F.data  == 'upload_schedule')
async def upload_schedule(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Напиши текст расписания:')
    await state.set_state(Settings.schedule)

@router.message(Settings.schedule)
async def schedule(message: Message, state: FSMContext):
    if message.text.lower() == 'назад':
        await message.answer('Вы успешно отменили установку расписания!')
        await state.clear()
        return

    await add.add_schedule(message.from_user.id, message.text)
    await message.answer('Вы успешно установили расписание! Старое расписание будет удалено...')
    await state.clear()


@router.callback_query(F.data == 'leave_from_group')
async def leave_from_group(callback: CallbackQuery):
    await set.set_user_group(callback.from_user.id, 0)

    headman = await get.get_group_headman(callback.from_user.id)
    await add.minus_group_member(headman)

    await callback.answer('Вы успешно покинули группу')


@router.callback_query(F.data == 'edit_group_name')
async def leave_from_group(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Settings.edit_name)
    await callback.message.answer('<b>▎Пожалуйста, введите новое название <ins>вашей группы</ins></b>',
                                  parse_mode=ParseMode.HTML,
                                  reply_markup=kb.edit_group_name)

@router.message(Settings.edit_name)
async def edit_group(message: Message, state: FSMContext):
    data = message.text
    await state.update_data(edit_name=data)
    await message.answer(f'Вы успешно изменили название группы на {data}')
    await state.clear()


@router.callback_query(F.data == 'no_edit')
async def no_edit(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer('Вы успешно отменили изменение названия группы')


@router.callback_query(F.data == 'change_homework')
async def set_homework(callback: CallbackQuery):
    headman = await get.get_group_headman(callback.from_user.id)
    homework = await get.get_homework(headman)
    await callback.message.answer(f'Текущее домашнее задание:\n\n {homework}', reply_markup=kb.set_homework)

@router.callback_query(F.data == 'edit')
async def set_homework(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Settings.homework_edit)
    await callback.message.answer('Введите <ins>новое домашнее задание</ins>', parse_mode=ParseMode.HTML)

@router.callback_query(F.data == 'add_and_edit')
async def set_homework(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Settings.homework_add_and_edit)
    await callback.message.answer('Введите то, <ins>что хотите добавить</ins>', parse_mode=ParseMode.HTML)


@router.message(Settings.homework_add_and_edit)
async def get_new_homework(message: Message, state: FSMContext):
    await state.update_data(homework_add_and_edit=message.text)
    data = message.text
    headman = await get.get_group_headman(message.from_user.id)
    await add.add_and_edit_homework(headman, data)
    homework = await get.get_homework(message.from_user.id)
    await message.answer(f'Вы изменили домашнее задание на: \n\n {homework}', reply_markup=kb.finish_homework_add_and_edit)


@router.message(Settings.homework_edit)
async def get_new_homework(message: Message, state: FSMContext):
    await state.update_data(homework_edit=message.text)
    data = message.text
    headman = await get.get_group_headman(message.from_user.id)
    await add.edit_homework(headman, data)
    homework = await get.get_homework(message.from_user.id)
    await message.answer(f'Вы изменили домашнее задание на: \n\n {homework}', reply_markup=kb.finish_homework_edit)


@router.callback_query(F.data == 'save_homework_edit')
async def save_homework(callback: CallbackQuery, state: FSMContext):
    homework = await get.get_homework(callback.from_user.id)
    await state.clear()
    await callback.message.answer(f'Вы успешно изменили домашнее задание на: \n\n {homework}')


@router.callback_query(F.data == 'save_homework_add_and_edit')
async def save_homework(callback: CallbackQuery, state: FSMContext):
    homework = await get.get_homework(callback.from_user.id)
    await state.clear()
    await callback.message.answer(f'Вы успешно изменили домашнее задание на: \n\n {homework}')


@router.callback_query(F.data == 'change_headman')
async def change_headman(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите юз нового старосты:')
    await state.set_state(Settings.new_headman)


@router.message(Settings.new_headman)
async def get_new_homework(message: Message, state: FSMContext, bot: Bot):
    mention = re.search(r'@(\w+)', message.text)

    await state.update_data(new_headman=message.text)

    if mention:
        username = mention.group(1)
        headman = await resolve_username_to_user_id(username)

        user = await get.get_user_bool(headman)
        old_headman = await get.get_user_group(headman)
        print(headman)
        print(old_headman)
        print(message.from_user.id)

        if headman != message.from_user.id and old_headman == message.from_user.id:
            users = await get.get_group_users(message.from_user.id)

            for user in users:
                await set.set_user_group(user, headman)

            await add.new_headman(message.from_user.id, headman)
            await message.answer(f'Вы успешно передали права старосты - @{username}!', reply_markup=kbr.user_main)
            await bot.send_message(headman, 'Вам передали права старосты в группе!', reply_markup=kbr.main)

        elif not user:
            await message.answer('Данный пользователь не зарегистрирован в боте.')

        elif headman == message.from_user.id:
            await message.answer('Вы не можете себя снова назначить старостой')

        elif old_headman != message.from_user.id:
            await message.answer('Данный пользователь не находится в вашей группе.')

        await state.clear()


@router.callback_query(F.data == 'change_deputy')
async def change_deputy(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите юз нового заместителя старосты:')
    await state.set_state(Settings.new_deputy)


@router.message(Settings.new_deputy)
async def get_new_deputy(message: Message, state: FSMContext, bot: Bot):
    mention = re.search(r'@(\w+)', message.text)

    await state.update_data(new_deputy=message.text)

    if mention:
        username = mention.group(1)
        deputy = await resolve_username_to_user_id(username)

        user = await get.get_user_bool(deputy)
        headman = await get.get_user_group(deputy)
        if deputy != message.from_user.id and headman == message.from_user.id:
            await add.new_deputy(message.from_user.id, deputy)
            await message.answer(f'Вы успешно передали права заместителя старосты - @{username}!')
            await bot.send_message(deputy, 'Вам передали права заместителя старосты в группе!', reply_markup=kbr.main)

        elif not user:
            await message.answer('Данный пользователь не зарегистрирован в боте.')

        elif deputy == message.from_user.id:
            await message.answer('Вы не можете назначить себя заместителем старосты.')

        elif headman != message.from_user.id:
            await message.answer('Данный пользователь не находится в вашей группе.')

        await state.clear()

@router.callback_query(F.data == 'link')
async def change_headman(callback: CallbackQuery):
    headman = await get.get_group_headman(callback.from_user.id)
    link = f'https://t.me/vanka_altgtu_bot?start={headman}'

    if os.path.exists(rf"qr-codes\{headman}.jpg"):
        qr = FSInputFile(f"qr-codes/{headman}.jpg")
        await callback.message.answer_photo(photo=qr,
                                            caption=f'Привет, {callback.from_user.first_name}! 👋'
                                                    '\n\nНадеюсь, у тебя всё хорошо!'
                                                    '\n\nЯ подготовил(а) QR-код и ссылку для вступления в нашу группу. Пожалуйста, поделись ими с новыми участниками, чтобы они могли легко присоединиться!'
                                                    f'\n\n🔗 Ссылка для вступления:\n{link}'
                                                    f'\n\nЕсли у тебя возникнут вопросы или понадобится помощь, дай знать!'
                                                    f'\n\nСпасибо за твою работу! 💪')
    else:
        # имя конечного файла
        filename = f"qr-codes/{headman}.jpg"
        # генерируем qr-код
        img = qrcode.make(link)
        # сохраняем img в файл
        img.save(filename)
        qr = FSInputFile(f"qr-codes/{headman}.jpg")
        await callback.message.answer_photo(photo=qr,
                                            caption=f'Привет, {callback.from_user.first_name}! 👋'
                                                    '\n\nНадеюсь, у тебя всё хорошо!'
                                                    '\n\nЯ подготовил(а) QR-код и ссылку для вступления в нашу группу. Пожалуйста, поделись ими с новыми участниками, чтобы они могли легко присоединиться!'
                                                    f'\n\n🔗 Ссылка для вступления:\n{link}'
                                                    f'\n\nЕсли у тебя возникнут вопросы или понадобится помощь, дай знать!'
                                                    f'\n\nСпасибо за твою работу! 💪')

@router.callback_query(F.data == 'mailing_list')
async def change_headman(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('🚀 Введите сообщение для рассылки')
    await state.set_state(Settings.mail)


@router.message(Settings.mail)
async def mailing(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(mail=message.text)
    mail = f'📢 Привет, друзья! 🌟 Это ваш староста, и у меня для вас важные новости! \n\n<blockquote><b>{message.text}</b></blockquote>'

    headman = await get.get_group_headman(message.from_user.id)
    users = await get.get_group_users(headman)
    for user in users:
        await bot.send_message(user, mail, parse_mode=ParseMode.HTML)


