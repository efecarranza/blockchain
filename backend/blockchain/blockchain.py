from backend.blockchain.block import Block

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
