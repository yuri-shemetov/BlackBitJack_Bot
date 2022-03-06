import requests
from django import template
from . import currency_usd
from decimal import *
from . import open_settings

register = template.Library()

def currency_rate():
    try:
        digits = open_settings.byn()
        BTC_USD = currency_usd.currency_rate()
        byn = Decimal(BTC_USD) * Decimal(digits) * Decimal((open_settings.percent()/100)+1)
        if Decimal(byn) <= Decimal(open_settings.rate_for_one_bit()):
            byn = open_settings.rate_for_one_bit()
    except:
        byn = 'error'
    return byn
