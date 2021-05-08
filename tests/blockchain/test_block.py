import pytest
import time

from backend.blockchain.block import Block, GENESIS_DATA
from backend.config import MINE_RATE, SECONDS
from backend.utils.hex_to_binary import hex_to_binary

def test_mine_block():
    last_block = Block.genesis()
    data = 'test-data'
    block = Block.mine_block(last_block, data)
    assert isinstance(block, Block)
    assert block.data == data
    assert block.last_hash == last_block.hash
    assert hex_to_binary(block.hash)[0:block.difficulty] == '0' * block.difficulty

def test_genesis():
    genesis = Block.genesis()
    assert isinstance(genesis, Block)
    for k,v in GENESIS_DATA.items():
        assert getattr(genesis, k) == v

def test_quickly_mine_block():
    last_block = Block.mine_block(Block.genesis(), 'anything')
    mined_block = Block.mine_block(last_block, 'new_one')

    assert mined_block.difficulty == last_block.difficulty + 1

def test_slowly_mined_block():
    last_block = Block.mine_block(Block.genesis(), 'anything')
    time.sleep(MINE_RATE / SECONDS)
    mined_block = Block.mine_block(last_block, 'new_one')

    assert mined_block.difficulty == last_block.difficulty - 1

def test_mined_block_difficulty_limits_at_one():
    last_block = Block(time.time_ns(), 'last_hash', 'hash', 'data', 1, 0)
    time.sleep(MINE_RATE / SECONDS)
    mined_block = Block.mine_block(last_block, 'second_data')

    assert mined_block.difficulty == 1

@pytest.fixture
def last_block():
    return Block.genesis()

@pytest.fixture
def block(last_block):
    return Block.mine_block(last_block, 'test_data')

def test_is_valid_block(last_block, block):
    Block.is_valid_block(last_block, block)

def test_is_valid_block_invalid_hash(last_block, block):
    block.last_hash = 'evil_last_hash'

    with pytest.raises(Exception, match='The block last_hash must be correct.'):
        Block.is_valid_block(last_block, block)

def test_is_valid_block_bad_proof_of_work(last_block, block):
    block.hash = 'fff'
    with pytest.raises(Exception, match='Proof of Work requirement was not met.'):
        Block.is_valid_block(last_block, block)

def test_is_valid_block_bad_difficulty(last_block, block):
    block.difficulty = 10
    block.hash = f'{"0" * block.difficulty}111abc'
    with pytest.raises(Exception, match='Difficulty must only adjust by one.'):
        Block.is_valid_block(last_block, block)

def test_is_valid_block_bad_block_hash(last_block, block):
    block.hash = '00000000000000000aabbcc'
    with pytest.raises(Exception, match='The block hash does not match expected hash.'):
        Block.is_valid_block(last_block, block)

