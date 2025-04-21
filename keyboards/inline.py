from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

start = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Добавить группу 👥', callback_data='new_group')
        ]
    ]
)


user = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Я студент 🎓', callback_data='student')
        ],
        [
            InlineKeyboardButton(text='Я староста 🧑‍🏫', callback_data='headman')
        ]
    ]
)

user_settings = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Покинуть группу ❌', callback_data='leave_from_group')
        ]
    ]
)


headman_settings = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Передать права старосты 🔄', callback_data='change_headman')
        ],
        [
            InlineKeyboardButton(text='Изменить расписание 📚', callback_data='upload_schedule')
        ],
        [
            InlineKeyboardButton(text='Назначить заместителя 🔄', callback_data='change_deputy')
        ],
        [
            InlineKeyboardButton(text='Изменить название группы ✏️', callback_data='edit_group_name'),
        ],
        [
            InlineKeyboardButton(text='Изменить домашнее задание 📚', callback_data='change_homework')
        ],
        [
            InlineKeyboardButton(text='Рассылка одногруппникам 🚀', callback_data='mailing_list')
        ],
        [
            InlineKeyboardButton(text='Ссылка на вступление 🔗', callback_data='link')
        ]
    ]
)

deputy_settings = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Изменить домашнее задание 📚', callback_data='change_homework')
        ],
        [
            InlineKeyboardButton(text='Рассылка одногруппникам 🚀', callback_data='mailing_list')
        ],
        [
            InlineKeyboardButton(text='Ссылка на вступление 🔗', callback_data='link')
        ],
    ]
)

schedule = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Сегодня ⏳', callback_data='today'),
            InlineKeyboardButton(text='Завтра 📆', callback_data='tomorrow')
        ],
        [
            InlineKeyboardButton(text='Неделя 🗓️', callback_data='week')
        ]
    ]
)

set_homework = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Изменить ✏️', callback_data='edit'),
            InlineKeyboardButton(text='Добавить ➕', callback_data='add_and_edit')
        ]
    ]
)


finish_homework_edit = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Сохранить изменения 💾', callback_data='save_homework_edit')
        ],
        [
            InlineKeyboardButton(text='Изменить ✏️', callback_data='edit'),
            InlineKeyboardButton(text='Добавить ➕', callback_data='add_and_edit')
        ]
    ]
)

finish_homework_add_and_edit = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Сохранить изменения 💾', callback_data='save_homework_add_and_edit')
        ],
        [
            InlineKeyboardButton(text='Изменить ✏️', callback_data='edit'),
            InlineKeyboardButton(text='Добавить ➕', callback_data='add_and_edit')
        ]
    ]
)


donate = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Поддержать 💖', url='https://www.donationalerts.com/r/jle4alika')
        ]
    ]
)

news = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Подписаться ✅', url='https://t.me/vankavstanka_altgtu_news')
        ]
    ]
)


edit_group_name = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Отмена ❌', callback_data='no_edit')
        ]
    ]
)