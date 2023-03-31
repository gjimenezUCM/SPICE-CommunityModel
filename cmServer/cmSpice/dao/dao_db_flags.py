from bson.json_util import dumps, loads
from copy import copy, deepcopy
import pymongo
from pymongo import MongoClient

from cmSpice.dao.dao_db import DAO_db

class DAO_db_flags(DAO_db):
    """
    DAO for accessing flag related data in MongoDB
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
        self.db_flags = self.mongo.spiceComMod.flags


    def getData(self):
        pass
    

    def getFlag(self):
        """
        :Return:
            List with all flags, Type: json List[<class 'dict'>]
        """
        # data = self.db_users.find({}, {"_id": 0})
        dataList = self.db_flags.find({})
        dataList = loads(dumps(list(dataList)))
        return dataList[0]

    
        

    def drop(self):
        """
            Deletes all data in collection
        """
        self.db_flags.delete_many({})

    def insertFlag(self, flagJSON):
        """
        :Parameters:
            flagJSON: flag associated to the perspective and the user.
        """
        temp = copy(flagJSON)
        if type(temp) is list:
            self.db_flags.insert_many(temp)
        else:
            self.db_flags.insert_one(temp)

    def replaceFlag(self, flagJSON):
        self.db_flags.replace_one({'perspectiveId': flagJSON['perspectiveId'], 'userid': flagJSON['userid']}, flagJSON)
            
    def updateFlag(self, flagJSON):
        key = {'perspectiveId': flagJSON['perspectiveId'], 'userid': flagJSON['userid']}
        self.db_flags.update_one(key, {"$set": flagJSON}, upsert=True)
 
    def getFlags(self):
        """
        :Return:
            flags, Type: List[<class 'dict'>]
        """
        data = self.db_flags.find({}, {"_id": 0})
        return loads(dumps(list(data)))
        
    def deleteFlag(self, flagJSON):
        """
        :Parameters:
            flagJSON: Flag/s, Type: <class 'dict'> OR List[<class 'dict'>]
        """
        # self.db_flags.delete_one(flagJSON)
        #self.db_flags.delete_one({'id': flagId})
        self.db_flags.delete_one({'perspectiveId': flagJSON['perspectiveId'], 'userid': flagJSON['userid']})
        
        
