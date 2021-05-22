import pytest

from backend.blockchain.blockchain import Blockchain
from backend.blockchain.block import GENESIS_DATA
from backend.wallet.wallet import Wallet
from backend.wallet.transaction import Transaction

def test_blockchain_instance():
    blockchain = Blockchain()
    assert blockchain.chain[0].hash == GENESIS_DATA['hash']

def test_add_block():
    blockchain = Blockchain()
    data = 'test-data'
    blockchain.add_block(data)
    assert blockchain.chain[-1].data == data

@pytest.fixture
def blockchain_three_blocks():
    blockchain = Blockchain()
    for i in range(3):
        blockchain.add_block([Transaction(Wallet(), 'recipient', i).to_json()])
    return blockchain

def test_is_valid_chain(blockchain_three_blocks):
    Blockchain.is_valid_chain(blockchain_three_blocks.chain)

def test_is_valid_chain_bad_genesis_block(blockchain_three_blocks):
    blockchain_three_blocks.chain[0].hash = 'bad_hash'
    with pytest.raises(Exception, match='The genesis block is invalid.'):
        Blockchain.is_valid_chain(blockchain_three_blocks.chain)

def test_replace_chain(blockchain_three_blocks):
    blockchain = Blockchain()
    blockchain.replace_chain(blockchain_three_blocks.chain)
    assert blockchain.chain == blockchain_three_blocks.chain

def test_replace_chain_new_chain_not_longer(blockchain_three_blocks):
    blockchain = Blockchain()
    with pytest.raises(Exception, match='Cannot replace: Incoming chain is shorter than existing chain.'):
        blockchain_three_blocks.replace_chain(blockchain.chain)

def test_replace_chain_bad_chain(blockchain_three_blocks):
    blockchain = Blockchain()
    blockchain_three_blocks.chain[1].hash = 'bad_hash'
    with pytest.raises(Exception, match='Cannot replace: Incoming chain is invalid'):
        blockchain.replace_chain(blockchain_three_blocks.chain)

def test_is_valid_transaction_chain(blockchain_three_blocks):
    Blockchain.is_valid_transaction_chain(blockchain_three_blocks.chain)

def test_is_valid_transaction_chain_duplicate_values(blockchain_three_blocks):
    tr = Transaction(Wallet(), 'recipient', 1).to_json()
    blockchain_three_blocks.add_block([tr, tr])
    with pytest.raises(Exception, match='Duplicate transaction in block. TransactionId:'):
        Blockchain.is_valid_transaction_chain(blockchain_three_blocks.chain)

def test_is_valid_transaction_chain_multiple_rewards(blockchain_three_blocks):
    reward = Transaction.reward_transaction(Wallet()).to_json()
    reward2 = Transaction.reward_transaction(Wallet()).to_json()

    blockchain_three_blocks.add_block([reward, reward2])
    with pytest.raises(Exception, match='Multiple mining rewards founds in block. Check block with hash:'):
        Blockchain.is_valid_transaction_chain(blockchain_three_blocks.chain)

def test_is_valid_transaction_chain_bad_transaction(blockchain_three_blocks):
    tr = Transaction(Wallet(), 'recipient', 1)
    tr.input['signature'] = Wallet().sign(tr.output)

    blockchain_three_blocks.add_block([tr.to_json()])
    with pytest.raises(Exception, match='Invalid signature'):
        Blockchain.is_valid_transaction_chain(blockchain_three_blocks.chain)

def test_is_valid_transaction_chain_bad_historic_balance(blockchain_three_blocks):
    wallet = Wallet()
    bad_tr = Transaction(wallet, 'recipient', 1)
    bad_tr.input[wallet.address] = 9000
    bad_tr.input['amount'] = 90001
    bad_tr.input['signature'] = wallet.sign(bad_tr.output)

    blockchain_three_blocks.add_block([bad_tr.to_json()])
    with pytest.raises(Exception, match='has invalid input amount'):
        Blockchain.is_valid_transaction_chain(blockchain_three_blocks.chain)
