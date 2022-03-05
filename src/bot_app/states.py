from aiogram.dispatcher.filters.state import State, StatesGroup

class GoStates(StatesGroup):
    start = State()
    setting = State()
    rate = State()
    fees = State()
    percent = State()
    go = State()
    btc = State()
    usd = State()
    byn = State()
    pay = State()
    photo = State()
    photo_ok = State()
    address = State()
    wait = State()
    rate = State()
    usd_byn = State()