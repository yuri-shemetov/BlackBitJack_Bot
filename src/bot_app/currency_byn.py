import requests
from django import template
from . import currency_usd
from decimal import *
from . my_local_settings import CURRENCY_RATE_FOR_ONE_BITCON, PERCENT

register = template.Library()

DOLLAR_RUB = 'https://www.nbrb.by/api/exrates/rates/431'

def currency_rate():
    response = requests.get(DOLLAR_RUB)
    try:
        response.raise_for_status()
        res = requests.get(DOLLAR_RUB)
        digits = res.json().get('Cur_OfficialRate')
        BTC_USD = currency_usd.currency_rate()
        byn = Decimal(BTC_USD) * Decimal(digits) * Decimal((PERCENT/100)+1)
        if Decimal(byn) <= Decimal(CURRENCY_RATE_FOR_ONE_BITCON):
            byn = CURRENCY_RATE_FOR_ONE_BITCON
    except:
        byn = 'error'
    return byn
