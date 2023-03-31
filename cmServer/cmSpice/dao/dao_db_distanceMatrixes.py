from bson.json_util import dumps, loads
from copy import copy, deepcopy
import pymongo
from pymongo import MongoClient

from cmSpice.dao.dao_db import DAO_db

class DAO_db_distanceMatrixes(DAO_db):
    """
    DAO for storing and accessing the distance matrix associated to a perspective's users.
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
        self.db_distanceMatrixes = self.mongo.spiceComMod.distanceMatrixes


    def getData(self):
        pass
        
    def insertDistanceMatrix(self, distanceMatrixJSON):
        """
        :Parameters:
            distanceMatrixJSON: distanceMatrix associated to the perspective and the user.
        """
        temp = copy(distanceMatrixJSON)
        if type(temp) is list:
            self.db_distanceMatrixes.insert_many(temp)
        else:
            self.db_distanceMatrixes.insert_one(temp)
    
    def getDistanceMatrixes(self):
        """
        :Return:
            List with all distanceMatrixes, Type: json List[<class 'dict'>]
        """
        # data = self.db_users.find({}, {"_id": 0})
        dataList = self.db_distanceMatrixes.find({})
        dataList = loads(dumps(list(dataList)))
        return dataList
        
    def getDistanceMatrix(self,perspectiveId):
        """
        :Parameters:
            perspectiveId: Type: <class 'str'>
        :Return:
            DistanceMatrix json associated to the perspective,  Type: <class 'dict'>
        """
        data = {}
        data = self.db_distanceMatrixes.find({"perspectiveId": perspectiveId}, {"_id": 0})
        
        data = loads(dumps(list(data)))
        if len(data) == 0:
            return {}
        return data[0]
    
    def updateDistanceMatrix(self, distanceMatrixJSON):
        key = {'perspectiveId': distanceMatrixJSON['perspectiveId']}
        self.db_distanceMatrixes.update_one(key,{"$set": distanceMatrixJSON},upsert=True)

 
    def drop(self):
        """
            Deletes all data in collection
        """
        self.db_distanceMatrixes.delete_many({})

    def deleteDistanceMatrix(self, distanceMatrixJSON):
        """
        :Parameters:
            distanceMatrixJSON: DistanceMatrix/s, Type: <class 'dict'> OR List[<class 'dict'>]
        """
        self.db_distanceMatrixes.delete_one(distanceMatrixJSON)

        
        
