from uuid import uuid4
from flask_cors import CORS
import requests
from flask import Flask, jsonify, request
import json
import datetime
from blockchain import Blockchain


# Instantiate the Node
app = Flask(__name__)
CORS(app)
# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()
typeUser = 1
userName = "A"

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


# /register - register new product
# {
#     param: upc
#     param: manufacturer
#     param: item_no
#     param: new_owner
# }
@app.route('/register', methods=['POST'])
def register_product():
    #print("helloooo",typeUser)
    if typeUser ==1:
        last_block = blockchain.last_block
        proof = blockchain.proof_of_work(last_block)

        values = request.get_json()
        required = ['upc', 'item_no', 'new_owner']
        if not all(k in values for k in required):
            return 'Missing values', 400
        #catch info into product
        c_product ={'upc': values['upc'],
                    'manufacturer': node_identifier,
                    'item_no': values['item_no']}
        #TODO: call validate
        exist_block = blockchain.identifyProduct(blockchain.chain ,c_product)
        if exist_block == False:
            blockchain.new_product(upc=values['upc'], manufacturer= node_identifier, item_no=values['item_no'])
            blockchain.new_owner(owner_history=[], owner=values['new_owner'])

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
        else:
            return jsonify({"message": "this Item can not mine twince",
                    "upc": values['upc'],
                    "item_no": values['item_no']}), 400
    else: 
            if typeUser == 2:
                return jsonify({"message": "you are not authorized to make new product",
                                "UserName": userName,
                                "UserID":node_identifier,
                                "UserType": "Agency"}), 400
            else:
                return jsonify({"message": "Unknown User type, you are not authorized to make new product",
                                "UserName": userName,
                                "UserID":node_identifier,
                                "UserType": typeUser}), 400


# /transaction - create new transaction
# {
#     param: upc
#     param: manufacturer
#     param: item_no
#     param: current_owner
#     param: new_owner
# }
@app.route('/transaction', methods=['POST'])
def transaction():
    #update the list
    replaced = blockchain.resolve_conflicts()
    if replaced:
        print("BlockChain updated")
    #do transation
    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block)

    # validate request parameters
    values = request.get_json()
    required = ['upc', 'manufacturer', 'item_no', 'current_owner', 'new_owner']
    if not all(k in values for k in required):
        return 'Missing values', 400
    if values['current_owner']==values['new_owner']:
        return 'You own this product, no need to do transfer', 400
    check_product ={'upc':values['upc'],
                    'manufacturer': values['manufacturer'],
                    'item_no':values['item_no']}
    # call validate
    verified_block =  blockchain.valid_trans(blockchain,check_product,values['current_owner'])
    if verified_block:
        #print("right here",verified_block["owner_history"])
        blockchain.new_product(upc=values['upc'], manufacturer=values['manufacturer'], item_no=values['item_no'])
        blockchain.new_owner(owner_history = list(verified_block["owner_history"]),owner=values['new_owner'])
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
    else:
        response = {'message': f'Transaction cannot be added to chain invalide verify'}

    return jsonify(response), 201

# {
#     param: upc
#     param: item_no
#     param: current_owner
# }
@app.route('/validate/<string:cur_upc>,<string:manufacturer>,<int:cur_item_no>,<string:cur_owner>', methods=['GET'])
def validate(cur_upc,manufacturer,cur_item_no,cur_owner):
    #TODO: validation; iterate through blockchain; verify by upc, item_no, current_owner for most recent
    check_product ={'upc':cur_upc,
                    'manufacturer': manufacturer,
                    'item_no':cur_item_no}
    result = blockchain.valid_trans(blockchain,check_product,cur_owner)
    if result:
        response = {
            'message': 'validated successfully',
            'chain': result,
            'length': len(blockchain.chain),
        }
        return jsonify(response), 200
    else:
        response = {
            'message': 'invalid',
        }
        return jsonify(response), 400
    

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes: 
        if str(userName) in node:
            print("Adding yourself is skipped node Address: 127.0.0.1:",userName)
        else:
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
    parser.add_argument('-t', '--type', default=1, type=int, help='type of user')
    args = parser.parse_args()
    port = args.port
    typeUser = args.type
    userName = port

    app.run(host='127.0.0.1', port=port)
   