import json
import uuid

from backend.config import STARTING_BALANCE
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature

class Wallet:
    """
    An individual wallet for a miner in the system.
    Keeps track of the miner's balance.
    Allows the miner to authorize transactions.
    """
    def __init__(self):
        self.address = str(uuid.uuid4())
        self.balance = STARTING_BALANCE
        self.private_key = ec.generate_private_key(ec.SECP256K1(), default_backend())
        self.public_key = self.private_key.public_key()
        self.serialize_public_key()

    def sign(self, data):
        """
        Generates a signature based on the data using the local private key.
        """
        return self.private_key.sign(json.dumps(data).encode('utf-8'), ec.ECDSA(hashes.SHA256()))

    def serialize_public_key(self):
        """
        Reset the public key to its serialized version.
        """
        pub_key_bytes = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        self.public_key = pub_key_bytes.decode('utf-8')


    @staticmethod
    def verify(public_key, data, signature):
        """
        Verify a signature based on the original public key and data.
        """
        deseralized_pub_key = serialization.load_pem_public_key(
            public_key.encode('utf-8'),
            default_backend()
        )
        try:
            deseralized_pub_key.verify(signature, json.dumps(data).encode('utf-8'), ec.ECDSA(hashes.SHA256()))
            return True
        except InvalidSignature:
            return False
