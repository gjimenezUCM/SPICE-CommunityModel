import json
from bson.json_util import dumps, loads
from copy import copy, deepcopy
import pymongo
from pymongo import MongoClient

from cmSpice.dao.dao_db import DAO_db




class DAO_db_similarity(DAO_db):
    """
        DAO for accessing similarities related data in MongoDB
        Contains basics CRUD operations
    """

    #def __init__(self, db_host="mongodb", db_port=27017, db_user="spice", db_password="spicepassword", db_name="spiceComMod"):
    def __init__(self):
        """
        :Parameters:
            db_host: mongodb address, Default value: "localhost"
            db_port: mongodb port, Default value: 27018
            db_user: mongodb user, Default value: ""
            db_password: mongodb pass, Default value: ""
            db_name: mongodb db name, Default value: "spiceComMod"
        """
        super().__init__()
        self.db_similarities = self.mongo.spiceComMod.similarities


    def getData(self):
        return self.getSimilarities()

    def deleteSimilarity(self, target_community_id="", other_community_id=""):
        """
        :Parameters:
            target_community_id: Type: <class 'str'>
            OR
            other_community_id: Type: <class 'str'>
        """
        if target_community_id != "":
            self.db_similarities.delete_one({'target-community-id': target_community_id})
        if other_community_id != "":
            self.db_similarities.delete_one({'other-community-id': other_community_id})

    def insertSimilarity(self, similarityJSON):
        """
        :Parameters:
            similarityJSON: similarity, Type: <class 'dict'>
        """
        temp = copy(similarityJSON)
        if type(temp) is list:
            self.db_similarities.insert_many(temp)
        else:
            self.db_similarities.insert_one(temp)

    def getSimilarities(self):
        """
        :Return:
            Similarities, Type: List[<class 'dict'>]
        """
        data = self.db_similarities.find({}, {"_id": 0})
        return loads(dumps(list(data)))

    def getSimilarity(self, target_community_id="", other_community_id=""):
        """
        :Parameters:
            target_community_id: Type: <class 'str'>
            OR
            other_community_id: Type: <class 'str'>
        :Return:
            Similarity, Type: <class 'dict'>
        """
        data = {}
        if target_community_id != "":
            data = self.db_similarities.find({"target-community-id": target_community_id}, {"_id": 0})
        if other_community_id != "":
            data = self.db_similarities.find({"other-community-id": other_community_id}, {"_id": 0})

        data = loads(dumps(list(data)))
        if len(data) == 0:
            return {}
        return data[0]

    def updateSimilarity(self, target_community_id="", other_community_id="", newJSON={}):
        """
        :Parameters:
            target_community_id: Type: <class 'str'>
            OR
            other_community_id: Type: <class 'str'>

            newJSON: JSON value, Type: <class 'dict'>
        """
        """
        response = ""
        temp = copy(newJSON)
        if target_community_id != "":
            response = self.db_similarities.replace_one({"target-community-id": target_community_id}, temp)
        if other_community_id != "":
            response = self.db_similarities.replace_one({"other-community-id": other_community_id}, temp)
        return response
        """
        
        key = {'target-community-id': target_community_id, 'other-community-id': other_community_id}
        response = self.db_similarities.update_one(key,{"$set": newJSON},upsert=True)
        
        print("json inserted: " )
        print(newJSON)
        print("\n")


    def drop(self):
        """
            MongoDB Delete Documents in this collection
        """
        self.db_similarities.delete_many({})
