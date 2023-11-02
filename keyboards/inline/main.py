from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data.config import BASE_URL
import requests


def towns(town_id: int):
    markup = InlineKeyboardMarkup(row_width=2)
    r = requests.get(url=f"{BASE_URL}/towns/?id={town_id}")
    dt = r.json()
    for i in dt:
        markup.insert(InlineKeyboardButton(i['name'], callback_data=i['id']))
    return markup


def cities(city_id: int, town_id: int):
    markup = InlineKeyboardMarkup(row_width=2)
    r = requests.get(url=f"{BASE_URL}/cities/?id={city_id}&town_id={town_id}")
    dt = r.json()
    for i in dt:
        markup.insert(InlineKeyboardButton(i['name'], callback_data=i['id']))
    return markup
