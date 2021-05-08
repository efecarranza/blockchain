import os
import random

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

PORT = 5000

if os.environ.get('PEER') == 'True':
    PORT = random.randint(5001, 6000)

app.run(port=PORT)
