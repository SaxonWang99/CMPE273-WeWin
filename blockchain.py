import hashlib
import json
from time import time
from urllib.parse import urlparse
import requests
import datetime


class Blockchain:
    def __init__(self):
        self.product = {'upc':"777777777777",
                        'manufacturer': "Genesis",
                        'item_no':"9"}
        self.owner_history = [{'owner': "WeWin-TV"}]
        self.chain = []
        self.nodes = set()

        # Create the genesis block
        self.new_block(previous_hash='1', proof=100)

    def register_node(self, address):
        """
        Add a new node to the list of nodes
        :param address: Address of node. Eg. 'http://192.168.0.5:5000'
        """

        parsed_url = urlparse(address)
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            # Accepts an URL without scheme like '192.168.0.5:5000'.
            self.nodes.add(parsed_url.path)
        else:
            raise ValueError('Invalid URL')

    def valid_chain(self, chain):
        """
        Determine if a given blockchain is valid
        :param chain: A blockchain
        :return: True if valid, False if not
        """

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            #print(f'{last_block}')
            #print(f'{block}')
            #print("\n-----------\n")
            # Check that the hash of the block is correct
            if block['previous_hash'] != self.hash(last_block):
                return False

            # Check that the Proof of Work is correct
            if not self.valid_proof(last_block['proof'], block['proof'], block['previous_hash']):
                return False

            last_block = block
            current_index += 1

        return True

    def identifyProduct(self, chain, check_product):
        if check_product is None:
            return False
        if len(chain) > 1:
            last_block = chain[1]
        current_index = 1
        result = False
        while current_index < len(chain):
            last_block = chain[current_index]
            if last_block['product'] == check_product:
                    #current_index = len(chain)
                    result = True
                    break
            current_index += 1
        return result

    def valid_trans(self, m_bchain, check_product,current_owner):
        """
        Determine if a given blockchain is valid
        :param chain: A blockchain
        :return: True if valid, False if not
        """
        chainvalided = self.valid_chain(m_bchain.chain)
        if(chainvalided):
            lastIndex = len(m_bchain.chain)-1
            last_block = m_bchain.chain[lastIndex]
            while lastIndex >0:
                #print("whiel")
                if last_block['product'] == check_product:
                        #print(last_block['owner_history'][0]['owner'])
                        #print("leng",last_owner_index)
                        if last_block['owner_history'][-1]['owner'] == current_owner:
                            return last_block
                        else:
                            #print(last_block['owner_history'],"-+-",current_owner)
                            return None
                    #else:
                        #print(last_block['product']['item_no'],"-+-",cur_item_no)
                #print(block)
                lastIndex-= 1
                last_block = m_bchain.chain[lastIndex]
        else:
            return None

    def resolve_conflicts(self):
        """
        This is our consensus algorithm, it resolves conflicts
        by replacing our chain with the longest one in the network.
        :return: True if our chain was replaced, False if not
        """

        neighbours = self.nodes
        new_chain = None

        # We're only looking for chains longer than ours
        max_length = len(self.chain)
        #print("max length",max_length)

        # Grab and verify the chains from all the nodes in our network
        #if neighbours:
            #currentNode = list(neighbours)[0]
        #print("curr", currentNode)
        for node in neighbours:
            #print(currentNode,"---",node)
            #if currentNode != node:
            if node:
                #print("helle",node)
                try:
                    response = requests.get(f'http://{node}/chain')
                    if response.status_code == 200:
                        #print("inhere",node)
                        length = response.json()['length']
                        chain = response.json()['chain']

                        # Check if the length is longer and the chain is valid
                        if length > max_length and self.valid_chain(chain):
                            #print("ttt",node)
                            max_length = length
                            new_chain = chain
                            print("chain will be update with new chain in ",node)
                except requests.exceptions.RequestException as e:  # This is the correct syntax
                    print(e)       
        #print("test here")
        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True

        return False

    def new_block(self, proof, previous_hash):
        """
        Create a new Block in the Blockchain
        :param proof: The proof given by the Proof of Work algorithm
        :param previous_hash: Hash of previous Block
        :return: New Block
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.utcnow()),
            #'timestamp': time(),
            'product': self.product,
            'owner_history': self.owner_history,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the product and owner_history
        self.product = None
        self.owner_history = []

        self.chain.append(block)
        return block

    def new_product(self, upc, manufacturer, item_no):
        """
        Creates a new product to go into the next mined Block
        :param upc: UPC of the product
        :param item_no: Item number of product
        :return: The index of the Block that will hold this transaction
        """
        self.product = { 
            'upc': upc,
            'manufacturer': manufacturer,
            'item_no': item_no
        }

        return self.last_block['index'] + 1

    def new_owner(self, owner_history, owner):
        """
        Creates a new owner to go into the next mined Block
        :param owner: Address of the Sender
        :return: The index of the Block that will hold this transaction
        """
        self.owner_history = owner_history
        self.owner_history.append({
            'owner': owner
        })

        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a Block
        :param block: Block
        """

        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_block):
        """
        Simple Proof of Work Algorithm:
         - Find a number p' such that hash(pp') contains leading 4 zeroes
         - Where p is the previous proof, and p' is the new proof
         
        :param last_block: <dict> last Block
        :return: <int>
        """

        last_proof = last_block['proof']
        last_hash = self.hash(last_block)

        proof = 0
        while self.valid_proof(last_proof, proof, last_hash) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof, last_hash):
        """
        Validates the Proof
        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :param last_hash: <str> The hash of the Previous Block
        :return: <bool> True if correct, False if not.
        """

        guess = f'{last_proof}{proof}{last_hash}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"