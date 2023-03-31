import requests
import json
import sys
from config import configDict
from requests.auth import HTTPBasicAuth

#--------------------------------------------------------------------------------------------------------------------------
#    Used to post demographic data (dict userid)
#--------------------------------------------------------------------------------------------------------------------------

def main():
    if len(sys.argv) < 2 :
        print("USAGE: python",__file__,"<museumName>")
        return -1

    museum = sys.argv[1]
    #--------------------------------------------------------------------------------------------------------------------------
    #    Select Configuration dictionary for a case study
    #--------------------------------------------------------------------------------------------------------------------------
    
    configData = configDict[museum]
    
    #--------------------------------------------------------------------------------------------------------------------------


    server = configData["server"]
    museum = configData["museum"]
    filename = 'ugcUsers.json'
    auth = HTTPBasicAuth(configData['user'], configData['pass'])
    
    #--------------------------------------------------------------------------------------------------------------------------
    #    Read data
    #--------------------------------------------------------------------------------------------------------------------------
    
    fileRoute = 'data/' + museum + '/' + filename
    with open(fileRoute, 'r', encoding='utf8') as f:
        data = json.load(f) 

    #--------------------------------------------------------------------------------------------------------------------------
    #    Perform POST requests (interactions)
    #--------------------------------------------------------------------------------------------------------------------------
    
    postDict = data

    postDictKeys = postDict.keys()
    for userid in postDictKeys:
        userArray = postDict[userid]
        
        # print("key: " + str(userid))
        # print("value: " + str(userData))
        
        print("userid: " + str(userid))
        print("value: " + str(userArray))
        print("\n")
        response=requests.post(f'{server}/v2.0/users/{userid}/update-generated-content', json = userArray, auth=auth)
        print(response)
        print("\n\n")
            


main()