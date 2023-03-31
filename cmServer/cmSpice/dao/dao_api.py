import json
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
        # self.route = route

    def getData(self):
        raise ValueError('Incorrect operation. Please use a specific method for the API request')

    def addPerspective(self, ugc):
        response = requests.post("http://localhost:8080/v2.0/perspective", json=ugc)
        return response

    def responseProcessing(self, response):
        """Process response from API"""
        if response.status_code == 400:
            return
        self.data = response.json()
        # self.data = json.dumps(self.data, sort_keys=True, indent=4)

    """__API for users__"""

    def userCommunities(self, userId):
        response = requests.get("http://localhost:8080/v2.0/users/{}/communities".format(userId))
        self.responseProcessing(response)
        return self.data, response

        # "Update community model with new user generated content"
        # tambien se puede llamar como updateUGC

    def updateUser(self, userId, ugc):
        response = requests.post("http://localhost:8080/v2.0/users/{}/update-generated-content".format(userId),
                                 json=ugc)
        return response

    """__API for communities__"""

    def communityList(self):
        response = requests.get("http://localhost:8080/v2.0/communities")
        self.responseProcessing(response)
        return self.data, response

    def communityDescription(self, communityId):
        response = requests.get("http://localhost:8080/v2.0/communities/{}".format(communityId))
        self.responseProcessing(response)
        return self.data, response

    def communityUsers(self, communityId):
        response = requests.get("http://localhost:8080/v2.0/communities/{}/users".format(communityId))
        self.responseProcessing(response)
        return self.data, response
        
    """__API for perspectives__"""
    def perspectiveList(self):
        response = requests.get("http://localhost:8080/v2.0/perspectives")
        self.responseProcessing(response)
        return self.data, response
        
    def perspectiveCommunities(self,perspectiveId):
        print( "http://localhost:8080/v2.0/perspectives/{}/communities".format(perspectiveId) )
        response = requests.get("http://localhost:8080/v2.0/perspectives/{}/communities".format(perspectiveId))
        self.responseProcessing(response)
        return self.data, response
    
    """__API for similarities__"""
    def similarityCommunities(self,communityId,otherCommunityId):
        response = requests.get("http://localhost:8080/v2.0/communities/{}/similarity/{}".format(communityId,otherCommunityId))
        self.responseProcessing(response)
        return self.data, response
        
    def dissimilarityCommunities(self,communityId,otherCommunityId):
        response = requests.get("http://localhost:8080/v2.0/communities/{}/dissimilarity/{}".format(communityId,otherCommunityId))
        self.responseProcessing(response)
        return self.data, response
        
