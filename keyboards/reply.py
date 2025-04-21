from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Расписание 📌'),
        KeyboardButton(text='Домашнее задание 📋'),
    ],
    [
        KeyboardButton(text='Настройки ⚙️')
    ]
],
                           resize_keyboard=True,
                           input_field_placeholder='Выберите пункт меню...'
)

user_main = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Расписание 📌'),
        KeyboardButton(text='Домашнее задание 📋'),
    ],
    [
        KeyboardButton(text='Настройки ⚙️')
    ]
],
                           resize_keyboard=True,
                           input_field_placeholder='Выберите пункт меню...'
)
