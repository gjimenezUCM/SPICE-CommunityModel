from bson.json_util import dumps, loads
import pymongo
from pymongo import MongoClient
from copy import copy, deepcopy

from cmSpice.dao.dao_db import DAO_db



class DAO_db_community(DAO_db):
    """
    DAO for accessing community related data in MongoDB
    Contains basics CRUD operations and some operations to manage 'Files'
    """

    #def __init__(self, db_host="mongodb", db_port=27017, db_user="spice", db_password="spicepassword", db_name="spiceComMod"):
    def __init__(self):
        """
        :Parameters:
            db_host: mongodb address, Default value: "localhost"
            db_port: mongodb port, Default value: 27017
            db_user: mongodb user, Default value: ""
            db_password: mongodb pass, Default value: ""
            db_name: mongodb db name, Default value: "spiceComMod"
        """
        super().__init__()
        self.db_communities = self.mongo.spiceComMod.communities
        self.db_fullListCommunities = self.mongo.spiceComMod["communitiesVisualization"]

    def getData(self):
        return self.getCommunities()

    def deleteCommunity(self, communityId):
        """
        :Parameters:
            communityId: Community id, Type: <class 'str'>
        """
        response = self.db_communities.delete_one({'id': communityId})

    def insertCommunity(self, communityJSON):
        """
        Inserts only 1 community to db_communities
        :Parameters:
            communityJSON: Community, Type: <class 'dict'> OR list(<class 'dict'>)
        """
        temp = copy(communityJSON)
        if type(temp) is list:
            self.db_communities.insert_many(temp)
        else:
            self.db_communities.insert_one(temp)



    def insertFileList(self, fileId, dataJSON):
        """
        Inserts json file to 'API Vis DB' and all communities from file to db_communities
            :Parameters:
                fileId: id, Type: <class 'dict'>
                communityJSON: Community, Type: <class 'dict'>
        """
        temp = copy(dataJSON)
        temp["fileId"] = fileId
        self.db_fullListCommunities.insert_one(copy(temp))
        for community in temp["communities"]:
            self.db_communities.insert_one(community)

    def getFileIndex(self):
        data = self.db_fullListCommunities.find({}, {"fileId": 1, "_id": 0})
        data = loads(dumps(list(data)))
        index = []
        for file in data:
            index.append(file["fileId"])
        return index

    def getFileList(self, fileId):
        """
        Returns file
        :Parameters:
                fileId: id, Type: <class 'dict'>
        :Return:
            File List
        """
        data = self.db_fullListCommunities.find({"fileId": fileId}, {"_id": 0})
        data = loads(dumps(list(data)))
        if len(data) == 0:
            return {}
        return data[0]

    def getFileLists(self):
        """
        Returns all files
        :Return:
            All File Lists
        """
        data = self.db_fullListCommunities.find({}, {"_id": 0})
        return loads(dumps(list(data)))

    def getCommunities(self):
        """
        :Return:
            Communities, Type: List[<class 'dict'>]
        """
        data = self.db_communities.find({}, {"_id": 0})
        return loads(dumps(list(data)))
    
    def getCommunitiesPerspective(self, perspectiveId):
        """
        :Return:
            Communities, Type: List[<class 'dict'>]
        """
        data = self.db_communities.find({"perspectiveId": perspectiveId, "community-type": "implicit"}, {"_id": 0})
        return loads(dumps(list(data)))
        
    def getCommunity(self, communityId):
        """
        :Parameters:
            communityId: Community id, Type: <class 'str'>
        :Return:
            Community, Type: <class 'dict'>
        """
        data = self.db_communities.find({"id": communityId}, {"_id": 0})
        data = loads(dumps(list(data)))
        if len(data) == 0:
            return {}
        return data[0]

    def getCommunityUsers(self, communityId):
        """
        :Parameters:
            communityId: Community id, Type: <class 'str'>
        :Return:
            Community users, Type: list[<class 'dict'>]
        """
        data = self.db_communities.find({"id": communityId}, {"users": 1, "_id": 0})
        return loads(dumps(list(data)))[0]

    def addUserToCommunity(self, communityId, newUser):
        """
        :Parameters:
            communityId: Community id, Type: <class 'str'>
            newUser: user, Type: <class 'dict'>
        """
        user = copy(newUser)
        response = self.db_communities.update_one(
            {"id": communityId},
            {
                "$push": {
                    "users": user
                }
            }
        )
        return response

    def replaceCommunity(self, communityId, newJSON):
        """
        :Parameters:
            communityId: Community id, Type: <class 'str'>
            newJSON: JSON value, Type: <class 'dict'>
        """
        temp = copy(newJSON)
        response = self.db_communities.replace_one({"id": communityId}, temp)
        return response

    def updateExplanation(self, communityId, newValue):
        """
        :Parameters:
            communityId: Community id, Type: <class 'str'>
            newValue: explanation, Type: <class 'str'>
        """
        value = copy(newValue)
        response = self.db_communities.update_one(
            {"id": communityId},
            {
                "$set": {
                    "explanation": value
                }
            },
            upsert=True
        )
        return response

    def dropAll(self):
        """
            Mongo DB Drop all documents in db_communities and db_fullListCommunities collection
        """
        self.drop()
        self.dropFullList()

    def drop(self,dropFilter = {}):
        """
            Mongo DB Drop all documents in db_communities collection
        """
        self.db_communities.delete_many(dropFilter)

    def dropFullList(self,dropFilter = {}):
        """
            Mongo DB Drop all documents in db_fullListCommunities collection
        """
        self.db_fullListCommunities.delete_many(dropFilter)
