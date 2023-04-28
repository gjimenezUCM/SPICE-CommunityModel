import json
import os
import requests
from requests.auth import HTTPBasicAuth


from cmSpice.dao.dao_class import DAO




class DAO_api(DAO):
    """
    DAO used only for test Spice API

    Usada solo para hacer pruebas
    Es la DAO para acceder a la API oficial de Spice.
    """
    def __init__(self, route=""):
        super().__init__(route)
        self.auth = HTTPBasicAuth(os.environ['API_USER'], os.environ['API_PASS'])
        self.pathApp = "http://app:" + os.environ['NODE_DOCKER_PORT']


    def getData(self):
        raise ValueError('Incorrect operation. Please use a specific method for the API request')

    def addPerspective(self, ugc):
        response = requests.post(self.pathApp + "/v2.0/perspective", json=ugc, auth=self.auth)
        return response

    def responseProcessing(self, response):
        """Process response from API"""
        if response.status_code == 400:
            return
        self.data = response.json()
        # self.data = json.dumps(self.data, sort_keys=True, indent=4)

    """__API for users__"""

    def userCommunities(self, userId):
        response = requests.get(self.pathApp + "/v2.0/users/{}/communities".format(userId), auth=self.auth)
        self.responseProcessing(response)
        return self.data, response

        # "Update community model with new user generated content"
        # tambien se puede llamar como updateUGC

    def updateUser(self, userId, ugc):
        response = requests.post(self.pathApp + "/v2.0/users/{}/update-generated-content".format(userId),
                                 json=ugc, auth=self.auth)
        return response

    """__API for communities__"""

    def communityList(self):
        response = requests.get(self.pathApp + "/v2.0/communities", auth=self.auth)
        self.responseProcessing(response)
        return self.data, response

    def communityDescription(self, communityId):
        response = requests.get(self.pathApp + "/v2.0/communities/{}".format(communityId), auth=self.auth)
        self.responseProcessing(response)
        return self.data, response

    def communityUsers(self, communityId):
        response = requests.get(self.pathApp + "/v2.0/communities/{}/users".format(communityId), auth=self.auth)
        self.responseProcessing(response)
        return self.data, response
        
    """__API for perspectives__"""
    def perspectiveList(self):
        response = requests.get(self.pathApp + "/v2.0/perspectives", auth=self.auth)
        self.responseProcessing(response)
        return self.data, response
        
    def perspectiveCommunities(self,perspectiveId):
        print( self.pathApp + "/v2.0/perspectives/{}/communities".format(perspectiveId) )
        response = requests.get(self.pathApp + "/v2.0/perspectives/{}/communities".format(perspectiveId), auth=self.auth)
        self.responseProcessing(response)
        return self.data, response
    
    """__API for similarities__"""
    def similarityCommunities(self,communityId,otherCommunityId):
        response = requests.get(self.pathApp + "/v2.0/communities/{}/similarity/{}".format(communityId,otherCommunityId), auth=self.auth)
        self.responseProcessing(response)
        return self.data, response
        
    def dissimilarityCommunities(self,communityId,otherCommunityId):
        response = requests.get(self.pathApp + "/v2.0/communities/{}/dissimilarity/{}".format(communityId,otherCommunityId), auth=self.auth)
        self.responseProcessing(response)
        return self.data, response

    def getSeedFile(self):
        print(self.auth)
        response = requests.get(self.pathApp + "/v2.0/visir/seed", auth=self.auth)
        self.responseProcessing(response)
        return self.data, response
        
