from backend.wallet.wallet import Wallet
from backend.blockchain.blockchain import Blockchain
from backend.wallet.transaction import Transaction
from backend.config import STARTING_BALANCE

def test_verify_valid_signature():
    data = { 'test': 'test_data' }
    wallet = Wallet()
    signature = wallet.sign(data)

    assert Wallet.verify(wallet.public_key, data, signature) == True

def test_verify_invalid_signature():
    data = { 'test': 'test_data' }
    wallet = Wallet()
    signature = wallet.sign(data)

    assert Wallet.verify(Wallet().public_key, data, signature) == False

def test_calculate_balance_starting_balance():
    blockchain = Blockchain()
    wallet = Wallet()

    assert Wallet.calculate_balance(blockchain, wallet.address) == STARTING_BALANCE

    amount = 50
    tr = Transaction(wallet, 'recipient', amount)

    blockchain.add_block([tr.to_json()])

    assert Wallet.calculate_balance(blockchain, wallet.address) == STARTING_BALANCE - amount

    received_amount = 25
    tr2 = Transaction(Wallet(), wallet.address, received_amount)

    blockchain.add_block([tr2.to_json()])

    assert Wallet.calculate_balance(blockchain, wallet.address) == STARTING_BALANCE - amount + received_amount
