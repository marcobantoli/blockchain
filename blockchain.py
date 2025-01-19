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
        self.pending_transactions = []
        self.difficulty = 4

    def create_genesis_block(self):
        # Create the first block of the blockchain
        return Block(0, time.time(), "Genesis Block", "0")

    def get_latest_block(self):
        # Get the last block in the blockchain
        return self.chain[-1]

    def add_transaction(self, transaction):
        # Add transaction to the pool of pending transactions
        self.pending_transactions.append(transaction)

    def is_chain_valid(self):
        # Go through each block in the blockchain
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Verify current block's hash
            if current_block.hash != current_block.calculate_hash():
                print(f"Block {current_block.index} has been tampered!")
                return False

            # Verify if the current block links properly to the previous block
            if current_block.previous_hash != previous_block.hash:
                print(
                    f"Block {current_block.index} is not linked to the previous block!"
                )
                return False

        print("Blockchain is valid.")
        return True

    def mine_pending_transactions(self, miner_address):
        # Include a reward transaction for the miner
        reward_transaction = Transaction("System", miner_address, 50)
        self.pending_transactions.append(reward_transaction)

        # Create a new block with pending transactions
        new_block = Block(
            index=self.get_latest_block().index + 1,
            timestamp=time.time(),
            data=[
                str(tx) for tx in self.pending_transactions
            ],  # Store transactions as strings
            previous_hash=self.get_latest_block().hash,
        )
        new_block.mine_block(self.difficulty)

        # Add the mined block to the chain
        self.chain.append(new_block)

        # Clear the pending transactions
        self.pending_transactions = []


class Transaction:
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount

    def __str__(self):
        return f"Transaction({self.sender} -> {self.recipient}: {self.amount})"


my_blockchain = Blockchain()

my_blockchain.add_transaction(Transaction("Alice", "Bob", 10))
my_blockchain.add_transaction(Transaction("Bob", "Charlie", 20))

print("Mining transactions...")
my_blockchain.mine_pending_transactions("Miner1")

my_blockchain.add_transaction(Transaction("Charlie", "Alice", 5))
my_blockchain.add_transaction(Transaction("Alice", "Bob", 15))

print("Mining transactions...")
my_blockchain.mine_pending_transactions("Miner1")

# Print the blockchain
for block in my_blockchain.chain:
    print(f"Block {block.index}:")
    print(f"Hash: {block.hash}")
    print(f"Previous Hash: {block.previous_hash}")
    print(f"Data: {block.data}")
