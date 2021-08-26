from bit import PrivateKey as Key
from . my_local_settings import private_key
import requests                   # new
from django import template       # new

register = template.Library()     # new 

def execute_transaction(dest_address, translation):
    
    fees = "https://api.blockchain.info/mempool/fees"  # new
    response = requests.get(fees)                      # new
    try:                                               # new
        response.raise_for_status()                    # new
        res = requests.get(fees)                       # new
        fee = int(res.json().get('priority'))          # new
    except:                                            # new
        fee = ''                                       # new

    source_k = Key(private_key)
    source_k.create_transaction([(dest_address, translation, 'btc')], fee=fee) # new
    source_k.send([(dest_address, translation, 'btc')], fee=fee)

def get_balance_bitcoins():
    source_k = Key(private_key)
    return source_k.get_balance('btc')
