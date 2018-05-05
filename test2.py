
import requests
import json

print("register nodw 5001")
m_node = {   
    "nodes" : ["http://192.168.0.1:5001"]
}
r = requests.post('http://127.0.0.1:5001/nodes/register',json = m_node)
print(r.text)
print("---------------------------------------------------------------")

print("get all info from chain")
r = requests.get('http://127.0.0.1:5001/chain')
print(r.text)
print("---------------------------------------------------------------")



