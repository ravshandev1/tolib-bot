from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from data.config import BASE_URL
import requests
from loader import dp
from states.main import Client, Travel
from keyboards.default.main import complete
from keyboards.inline.main import towns, cities


@dp.message_handler(state=Client.phone, content_types=['contact'])
async def a(mes: Message, state: FSMContext):
    await mes.answer("Muvaffaqiyatli ro'yxatdan o'tdingiz!", reply_markup=ReplyKeyboardRemove())
    data = dict()
    data['full_name'] = mes.from_user.full_name
    data['username'] = f"https://t.me/{mes.from_user.username}"
    data['telegram_id'] = mes.from_user.id
    if mes.contact:
        data['phone'] = mes.contact.phone_number
    else:
        data['phone'] = mes.text
    r = requests.post(url=f"{BASE_URL}/user/client/", data=data)
    if r.status_code == 201:
        await mes.answer("Qayerdasiz?", reply_markup=towns(0))
        await Travel.where.set()
    else:
        await mes.answer("Xato")
        await state.finish()


@dp.callback_query_handler(state=Travel.where)
async def a(call: CallbackQuery, state: FSMContext):
    await state.update_data({'where': call.data})
    await call.message.edit_text("Qaysi tumandan?", reply_markup=cities(city_id=0, town_id=int(call.data)))
    await Travel.next()
    await call.answer(cache_time=1)


@dp.callback_query_handler(state=Travel.where_city)
async def a(call: CallbackQuery, state: FSMContext):
    t_id = await state.get_data()
    await state.update_data({'where_city': call.data})
    await call.message.edit_text("Qayerga borasiz?", reply_markup=towns(int(t_id['where'])))
    await Travel.next()
    await call.answer(cache_time=1)


@dp.callback_query_handler(state=Travel.to_where)
async def a(call: CallbackQuery, state: FSMContext):
    c_id = await state.get_data()
    await state.update_data({'to_where': call.data})
    await call.message.edit_text("Qaysi tumaniga?",
                                 reply_markup=cities(city_id=int(c_id['where_city']), town_id=int(call.data)))
    await Travel.next()
    await call.answer(cache_time=1)


@dp.callback_query_handler(state=Travel.to_where_city)
async def a(call: CallbackQuery, state: FSMContext):
    await state.update_data({'to_where_city': call.data})
    await call.message.delete()
    await call.message.answer("Yulovchilar sonini kiriting!")
    await Travel.next()
    await call.answer(cache_time=1)


@dp.message_handler(state=Travel.count_person)
async def a(mes: Message, state: FSMContext):
    await state.update_data({'count_person': mes.text})
    data = await state.get_data()
    r = requests.post(url=f"{BASE_URL}/?telegram_id={mes.from_user.id}", data=data)
    if r.status_code == 201:
        await mes.answer(
            "Ma'lumotlaringizni taksislarga yubordik!\nSizga aloqaga chiqishadi!\nAgarda taksi topilsa <b>Topildi</b> tugmasini bosing!",
            reply_markup=complete)
        travel_id = r.json()
        await state.update_data({'id': travel_id['id']})
        await Travel.next()
    else:
        await mes.answer("Xato\nBoshidan urinib kuring!")
        await Travel.where.set()


@dp.message_handler(state=Travel.complete)
async def a(mes: Message, state: FSMContext):
    if mes.text == "Topildi":
        dt = await state.get_data()
        r = requests.patch(url=f"{BASE_URL}/?id={dt['id']}")
        if r.status_code == 200:
            await mes.answer("Botimizdan foydalanganiz uchun raxmat!", reply_markup=ReplyKeyboardRemove())
            await mes.answer("Qayerdasiz?", reply_markup=towns(0))
        else:
            await mes.answer("Xato")
    await state.finish()
    await Travel.where.set()
