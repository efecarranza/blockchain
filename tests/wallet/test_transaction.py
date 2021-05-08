import pytest

from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet

def test_transaction():
    sender_wallet = Wallet()
    recipient = 'recipient'
    amount = 50
    transaction = Transaction(sender_wallet, recipient, amount)

    assert transaction.output[recipient] == amount
    assert transaction.output[sender_wallet.address] == sender_wallet.balance - amount
    assert 'timestamp' in transaction.input
    assert transaction.input['amount'] == sender_wallet.balance
    assert transaction.input['address'] == sender_wallet.address
    assert transaction.input['public_key'] == sender_wallet.public_key
    assert Wallet.verify(transaction.input['public_key'], transaction.output, transaction.input['signature'])

def test_transaction_exceeds_balance():
    with pytest.raises(Exception, match='Amount exceeds balance.'):
        Transaction(Wallet(), 'recipient', 100000)

def test_update_transaction_exceeds_balance():
    wallet = Wallet()
    transaction = Transaction(wallet, 'recipient', 100)

    with pytest.raises(Exception, match='Amount exceeds balance.'):
        transaction.update(wallet, 'new_recipient', 1000000)

def test_update_transaction_successful():
    wallet = Wallet()
    recipient = 'recipient'
    amount = 100
    transaction = Transaction(wallet, recipient, amount)

    next_recipient = 'next_recipient'
    next_amount = 200

    transaction.update(wallet, next_recipient, next_amount)

    assert transaction.output[next_recipient] == next_amount
    assert transaction.output[wallet.address] == wallet.balance - amount - next_amount
    assert Wallet.verify(transaction.input['public_key'], transaction.output, transaction.input['signature'])

    to_first_again = 25
    transaction.update(wallet, recipient, to_first_again)

    assert transaction.output[recipient] == amount + to_first_again
    assert transaction.output[wallet.address] == wallet.balance - amount - next_amount - to_first_again
    assert Wallet.verify(transaction.input['public_key'], transaction.output, transaction.input['signature'])

def test_is_valid_transaction():
    Transaction.is_valid_transaction(Transaction(Wallet(), 'recipient', 50))

def test_is_valid_transaction_invalid_output():
    wallet = Wallet()
    transaction = Transaction(Wallet(), 'recipient', 50)
    transaction.output[wallet.address] = 1000
    with pytest.raises(Exception, match='Invalid transaction: output values.'):
        Transaction.is_valid_transaction(transaction)

def test_is_valid_transaction_invalid_signature():
    transaction = Transaction(Wallet(), 'recipient', 50)
    transaction.input['signature'] = Wallet().sign(transaction.output)

    with pytest.raises(Exception, match='Invalid signature.'):
        Transaction.is_valid_transaction(transaction)
