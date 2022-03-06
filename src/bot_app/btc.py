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
from . import open_settings

@dp.callback_query_handler(lambda c: c.data == 'btc', state=GoStates.go)
async def button_click_call_back(callback_query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await GoStates.btc.set()
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"Введите количество биткоинов, BTC:")

# Здесь получаем ответ, указывая состояние и передавая сообщение пользователя
@dp.message_handler(state=GoStates.btc)
async def process_message(message: types.Message, state: FSMContext):
    if currency_rate() != 'error':
        try:
            async with state.proxy() as data:
                data['text'] = message.text
                user_message = data['text']
            BTC_BYN = currency_rate()
            MIN_BTC = round(Decimal((50-Decimal(open_settings.fees())-Decimal(0.5))/BTC_BYN), 5)
            MAX_BTC = round(Decimal((1500-Decimal(open_settings.fees())-Decimal(0.5))/BTC_BYN), 5)
            if Decimal(user_message) >= MIN_BTC and Decimal(user_message) <= MAX_BTC:
                # дальше обрабатываем сообщение, ведем рассчеты и выдаем ответ.
                balance = get_balance_bitcoins()

                BTC_USD = currency_usd.currency_rate()
                ONE_BIT = round(Decimal(3/BTC_USD), 8)

                if (Decimal(user_message) + Decimal(ONE_BIT)) <= Decimal(balance):
                    money = round(Decimal(user_message)*Decimal(BTC_BYN) + Decimal(open_settings.fees()) + Decimal(0.5), 0)
                    answer_for_user = \
                        f'Стоимость указанного Вами количества биткоинов составит ' + str(money) + f' BYN. Отправка транзакции осуществляется с ПРИОРИТЕТОМ. Продолжить?'
                    await bot.send_message(
                        message.from_user.id,
                        answer_for_user,
                        reply_markup=inline_answer,
                        parse_mode='HTML')

                    # Finish conversation
                    await state.finish()
                    await GoStates.pay.set()

                    if(not db.subscriber_exists(message.from_user.id)):
                        # add user
                        db.add_subscriber(
                            message.from_user.id,
                            rate="BTC", price=str(money), translation=user_message, created=str(datetime.now().strftime('%d/%m/%y-%H:%M:%S'))
                        )
                    else:
                        # if user has to DB that update his
                        db.update_subscription(
                            message.from_user.id,
                            rate="BTC", price=str(money), translation=user_message, created=str(datetime.now().strftime('%d/%m/%y-%H:%M:%S'))
                        )
                else:
                    await message.reply(messages.BALANCE_BIT_MESSAGE + f'Для перевода доступно {balance} BTC.', reply_markup=inline_new)

            elif Decimal(user_message) > MAX_BTC:
                await message.reply(f'Количество биткоинов должно быть не более {MAX_BTC} BTC: ')
            else:
                await message.reply(f'Количество биткоинов должно быть не менее {MIN_BTC} BTC: ')
        except:
           await message.reply(f'Введите корректную сумму (десятичную часть отделяйте только точкой!): ')
    else:
        await message.reply(messages.SERVER_ERROR)