import requests
import json

print("register node 5000")
m_node = {   
    "nodes" : ["http://192.168.0.1:5000"]
}
r = requests.post('http://127.0.0.1:5001/nodes/register',json = m_node)
print(r.text)
print("---------------------------------------------------------------")
print("get update")
r = requests.get('http://127.0.0.1:5001/nodes/resolve')
print(r.text)
print("---------------------------------------------------------------")