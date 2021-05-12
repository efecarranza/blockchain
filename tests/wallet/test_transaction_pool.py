from backend.wallet.transaction_pool import TransactionPool
from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet
from backend.blockchain.blockchain import Blockchain

def test_set_transaction():
    tp = TransactionPool()
    transaction = Transaction(Wallet(), 'recipient', 100)
    tp.set_transaction(transaction)

    assert tp.transaction_map[transaction.id] == transaction

def test_clear_transactions():
    tp = TransactionPool()

    tr = Transaction(Wallet(), 'recipient', 1)
    tp.set_transaction(tr)

    tr2 = Transaction(Wallet(), 'recipient', 2)
    tp.set_transaction(tr2)

    blockchain = Blockchain()
    blockchain.add_block([tr.to_json(), tr2.to_json()])

    assert tr.id in tp.transaction_map
    assert tr2.id in tp.transaction_map

    tp.clear_transactions(blockchain)

    assert tr.id not in tp.transaction_map
    assert tr2.id not in tp.transaction_map
