
import requests
import json

option =-1
currentIndex =1
serverUrl ="http://127.0.0.1:"
mPort = 5000
manufacturer =""
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
    result = json.loads(r.text)
    global manufacturer
    manufacturer = result['ID']
    print(r.text)
    print("ID",manufacturer)
    print("--------------------------------------------------------------------------------")

def getChain(printOption):
    if printOption == 1:
        print("get all info from chain")
        myURL = serverUrl+'/chain'
        r = requests.get(myURL)
        print(r.text)
        print("------------------------------------------------------------------------------------")
    else:
        myURL = serverUrl+'/chain'
        r = requests.get(myURL)
        result = json.loads(r.text)
        currentIndex = int(result['length'])
        print(currentIndex)
        print("------------------------------------------------------------------------------------")
        
       

def mineProduct():
    myURL = serverUrl+'/register'
    getChain(2)
    print("press 1 mine a product 2 to auto mine 5 product to blockchain")
    loption = int(input())
    if loption==1:
        print("please input new owner")
        lnewowner = input()
        block['item_no']=currentIndex +1
        block['new_owner']= lnewowner
        r = requests.post(myURL,json = block)
        print(r.text)
        print("---------------------------------------------------------------")
    else:
        start = currentIndex+1
        for a in range(start,start+ 5):
            block['item_no'] = a
            #print(block)
            r = requests.post(myURL,json = block)
            print(r.text)
            print("---------------------------------------------------------------")


def transProduct():
    #r = requests.post('http://127.0.0.1:5000/transaction',json = trans_block)
    myURL = serverUrl+'/transaction'
    getChain(2)
    trans_block['manufacturer'] = manufacturer
    print("from :",manufacturer)
    print("press 1 transfer from manufacture 2 to enter a name")
    loption = int(input())
    if loption==1:      
        print("please enter item number")
        item = int(input())
        trans_block['item_no'] = item
        print("please enter new owner")
        new = input()
        trans_block['new_owner'] = new
        print("please enter old owner")
        old = input()
        trans_block['current_owner'] = old
        print("here",trans_block)
        r = requests.post(myURL,json = trans_block)
        print(r.text)
        print("---------------------------------------------------------------")
    else:
        print("please enter item number")
        item = int(input())
        trans_block['item_no'] = item
        print("please enter new owner")
        new = input()
        trans_block['new_owner'] = new
        print("please enter old owner")
        old = input()
        trans_block['current_owner'] = old
        print("here",trans_block)
        r = requests.post(myURL,json = trans_block)
        print(r.text)
        print("---------------------------------------------------------------")

def validateProduct():
    myURL = serverUrl+'/validate/300871365612,'+ manufacturer+','
    print("please enter item number")
    item = input()
    myURL += str(item)
    print("please enter owner")
    owner = input()
    myURL += ','+owner
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
                        getChain(1)
                except ValueError:
                #Handle the exception
                    print('Please enter an integer')
    except ValueError:
    #Handle the exception
        print('Please enter an integer')






