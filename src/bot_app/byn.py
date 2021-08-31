from aiogram import types
from aiogram.dispatcher import FSMContext
from . app import dp, bot, db
from . keybords import inline_answer
from . states import GoStates
from . currency_byn import currency_rate
from decimal import *
from datetime import datetime
from . import messages
from . transactions import get_balance_bitcoins
from . keybords import inline_new
from . import currency_usd

@dp.callback_query_handler(lambda c: c.data == 'byn', state=GoStates.go)
async def button_click_call_back(callback_query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await GoStates.byn.set()
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"Введите сумму, BYN:")

# Здесь получаем ответ, указывая состояние и передавая сообщение пользователя
@dp.message_handler(state=GoStates.byn)
async def process_message(message: types.Message, state: FSMContext):
    if currency_rate() != 'error':
        try:
            async with state.proxy() as data:
                data['text'] = message.text
                user_message = data['text']
            if Decimal(user_message) >= 50 and Decimal(user_message) <= 1500:
                # дальше обрабатываем сообщение, ведем рассчеты и выдаем ответ.
                balance = get_balance_bitcoins()

                BTC_BYN = currency_rate()
                money = round(Decimal(user_message)/Decimal(BTC_BYN), 8)

                BTC_USD = currency_usd.currency_rate()
                ONE_BIT = round(Decimal(1.5/BTC_USD), 8)

                if Decimal(balance) >= Decimal(money + ONE_BIT):

                    answer_for_user = f'Вам будет отправлено ' + str(money) + f' BTC. Продолжить?'
                    await bot.send_message(
                        message.from_user.id,
                        answer_for_user,
                        reply_markup=inline_answer,
                        parse_mode='HTML'
                    )
                    # Finish conversation
                    await state.finish()
                    await GoStates.pay.set()
                    if(not db.subscriber_exists(message.from_user.id)):
                        # add user
                        db.add_subscriber(
                            message.from_user.id,
                            rate="BYN", price=user_message, translation=str(money), created=str(datetime.now().strftime('%d/%m/%y-%H:%M:%S'))
                        )
                    else:
                        # if user has to DB that update his
                        db.update_subscription(
                            message.from_user.id,
                            rate="BYN", price=user_message, translation=str(money), created=str(datetime.now().strftime('%d/%m/%y-%H:%M:%S'))
                        )

                else:
                    await message.reply(messages.BALANCE_BYN_MESSAGE + f'Для перевода доступно {balance} BTC.', reply_markup=inline_new)


            elif Decimal(user_message) > 1500:
                await message.reply(f'Ваша сумма должна быть не более 1500 BYN: ')
            else:
                await message.reply(f'Ваша сумма должна быть не менее 50 BYN: ')
        except:
            await message.reply(f'Введите корректную сумму: ')
    else:
        await message.reply(messages.SERVER_ERROR)