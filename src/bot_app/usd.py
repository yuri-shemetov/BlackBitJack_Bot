from aiogram import types
from aiogram.dispatcher import FSMContext
from . app import dp, bot, db
from . keybords import inline_answer
from . states import GoStates
from . currency_usd import currency_rate
from decimal import *
from datetime import datetime

@dp.callback_query_handler(lambda c: c.data == 'usd', state=GoStates.go)
async def button_click_call_back(callback_query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await GoStates.usd.set()
    await bot.answer_callback_query(callback_query.id)
    answer = callback_query.data 
    await bot.send_message(callback_query.from_user.id, f"Введите сумму $:")

# Здесь получаем ответ, указывая состояние и передавая сообщение пользователя
@dp.message_handler(state=GoStates.usd)
async def process_message(message: types.Message, state: FSMContext):
    
    try:
        async with state.proxy() as data:
            data['text'] = message.text
            user_message = data['text']
        if Decimal(user_message) >= 20:
            # дальше обрабатываем сообщение, ведем рассчеты и выдаем ответ.
            BTC_USD = currency_rate()
            money = round(Decimal(user_message)/Decimal(BTC_USD), 5)
            answer_for_user = f'Вам будет отправлено ' + str(money) + f'BTC'
            await bot.send_message(
                message.from_user.id,
                answer_for_user ,
                reply_markup=inline_answer,
                parse_mode='HTML',
            )

            # Finish conversation
            await state.finish()  
            await GoStates.go.set()

            # ADD or UPDATE for User in DATABASE

            if(not db.subscriber_exists(message.from_user.id)):
                # add user
                db.add_subscriber(message.from_user.id, rate="USD", price=user_message, translation=str(money), created=str(datetime.now()))
            else:
                # if user has to DB that update his
                db.update_subscription(message.from_user.id, rate="USD", price=user_message, translation=str(money), created=str(datetime.now()))

        else:
            await message.reply(f'Ваша сумма должна быть не менее 20$: ')
    except:
       await message.reply(f'Введите корректную сумму: ')