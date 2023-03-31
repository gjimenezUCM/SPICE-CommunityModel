import json
from bson.json_util import dumps, loads
from copy import copy, deepcopy
import pymongo
from pymongo import MongoClient

from cmSpice.dao.dao_db import DAO_db


# {
#     _id: "0",
#     perspectiveId: "0",
#     description: "Opinions regarding Roman Rebellion",
#     similarities: {
#         "belief Roman Rebellion": 0.7
#         "openess": 0.2
#         "history" : 0.1
#     }
# }
# Similarities: key (attribute); value (weight or importance)

class DAO_db_perspectives(DAO_db):
    """
    DAO for accessing perspective related data in MongoDB
    Contains basics CRUD operaions
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
        self.db_perspectives = self.mongo.spiceComMod.perspectives

    def getData(self):
        return self.getPerspectives()

    def insertPerspective(self, perspectiveJSON):
        """
        :Parameters:
            perspectiveJSON: Perspective, Type: <class 'dict'>
        """
        temp = copy(perspectiveJSON)
        if type(temp) is list:
            self.db_perspectives.insert_many(temp)
        else:
            self.db_perspectives.insert_one(temp)

    def getPerspectives(self):
        """
        :Return:
            perspectives, Type: List[<class 'dict'>]
        """
        data = self.db_perspectives.find({}, {"_id": 0})
        return loads(dumps(list(data)))

    def getPerspective(self, perspectiveId):
        """
        :Parameters:
            perspectiveId: Type: <class 'str'>
        :Return:
            perspective, Type: <class 'dict'>
        """
        data = {}
        data = self.db_perspectives.find({"id": perspectiveId}, {"_id": 0})
        #data = self.db_perspectives.find({"_id": perspectiveId})

        data = loads(dumps(list(data)))
        if len(data) == 0:
            return {}
        return data[0]   

    def updatePerspective(self, perspectiveId, newJSON):
        """
        :Parameters:
            perspectiveId: Type: <class 'str'>
            newJSON: JSON value, Type: <class 'dict'>
        """
        temp = copy(newJSON)
        response = self.db_perspectives.replace_one({"id": perspectiveId}, temp)

    def deletePerspective(self, perspectiveId):
        """
        :Parameters:
            perspectiveId: Type: <class 'str'>
        """
        self.db_perspectives.delete_one({'id': perspectiveId})

    def drop(self):
        """
            MongoDB Delete Documents in this collection
        """
        self.db_perspectives.delete_many({})
