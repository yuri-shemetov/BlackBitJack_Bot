from aiogram import types
from . app import dp, bot
from . import messages
from aiogram.dispatcher import FSMContext
from . keybords import inline_admin, inline_setting
from . states import GoStates

# Setting
@dp.callback_query_handler(lambda c: c.data == 'setting', state=GoStates.setting)
async def button_click_call_back(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    file_rate = open('settings/currency_rate.txt')
    now_rate = file_rate.read()
    file_rate.close()
    file_fees = open('settings/fees.txt')
    now_fees = file_fees.read()
    file_fees.close()
    file_percent = open('settings/percent.txt')
    now_percent = file_percent.read()
    file_percent.close()
    await bot.send_message(callback_query.from_user.id, 
    f'Курс: {now_rate} BYN;\nКомиссия: {now_fees} BYN;\nПроцент: {now_percent} %;' + messages.SETTING, 
    reply_markup=inline_setting)
    await state.finish()
    await GoStates.rate.set()

# Upload Set_Rate
@dp.callback_query_handler(lambda c: c.data == 'rate', state=GoStates.rate) 
async def button_click_call_back(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Введите курс, BYN')

# Successful Set_Rate
@dp.message_handler(content_types=["text"], state=GoStates.rate)
async def process_message(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['text'] = message.text
            user_message = int(data['text'])
        file = open("settings/currency_rate.txt", "w+")
        file.write(f'{user_message}')
        file.close()
        await message.reply('Курс успешно изменен!', reply_markup=inline_admin)
        await state.finish()
        await GoStates.setting.set()
    except:
        await message.reply('Введите корректно курс')

# Upload Set_Fees
@dp.callback_query_handler(lambda c: c.data == 'fees', state=GoStates.rate) 
async def button_click_call_back(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Введите комиссию, BYN')
    await state.finish()
    await GoStates.fees.set()

# Successful Set_Fees
@dp.message_handler(content_types=["text"], state=GoStates.fees)
async def process_message(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['text'] = message.text
            user_message = float(data['text'])
        file = open("settings/fees.txt", "w+")
        file.write(f'{user_message}')
        file.close()
        await message.reply('Комиссия успешно изменена!', reply_markup=inline_admin)
        await state.finish()
        await GoStates.setting.set()
    except:
        await message.reply('Введите корректно коммисию, десятичную дробь пишите только точкой!')

# Upload Set_Persent
@dp.callback_query_handler(lambda c: c.data == 'percent', state=GoStates.rate) 
async def button_click_call_back(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Введите процент, %')
    await state.finish()
    await GoStates.percent.set()

# Successful Set_Fees
@dp.message_handler(content_types=["text"], state=GoStates.percent)
async def process_message(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['text'] = message.text
            user_message = float(data['text'])
        file = open("settings/percent.txt", "w+")
        file.write(f'{user_message}')
        file.close()
        await message.reply('Процент успешно изменен!', reply_markup=inline_admin)
        await state.finish()
        await GoStates.setting.set()
    except:
        await message.reply('Введите корректно процент, десятичную дробь пишите только точкой!')