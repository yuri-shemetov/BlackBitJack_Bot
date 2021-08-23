from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

inline_button_new = InlineKeyboardButton('Создать новую заявку', callback_data='new')
inline_button_btc = InlineKeyboardButton('BTC', callback_data='btc')
inline_button_byn = InlineKeyboardButton('BYN', callback_data='byn')
inline_button_yes = InlineKeyboardButton('OK', callback_data='OK')
inline_button_cancel = InlineKeyboardButton('Cancel', callback_data='cancel')
inline_button_paid = InlineKeyboardButton('Оплачено', callback_data='paid')
inline_button_photo_ok = InlineKeyboardButton('OK', callback_data='photo_ok')

# Keyboard

inline_photo_ok = InlineKeyboardMarkup()
inline_pay = InlineKeyboardMarkup()
inline_persona = InlineKeyboardMarkup()
inline_answer = InlineKeyboardMarkup()
inline_new = InlineKeyboardMarkup()
inline_rate = InlineKeyboardMarkup()

# Out

inline_photo_ok.add(inline_button_photo_ok)
inline_pay.row(inline_button_paid, inline_button_cancel)
inline_answer.row(inline_button_yes, inline_button_cancel)
inline_new.add(inline_button_new)
inline_rate.row(inline_button_byn, inline_button_btc)
