import os
import time

from backend.blockchain.block import Block
from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback

pnconfig = PNConfiguration()
pnconfig.subscribe_key = os.environ.get('PUBSUB_SUBSCRIBE_KEY')
pnconfig.publish_key = os.environ.get('PUBSUB_PUBLISH_KEY')

CHANNELS = {
    'TEST': 'TEST',
    'BLOCK': 'BLOCK',
}

class Listener(SubscribeCallback):
    def __init__(self, blockchain):
        self.blockchain = blockchain

    def message(self, pubnub, message_object):
        print(f'\n-- Channel: {message_object.channel}')
        print(f'\n-- Incoming Message -- {message_object.message}')

        if message_object.channel == CHANNELS['BLOCK']:
            block = Block.from_json(message_object.message)
            potential_chain = self.blockchain.chain[:]
            potential_chain.append(block)
            try:
                self.blockchain.replace_chain(potential_chain)
                print(f'\n-- Successfully replace the chain.')
            except Exception as e:
                print(f'\n-- Did not replace chain: {e}')

class PubSub():
    """
    Handles the publish/subscribe layer of the application.
    Provides communication between the nodes of the blockchain network.
    """
    def __init__(self, blockchain):
        self.pubnub = PubNub(pnconfig)
        self.pubnub.subscribe().channels(CHANNELS.values()).execute()
        self.pubnub.add_listener(Listener(blockchain))

    def publish(self, channel, message):
        """
        Publish the message object to the channel.
        """
        self.pubnub.publish().channel(channel).message(message).sync()

    def broadcast_block(self, block):
        """
        Broadcast a block object to all nodes.
        """
        self.publish(CHANNELS['BLOCK'], block.to_json())

def main():
    ps = PubSub()
    time.sleep(1)
    ps.publish(CHANNELS['TEST'], {'hey': 'testing!'})

if __name__ == '__main__':
    main()
