from bson.json_util import dumps, loads
from copy import copy, deepcopy
import pymongo
from pymongo import MongoClient

from cmSpice.dao.dao_db import DAO_db

class DAO_db_interactionDistances(DAO_db):
    """
    DAO for storing and accessing the interaction similarity data

    -------------------------------------------------------------------------------------------------------------
    Each object includes:

    attribute: name of the column the similarity measure is applied to (Interaction attribute: emotions, sentiments, values)
    similarity: name of the similarity measure (e.g., EqualSimilarity, EmotionSimilarity)
    citizen1: name of the first citizen
    artwork1: artwork id asociated to citizen1. It corresponds to the 'id' attribute in artworks data.
    citizen2: name of the second citizen
    artwork2: artwork id asociated to citizen2. It corresponds to the 'id' attribute in artworks data.
    distance: distance between the interaction attribute associated to citizen1-artwork1 and citizen2-artwork2
    dominantValue (List): dominant attribute values summarizing the interaction between citizen1-artwork1 and citizen2-artwork2
        [dominantValue(citizen1), dominantValue(citizen2)]

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
        self.db_interactionDistances = self.mongo.spiceComMod.interactionDistances


    def getData(self):
        pass
        
    def insertInteractionDistance(self, interactionDistanceJSON):
        """
        :Parameters:
            interactionDistanceJSON: JSON object encoding the similarity information between 2 user interactions 
        """
        temp = copy(interactionDistanceJSON)
        if type(temp) is list:
            self.db_interactionDistances.insert_many(temp)
        else:
            self.db_interactionDistances.insert_one(temp)
    
    def getInteractionDistances(self):
        """
        :Return:
            List with all interactionDistances, Type: json List[<class 'dict'>]
        """
        # data = self.db_users.find({}, {"_id": 0})
        dataList = self.db_interactionDistances.find({})
        dataList = loads(dumps(list(dataList)))
        return dataList
        
    def getInteractionDistance(self, interactionDistanceJSON):
        """
        :Parameters:
            interactionDistanceJSON: dict object with the following parameters:
                attribute
                similarity
                citizen1
                artwork1
                citizen2
                artwork2

        :Return:
            Distance json associated to the two interactions,  Type: <class 'dict'>
        """
        data = {}
        data = self.db_interactionDistances.find(interactionDistanceJSON, {"_id": 0})
        
        data = loads(dumps(list(data)))
        if len(data) == 0:
            return {}
        return data[0]
    
    def updateInteractionDistance(self, interactionDistanceJSON):
        updateObject = {}
        updateObject['attribute'] = interactionDistanceJSON['attribute']
        updateObject['similarity'] = interactionDistanceJSON['similarity']
        updateObject['citizen1'] = interactionDistanceJSON['citizen1']
        updateObject['artwork1'] = interactionDistanceJSON['artwork1']
        updateObject['citizen2'] = interactionDistanceJSON['citizen2']
        updateObject['artwork2'] = interactionDistanceJSON['artwork2']

        key = updateObject
        self.db_interactionDistances.update_one(key,{"$set": interactionDistanceJSON},upsert=True)

 
    def drop(self):
        """
            Deletes all data in collection
        """
        self.db_interactionDistances.delete_many({})

    def deleteInteractionDistance(self, interactionDistanceJSON):
        """
        :Parameters:
            interactionDistanceMatrixJSON: DistanceMatrix/s, Type: <class 'dict'> OR List[<class 'dict'>]
        """
        self.db_interactionDistances.delete_one(interactionDistanceJSON)

        
        
