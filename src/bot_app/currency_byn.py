import requests
from django import template
from . import currency_usd
from decimal import *
from . open_settings import CURRENCY_RATE_FOR_ONE_BITCON, PERCENT, BYN

register = template.Library()

def currency_rate():
    try:
        digits = BYN
        BTC_USD = currency_usd.currency_rate()
        byn = Decimal(BTC_USD) * Decimal(digits) * Decimal((PERCENT/100)+1)
        if Decimal(byn) <= Decimal(CURRENCY_RATE_FOR_ONE_BITCON):
            byn = CURRENCY_RATE_FOR_ONE_BITCON
    except:
        byn = 'error'
    return byn
