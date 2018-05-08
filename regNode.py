import requests
import json

print("register node 5000 and 5001")
m_node = {   
    "nodes" : ["http://127.0.0.1:5000","http://127.0.0.1:5001","http://127.0.0.1:5002"]
}
r = requests.post('http://127.0.0.1:5000/nodes/register',json = m_node)
print(r.text)
print("---------------------------------------------------------------")