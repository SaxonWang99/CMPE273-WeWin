from uuid import uuid4

import requests
from flask import Flask, jsonify, request

from blockchain import Blockchain


# Instantiate the Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


@app.route('/register', methods=['POST'])
def register_product():
    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block)

    values = request.get_json()

    required = ['upc', 'owner']
    if not all(k in values for k in required):
        return 'Missing values', 400

    blockchain.new_product(upc=values['upc'])
    blockchain.new_owner(owner=values['owner'])

    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'product': block['product'],
        'owner_history': block['owner_history'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 201


@app.route('/transaction', methods=['POST'])
def transaction():
    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block)

    values = request.get_json()

    required = ['upc', 'owner']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # TODO: append owner to owner_history in product's previous block

    return None


@app.route('/validation', methods=['GET'])
def validate():

    #TODO: validation

    return None


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port)