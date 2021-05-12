import requests
import time

from backend.wallet.wallet import Wallet

BASE_URL = 'http://localhost:5000'
def get_blockchain():
    return requests.get(BASE_URL + '/blockchain').json()

def get_blockchain_mine():
    return requests.get(BASE_URL + '/blockchain/mine').json()

def post_wallet_transact(recipient, amount):
    data = {
        'recipient': recipient,
        'amount': amount
    }
    return requests.post(BASE_URL + '/wallet/transact', json=data).json()

start_blockchain = get_blockchain()
print(f'start_blockchain: {start_blockchain}')


recipient = Wallet().address

first_tr = post_wallet_transact(recipient, 100)
print(f'\n first_tr: {first_tr}')

second_tr = post_wallet_transact(recipient, 23)
print(f'\n second_tr: {second_tr}')

time.sleep(2)
mined_block = get_blockchain_mine()
print(f'\n mined_block: {mined_block}')
