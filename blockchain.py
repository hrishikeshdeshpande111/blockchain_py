import hashlib
import json
import time
import requests
from datetime import datetime


class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps({"index": self.index, "timestamp": self.timestamp, "data": self.data, "previous_hash": self.previous_hash}, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def validate_previous_hash(self, previous_block):
        return self.previous_hash == previous_block.hash
    
    def __str__(self):
        return f"Block {self.index} ({self.timestamp}): {self.data}"
    
    
    
class CustomEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        if isinstance(o, Block):
            return {
                "index": o.index,
                "timestamp": o.timestamp,
                "data": o.data,
                "previous_hash": o.previous_hash,
                "hash": o.hash
            }
        return super().default(o)



class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.current_transactions = []

    def create_genesis_block(self):
        return Block(0, time.time(), "Genesis Block", "0")

    def new_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

    def add_transaction(self, sender, recipient, amount):
        # Create a new transaction object and append it to the list of pending transactions
        self.pending_transactions.append(self.new_transaction(self, sender, recipient, amount))

        # Print a message to the console to indicate that the transaction has been added
        print(f"Transaction added: {sender} sent {amount} coins to {recipient}")

    def proof_of_work(self, last_block):
        # Find a proof that, when hashed with the previous block's hash, produces a hash that starts with 4 zeros.
        proof = 0
        while self.valid_proof(last_block, proof) is False:
            proof += 1
        return proof

    def valid_proof(self, last_block, proof):
        guess = f'{last_block.hash}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def new_block(self, proof):
        previous_block = self.last_block
        index = previous_block.index + 1
        timestamp = time.time()
        data = self.current_transactions
        previous_hash = previous_block.hash
        block = Block(index, timestamp, data, previous_hash)
        self.chain.append(block)
        self.current_transactions = []
        return block

    @property
    def last_block(self):
        return self.chain[-1]

    def consensus(self):
        # Implement a simple consensus algorithm: replace the chain with the longest valid chain of other nodes.
        other_chains = []
        for node in self.nodes:
            if node != self.node_url:
                response = requests.get(f'{node}/chain')
                if response.status_code == 200:
                    chain_length = response.json()['length']
                    chain = response.json()['chain']
                    other_chains.append(chain)
        if not other_chains:
            return False

        longest_chain = max(other_chains, key=len)

        if len(longest_chain) > len(self.chain) and self.valid_chain(longest_chain):
            self.chain = longest_chain
            return True
        else:
            return False

    def valid_chain(self, chain):
        # Check if a given blockchain is valid
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            if not block.validate_previous_hash(last_block):
                return False
            if not self.valid_proof(last_block, block.proof):
                return False
            last_block = block
            current_index += 1

        return True
    
    def __str__(self):
        blocks = [str(block) for block in self.chain]
        return "\n".join(blocks)
    
# blockchain = Blockchain()

# # Add some transactions
# blockchain.new_transaction(sender='Hrishikesh', recipient='Ninad', amount=1)
# blockchain.new_transaction(sender='Prasanna', recipient='Hrishikesh', amount=123)

# # Mine a block
# last_block = blockchain.last_block
# proof = blockchain.proof_of_work(last_block)
# blockchain.new_block(proof)

# # Print the blockchain
# print(blockchain)
