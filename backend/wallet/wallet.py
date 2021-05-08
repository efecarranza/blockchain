import uuid

from backend.config import STARTING_BALANCE

class Wallet:
    """
    An individual wallet for a miner in the system.
    Keeps track of the miner's balance.
    Allows the miner to authorize transactions.
    """
    def __init__(self):
        self.address = str(uuid.uuid4())
        self.balance = STARTING_BALANCE
