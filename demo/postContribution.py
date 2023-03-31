import requests
import json
import sys
from config import configDict
from requests.auth import HTTPBasicAuth

#--------------------------------------------------------------------------------------------------------------------------
#    Used to post contribution data (dict of interaction_attributes)
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
    filename = 'ugcContributions.json'
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

    postDictKeys = ["English translation", "plutchik_emotions"]
    postDictKeys = postDict.keys()
    for ctype in postDictKeys:
        contribsDict = postDict[ctype]
        for key, value in contribsDict.items():
            response=requests.post(f'{server}/v2.0/users/{key}/update-generated-content', json = value, auth=auth)
            
            print("key: " + str(key))
            print("value: " + str(value))
            print(response)
            print("\n\n")


main()