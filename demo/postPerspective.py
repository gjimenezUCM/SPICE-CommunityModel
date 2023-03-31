import json
import requests
import sys
from config import configDict
from requests.auth import HTTPBasicAuth

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

    # Change Sample Perspective
    filename = 'samplePerspective.json'
    auth = HTTPBasicAuth(configData['user'], configData['pass'])

    #--------------------------------------------------------------------------------------------------------------------------
    #    Insert perspective
    #--------------------------------------------------------------------------------------------------------------------------

    route = "data/" + museum + "/" + filename
    file = open(route)
    perspective = json.load(file)
    
    response = requests.post("{}/v2.0/perspectives".format(server), json=perspective, auth=auth)
    print(response)
    print(response.text)
    

main()
