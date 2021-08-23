
# Адрес кошелька пользователя
def check_wallet(wallet):
    url_for_view = f'https://www.blockchain.com/ru/btc/address/{wallet}'
    text = url_for_view + '\n'
    return text