import os
import random
import requests

from flask import Flask, jsonify, request
from backend.blockchain.blockchain import Blockchain
from backend.pubsub import PubSub
from backend.wallet.transaction import Transaction
from backend.wallet.transaction_pool import TransactionPool
from backend.wallet.wallet import Wallet

app = Flask(__name__)
blockchain = Blockchain()
wallet = Wallet(blockchain)
tp = TransactionPool()
ps = PubSub(blockchain, tp)

@app.route('/')
def index():
    return 'Welcome to BeachCoin'

@app.route('/blockchain')
def blockchain_data():
    return jsonify(blockchain.to_json())

@app.route('/blockchain/mine')
def mine_block():
    transaction_data = tp.transaction_data()
    transaction_data.append(Transaction.reward_transaction(wallet).to_json())
    blockchain.add_block(transaction_data)
    block = blockchain.chain[-1]
    ps.broadcast_block(block)
    tp.clear_transactions(blockchain)


    return jsonify(block.to_json())

@app.route('/wallet/transact', methods=['POST'])
def transact():
    data = request.get_json()
    transaction = tp.existing_transaction(wallet.address)

    if transaction:
        transaction.update(wallet, data['recipient'], data['amount'])
    else:
        transaction = Transaction(wallet, data['recipient'], data['amount'])

    ps.broadcast_transaction(transaction)

    return jsonify(transaction.to_json())

@app.route('/wallet/info')
def wallet_info():
    return jsonify({'address': wallet.address, 'balance': wallet.balance})

ROOT_PORT = 5000
PORT = ROOT_PORT

if os.environ.get('PEER') == 'True':
    PORT = random.randint(5001, 6000)

    r = requests.get(f'http://localhost:{ROOT_PORT}/blockchain')
    r_blockchain = Blockchain.from_json(r.json())

    try:
        blockchain.replace_chain(r_blockchain.chain)
        print('\n-- Successfully syncrhonized the local chain.')
    except Exception as e:
        print(f'\n-- Error synchronizing: {e}')


app.run(port=PORT)
