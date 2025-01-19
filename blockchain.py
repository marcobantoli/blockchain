import hashlib
import time


class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()
        self.nonce = 0

    def calculate_hash(self):
        # Generate hash for this block using its content
        block_content = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}"
        return hashlib.sha256(block_content.encode()).hexdigest()

    def mine_block(self, difficulty):
        # Perform proof of work to find a hash with leading zeros
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"Block mined: {self.hash}")


class Blockchain:
    def __init__(self):
        # Initialize block with the genesis block
        self.chain = [self.create_genesis_block()]
        self.difficulty = 4

    def create_genesis_block(self):
        # Create the first block of the blockchain
        return Block(0, time.time(), "Genesis Block", "0")

    def get_latest_block(self):
        # Get the last block in the blockchain
        return self.chain[-1]

    def add_block(self, data):
        # Add a new block to the blockchain
        latest_block = self.get_latest_block()
        new_block = Block(
            index=latest_block.index + 1,
            timestamp=time.time(),
            data=data,
            previous_hash=latest_block.hash,
        )
        # Mine the block first before adding it
        new_block.mine_block(self.difficulty)

        self.chain.append(new_block)

    def is_chain_valid(self):
        # Iterate through the chain
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # First verify current block's hash
            if current_block.hash != current_block.calculate_hash:
                print(f"Block {current_block.index} has been tampered!")
                return False

            # Second verify the link between current and previous blocks
            if current_block.previous_hash != previous_block.hash:
                print(
                    f"Block {current_block.index} is not linked to the previous block!"
                )
                return False

        print("Blockchain is valid.")
        return True


my_blockchain = Blockchain()

my_blockchain.add_block("First block after genesis")
my_blockchain.add_block("Second block after genesis")

# Print the chain
for block in my_blockchain.chain:
    print(
        f"Index: {block.index}, Data: {block.data}, Hash: {block.hash}, Nonce: {block.nonce}"
    )

print(my_blockchain.is_chain_valid())
