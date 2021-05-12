from backend.wallet.transaction_pool import TransactionPool
from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet

def test_set_transaction():
    tp = TransactionPool()
    transaction = Transaction(Wallet(), 'recipient', 100)
    tp.set_transaction(transaction)

    assert tp.transaction_map[transaction.id] == transaction
