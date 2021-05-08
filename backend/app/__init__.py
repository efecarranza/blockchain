import os
import random
import requests

from flask import Flask, jsonify
from backend.blockchain.blockchain import Blockchain
from backend.pubsub import PubSub

app = Flask(__name__)
blockchain = Blockchain()
ps = PubSub(blockchain)

@app.route('/')
def index():
    return 'Welcome to BeachCoin'

@app.route('/blockchain')
def blockchain_data():
    return jsonify(blockchain.to_json())

@app.route('/blockchain/mine')
def mine_block():
    transaction_data = 'mock_transaction_data'
    blockchain.add_block(transaction_data)
    block = blockchain.chain[-1]
    ps.broadcast_block(block)

    return jsonify(block.to_json())

ROOT_PORT = 5000
PORT = ROOT_PORT

if os.environ.get('PEER') == 'True':
    PORT = random.randint(5001, 6000)

    r = requests.get(f'http://localhost:{ROOT_PORT}/blockchain')
    r_blockchain = Blockchain.from_json(r.json())
    print(r_blockchain)

    try:
        blockchain.replace_chain(r_blockchain.chain)
        print('\n-- Successfully syncrhonized the local chain.')
    except Exception as e:
        print(f'\n-- Error synchronizing: {e}')


app.run(port=PORT)
