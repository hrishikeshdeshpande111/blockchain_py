**Overview** :
This is a Python program that implements a basic blockchain using proof-of-work and a consensus algorithm.

**Dependencies** :
This program requires the following dependencies:

Python 3
hashlib
json
time
requests

**Usage** :
To use this program, simply run the Python script blockchain.py using Python 3. The program will create a new blockchain and add some transactions. It will then mine a new block and print the entire blockchain.

**Classes** :
This program contains the following classes:

**Block** :
This class represents a block in the blockchain. Each block contains an index, a timestamp, some data, a hash of the previous block, and its own hash.

**CustomEncoder** :
This class is a custom JSON encoder that can encode datetime objects and Block objects.

**Blockchain** :
This class represents the entire blockchain. It contains a list of blocks and a list of pending transactions. It also contains methods for adding new transactions, mining new blocks, and implementing a consensus algorithm.
