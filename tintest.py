import requests
import json

print("get all info from chain")
r = requests.get('http://127.0.0.1:5000/chain')
print(r.text)
print("---------------------------------------------------------------")

block = {   
    "upc" : "300871365612", 
    "item_no":1,
    "owner": "TinVu",
}
print("mine 1000 products to blockchain")
for a in range(1, 5):
    block['item_no'] = a
    #print(block)
    r = requests.post('http://127.0.0.1:5000/register',json = block)

r = requests.get('http://127.0.0.1:5000/chain')
print(r.text)
print("---------------------------------------------------------------")

trans_block = {   
    "upc" : "300871365612", 
    "item_no":1,
    "current_owner": "TinVu",
    "new_owner": "A",
}
#r = requests.post('http://127.0.0.1:5000/transaction',json = trans_block)
print("do transaction 10 products to blockchain")
for a in range(1, 5):
    trans_block['new_owner'] =  trans_block['new_owner']+str(a)
    trans_block['item_no'] = a
    #print(trans_block)
    r = requests.post('http://127.0.0.1:5000/transaction',json = trans_block)

r = requests.get('http://127.0.0.1:5000/chain')
print(r.text)
print("---------------------------------------------------------------")

print("validate 300871365612,1,TinVu ")
murl ='http://127.0.0.1:5000/validate/300871365612,1,TinVu'
r = requests.get(murl)

print(r.text)
print("---------------------------------------------------------------")

print("validate 300871365612,1,A1")
murl ='http://127.0.0.1:5000/validate/300871365612,1,A1'
r = requests.get(murl)

print(r.text)
print("---------------------------------------------------------------")