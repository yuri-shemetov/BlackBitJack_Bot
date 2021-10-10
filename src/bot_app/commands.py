from aiogram import types
from . app import dp, bot, db
from . import messages
from aiogram.dispatcher import FSMContext
from . keybords import inline_new, inline_rate, inline_pay, inline_photo_ok, inline_admin
from . states import GoStates
from datetime import datetime
from . mail import get_new_email
from . my_yadisk import save_to_yadisk, save_to_yadisk_wallet
from . wallet_balance import check_wallet
from . transactions import execute_transaction
from . cleaner import get_files_messages, get_files_photos, get_files_wallets, remove_old_files
from . black_list import black_list
from . my_local_settings import ADMIN
from decimal import *
import asyncio
from os import mkdir

# Start
@dp.message_handler(commands=['start'], state='*')
async def send_welcome(message: types.Message):
    for i in black_list:
        if message.from_user.id == int(i):                                                    
            await message.reply(messages.BLACK_LIST)
            break
    if message.from_user.id == ADMIN:
        await message.reply(messages.WELCOME_ADMIN, reply_markup=inline_admin)
        await GoStates.setting.set()
    if message.from_user.id != int(i) and message.from_user.id != ADMIN:
        await message.reply(messages.WELCOME_MESSAGE, reply_markup=inline_new)

# Cancel
@dp.callback_query_handler(lambda c: c.data == 'cancel', state='*')
async def button_click_call_back(callback_query: types.CallbackQuery):
    for i in black_list:
        if callback_query.from_user.id == int(i):
            await bot.send_message(callback_query.from_user.id, messages.BLACK_LIST)
            break
    if callback_query.from_user.id != int(i):
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, messages.CANCEL_MESSAGE, reply_markup=inline_new)

# New application
@dp.callback_query_handler(lambda c: c.data == 'new', state='*') 
async def button_click_call_back(callback_query: types.CallbackQuery):
    for i in black_list:
        if callback_query.from_user.id == int(i):
            await bot.send_message(callback_query.from_user.id, messages.BLACK_LIST)
            break
    if callback_query.from_user.id != int(i):
        await GoStates.go.set()
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, messages.CHOISE_RATE_MESSAGE, reply_markup=inline_rate)

# List commands for payment
@dp.callback_query_handler(lambda c: c.data == 'OK', state=GoStates.pay)
async def button_click_call_back(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    all_price = db.get_subscriptions_all_price(callback_query.from_user.id)
    text = ''
    for i in all_price:
        for all_text in i:
            text = text + str(all_text) + ' '
    text = 'Итого к оплате: *' + text + 'BYN*'
    await bot.send_message(callback_query.from_user.id, text + messages.NEXT_STEP_MESSAGE,
                           parse_mode="Markdown", reply_markup=inline_pay,)

# Upload photo
@dp.callback_query_handler(lambda c: c.data == 'paid', state=GoStates.pay)
async def button_click_call_back(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await state.finish()
    await GoStates.photo.set()
    await bot.send_message(callback_query.from_user.id, messages.UPLOAD_PHOTO_MESSAGE)

# Error photo upload
@dp.message_handler(content_types=["text", "sticker", "pinned_message", "audio"], state=GoStates.photo)
async def process_photo_invalid(message: types.Message):
    await message.reply(messages.UPLOAD_ERROR_MESSAGE)

# Successful photo upload
@dp.message_handler(content_types=["photo"], state=GoStates.photo)
async def process_photo(message: types.Message, state: FSMContext):
    photo = message.photo.pop()
    username = message.from_user.first_name
    id_user = str(message.from_user.id)
    lastname = ''
    if message.from_user.last_name != None:
        lastname = message.from_user.last_name
    try:
        mkdir(f"media/")
    except:
        pass
    path_jpg = 'media/' + str(datetime.now().strftime('%y_%m_%d__%H-%M-%S')) + '-' + username +'-' + lastname + '-' + id_user + '_' + '.jpg'
    await photo.download(path_jpg)  
    db.update_subscription_photo(message.from_user.id, photo=path_jpg)  
    await message.reply(messages.UPLOAD_OK_MESSAGE, reply_markup=inline_photo_ok)
    await state.finish()
    await GoStates.photo_ok.set()
    # send photo to yadisk
    save_to_yadisk(id_user=id_user, path_jpg=path_jpg)

# Upload address
@dp.callback_query_handler(lambda c: c.data == 'photo_ok', state=GoStates.photo_ok) 
async def button_click_call_back(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, messages.ENTER_ADDRESS_MESSAGE)
    await state.finish()
    await GoStates.address.set()

# Error address upload
@dp.message_handler(content_types=["photo", "sticker", "pinned_message", "audio"], state=GoStates.address)
async def process_address_invalid(message: types.Message):
    await message.reply(messages.ADDRESS_ERROR_MESSAGE)

# Successful address upload
@dp.message_handler(content_types=["text"], state=GoStates.address)
async def process_message(message: types.Message, state: FSMContext):
    try:
        # get address client
        async with state.proxy() as data:
            data['text'] = message.text
            user_message = data['text']

        # message on receipt of the application
        await bot.send_message(message.from_user.id, messages.STATUS_WAIT_MESSAGE,  parse_mode='HTML')

        # Remember address
        db.update_subscription_address(message.from_user.id, address=user_message)

        # Send address to yandex_disk
        username = message.from_user.first_name
        id_user = str(message.from_user.id)
        lastname = ''
        if message.from_user.last_name != None:
            lastname = message.from_user.last_name
        save_to_yadisk_wallet(username=username, lastname=lastname, id_user=id_user, user_message=user_message)

    except:
        await message.reply(messages.ADDRESS_ERROR_MESSAGE)

    # WAIT

    try:
        all_price = db.get_subscriptions_all_price(message.from_user.id)
        price = ''
        for i in all_price:
            for all_text in i:
                price = price + str(all_text)
        time_wait = 0
        while time_wait != 24:  #<--- 5*24=120 seconds or 2 minuts
            # check mail and get a new payment message
            money = get_new_email(price=price)
            #print(money)
            if Decimal(money) == Decimal(price):
                # transaction
                bitcoins = db.get_subscriptions_translation(message.from_user.id)
                translation = ''
                for i in bitcoins:
                    for all_text in i:
                        translation += str(all_text)
                execute_transaction(dest_address=user_message, translation=translation)

                # show a message about successful transaction and a wallet
                wallet = check_wallet(user_message)
                await bot.send_message(message.from_user.id, messages.GET_APLICATION + wallet, reply_markup=inline_new, parse_mode='HTML')

                # Finish conversation
                await state.finish()

                # delete old media files
                files = get_files_photos(path='media/')
                remove_old_files(path='media/', files=files)

                # delete old messages files
                files = get_files_messages(path='message/')
                remove_old_files(path='message/', files=files)

                # delete old wallets files
                files = get_files_wallets(path='wallet/')
                remove_old_files(path='wallet/', files=files)

                break
            await asyncio.sleep(5)
            time_wait += 1

        if Decimal(money) != Decimal(price):
            await message.answer(messages.CHECK_ERROR_MESSAGE_FROM_BANK, reply_markup=inline_new, parse_mode='HTML')
            await state.finish()
            pass
            

    except:
        await message.reply(messages.CHECK_ERROR_CONNECT_TO_EMAIL, reply_markup=inline_new, parse_mode='HTML')
        await state.finish()