from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

phone = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Mening raqamim", request_contact=True)
        ]
    ],
    resize_keyboard=True
)
complete = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Topildi")
        ]
    ],
    resize_keyboard=True
)
