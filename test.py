
import requests
import json

print("register node 5001 to 5001")
node_list = {   
    "nodes" : ["http://127.0.0.1:5001"]
}
r = requests.post('http://127.0.0.1:5001/nodes/register',json = node_list)
print(r.text)

print("----------------------------")

print("print chain")
r = requests.get('http://127.0.0.1:5001/chain')
print(r.text)

print("----------------------------")

print("register new product1")
new_product = {
    "upc": 1,
    "manufacturer": 10,
    "item_no": 100,
    "new_owner": "Fred"
}
r = requests.post('http://127.0.0.1:5001/register',json = new_product)
print(r.text)

print("----------------------------")

print("print chain")
r = requests.get('http://127.0.0.1:5001/chain')
print(r.text)

print("----------------------------")

print("register new product2")
new_product = {
    "upc": 2,
    "manufacturer": 10,
    "item_no": 100,
    "new_owner": "Fred"
}
r = requests.post('http://127.0.0.1:5001/register',json = new_product)
print(r.text)

print("----------------------------")

print("print chain")
r = requests.get('http://127.0.0.1:5001/chain')
print(r.text)

print("----------------------------")

print("create transaction1")
new_transaction = {
    "upc": 1,
    "manufacturer": 10,
    "item_no": 100,
    "current_owner": "Fred",
    "new_owner": "Matt"
}
r = requests.post('http://127.0.0.1:5001/transaction',json = new_transaction)
print(r.text)