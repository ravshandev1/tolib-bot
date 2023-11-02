from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from data.config import BASE_URL
import requests
from loader import dp
from keyboards.inline.main import towns
from states.main import Client, Travel
from keyboards.default.main import phone


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    r = requests.get(url=f"{BASE_URL}/user/{message.from_user.id}/")
    if r.status_code == 404:
        await message.answer(
            f"Assalomu alaykum {message.from_user.full_name}! Botimizga xush kelibsiz!\nBotimizdan ro'yxatdan o'tish uchun telefon raqamingizni yozing!",
            reply_markup=phone)
        await Client.phone.set()
    elif r.status_code == 200:
        await message.answer("Qayerdasiz?", reply_markup=towns(0))
        await Travel.where.set()
