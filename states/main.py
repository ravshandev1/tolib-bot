from aiogram.dispatcher.filters.state import State, StatesGroup


class Client(StatesGroup):
    phone = State()


class Travel(StatesGroup):
    where = State()
    where_city = State()
    to_where = State()
    to_where_city = State()
    count_person = State()
    complete = State()
