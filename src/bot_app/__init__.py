import logging
from .app import dp
from . import commands, usd, byn, btc, settings_admin

logging.basicConfig(level=logging.INFO)