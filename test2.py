
import requests
import json

option =-1
serverUrl ="http://127.0.0.1:"
mPort = 5000
block = {   
    "upc" : "300871365612",
    "item_no":1,
    "new_owner": "TinVu",
}
trans_block = {   
    "upc" : "300871365612",
    'manufacturer': "",
    "item_no":1,
    "current_owner": "TinVu",
    "new_owner": "A",
}   
    
def nodeReg():
    print("register node 5000, 5001, 5002, 5003, 5004, 5005")
    m_node = {   
        "nodes" : ["http://127.0.0.1:5000","http://127.0.0.1:5001",
        "http://127.0.0.1:5002","http://127.0.0.1:5003","http://127.0.0.1:5004","http://127.0.0.1:5005"]
    }
    myURL = serverUrl+'/nodes/register'
    r = requests.post(myURL,json = m_node)
    print(r.text)
    print("--------------------------------------------------------------------------------")

def getChain():
    print("get all info from chain")
    myURL = serverUrl+'/chain'
    r = requests.get(myURL)
    print(r.text)
    print("------------------------------------------------------------------------------------")

def mineProduct():
    print("mine 1000 products to blockchain")
    myURL = serverUrl+'/register'
    for a in range(1, 5):
        block['item_no'] = a
        #print(block)
        r = requests.post(myURL,json = block)
        print(r.text)
        print("---------------------------------------------------------------")


def transProduct():
    #r = requests.post('http://127.0.0.1:5000/transaction',json = trans_block)
    print("do transaction 10 products to blockchain")
    print("Please enter manufacturer ID")
    c_owner = input()
    trans_block['manufacturer'] = c_owner
    print("current manufacturer",trans_block)
    myURL = serverUrl+'/transaction'
    for a in range(1, 5):
        trans_block['new_owner'] =  trans_block['new_owner']+str(a)
        trans_block['item_no'] = a
        #print(trans_block)
        r = requests.post(myURL,json = trans_block)
        print(r.text)
        print("---------------------------------------------------------------")

def validateProduct():

    print("validate 300871365612,1,TinVu ")
    myURL = serverUrl+'/validate/300871365612,1,TinVu'
    r = requests.get(myURL)
    print(r.text)
    print("---------------------------------------------------------------")

    print("validate 300871365612,1,A1")
    myURL = serverUrl+'/validate/300871365612,1,A1'
    r = requests.get(myURL)
    print(r.text)
    print("---------------------------------------------------------------")

def relicateChain():
    print("update chain with neighbor node ")
    myURL = serverUrl+'/nodes/resolve'
    r = requests.get(myURL)
    print(r.text)
    print("---------------------------------------------------------------")

while option == -1:
    print("Please enter port number of your server from 5000 to 6000")
    try:
        mPort = int(input())
        if mPort < 5000 or mPort >6000:
            print('not in the range of 5000 to 6000')
        else:
            serverUrl += str(mPort)
            print("your are running ",serverUrl)
            option = 1
            while option > 0:
                print("Please enter :1 for register, 2: to registry new product, 3 for transfer,4 for validate product, 5 for replicate, 6 to get the chain" )
                try:
                    option = int(input())
                    if option ==1:
                        nodeReg()
                    if option ==2:
                        mineProduct()
                    if option ==3:
                        transProduct()
                    if option ==4:
                        validateProduct()
                    if option ==5:
                        relicateChain()
                    if option ==6:
                        getChain()
                except ValueError:
                #Handle the exception
                    print('Please enter an integer')
    except ValueError:
    #Handle the exception
        print('Please enter an integer')






