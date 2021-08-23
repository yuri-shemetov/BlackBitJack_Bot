import logging
from .app import dp
from . import commands, usd, byn, btc

logging.basicConfig(level=logging.INFO)