from bit import PrivateKey as Key
from . my_local_settings import private_key


def execute_transaction(dest_address, translation):
    source_k = Key(private_key)
    source_k.send([(dest_address, translation, 'btc')])

def get_balance_bitcoins():
    source_k = Key(private_key)
    return source_k.get_balance('btc')
