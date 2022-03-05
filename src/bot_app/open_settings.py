from decimal import *

#Текущий курс биткоина, комиссия и процент

file_rate = open('settings/currency_rate.txt')
now_rate = file_rate.read()
file_rate.close()
CURRENCY_RATE_FOR_ONE_BITCON = Decimal(now_rate)

file_fees = open('settings/fees.txt')
now_fees = file_fees.read()
file_fees.close()
FEES = Decimal(now_fees)

file_percent = open('settings/percent.txt')
now_percent = file_percent.read()
file_percent.close()
PERCENT = Decimal(now_percent)

file_byn = open('settings/byn.txt')
now_byn = file_byn.read()
file_byn.close()
BYN = Decimal(now_byn)