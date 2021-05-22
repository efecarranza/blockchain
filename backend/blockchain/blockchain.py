from backend.blockchain.block import Block
from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet
from backend.config import MINING_REWARD_INPUT

class Blockchain:
    """
    The blockchain is a public ledger of transactions.
    Implemented as a list of blocks - data sets of transactions.
    """
    def __init__(self):
        self.chain = [Block.genesis()]

    def add_block(self, data):
        self.chain.append(Block.mine_block(self.chain[-1], data))

    def __repr__(self):
        return f'Blockchain: {self.chain}'

    def replace_chain(self, chain):
        """
        Replace the local chain with the incoming one if the following rules apply:
        - The incoming chain must be longer than the local one
        - The incoming chain is formatted properly
        """

        if len(chain) <= len(self.chain):
            raise Exception('Cannot replace: Incoming chain is shorter than existing chain.')

        try:
            Blockchain.is_valid_chain(chain)
        except Exception as e:
            raise Exception(f'Cannot replace: Incoming chain is invalid - {e}')

        self.chain = chain

    def to_json(self):
        """
        Serialize the blockchain into a list of blocks.
        """
        return [b.to_json() for b in self.chain]

    @staticmethod
    def from_json(chain_json):
        """
        Deserialize the blockchain data from JSON.
        """
        blockchain = Blockchain()
        blockchain.chain = [Block.from_json(b) for b in chain_json]
        return blockchain

    @staticmethod
    def is_valid_chain(chain):
        """
        Validate incoming chain
        - The chain must start with the genesis block
        - Blocks must be formatted correctly
        """
        if chain[0] != Block.genesis():
            raise Exception('The genesis block is invalid.')

        for i in range(1, len(chain)):
            Block.is_valid_block(chain[i-1], chain[i])

        Blockchain.is_valid_transaction_chain(chain)

    @staticmethod
    def is_valid_transaction_chain(chain):
        """
        Enforce the rules of a chain composed of blocks of transactions.
            - Each transaction must only appear once in the chain.
            - There can only be one mining reward per block.
            - Each transaction must be valid.
        """
        transaction_ids = set()
        for i in range(len(chain)):
            block = chain[i]
            has_mining_reward = False
            for tr in block.data:
                transaction = Transaction.from_json(tr)

                if transaction.id in transaction_ids:
                    raise Exception(f'Duplicate transaction in block. TransactionId: {transaction.id}')
                transaction_ids.add(transaction.id)

                if transaction.input == MINING_REWARD_INPUT:
                    if has_mining_reward:
                        raise Exception(f'Multiple mining rewards founds in block. Check block with hash: {block.hash}')
                    has_mining_reward = True
                else:
                    historic_blockchain = Blockchain()
                    historic_blockchain.chain = chain[0:i]
                    historic_balance = Wallet.calculate_balance(historic_blockchain, transaction.input['address'])

                    if historic_balance != transaction.input['amount']:
                        raise Exception(f'TransactionId: {transaction.id} has invalid input amount.')

                Transaction.is_valid_transaction(transaction)
