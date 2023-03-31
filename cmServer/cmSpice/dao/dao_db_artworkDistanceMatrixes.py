from bson.json_util import dumps, loads
from copy import copy, deepcopy
import pymongo
from pymongo import MongoClient

from cmSpice.dao.dao_db import DAO_db

class DAO_db_artworkDistanceMatrixes(DAO_db):
    """
    DAO for storing and accessing the distance matrix associated to the first similarity object (artworks)

    In the case of HECHT, there are not artworks. Consequently, HECHT users are the first similarity object and 
    this DAO is used for their user data too.

    -------------------------------------------------------------------------------------------------------------
    Each object includes:

    attribute: name of the column the similarity measure is applied to
    similarity: name of the similarity measure (e.g., EqualSimilarity, EmotionSimilarity)
    index: array listing the artwork data index. This allows to update the distance matrix if a new artwork is added 
    without computing everything again.
    distanceMatrix: distance matrix associated to the current artworks
    dominantValueMatrix: matrix of dominant values used for community explanations. 

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
        self.db_artworkDistanceMatrixes = self.mongo.spiceComMod.artworkDistanceMatrixes


    def getData(self):
        pass
        
    def insertArtworkDistanceMatrix(self, artworkDistanceMatrixJSON):
        """
        :ParametersworkDistanceMatrix:
            artworkDistanceMatrixJSON: artworkDistanceMatrix associated to the perspective and the user.
        """
        temp = copy(artworkDistanceMatrixJSON)
        if type(temp) is list:
            self.db_artworkDistanceMatrixes.insert_many(temp)
        else:
            self.db_artworkDistanceMatrixes.insert_one(temp)
    
    def getArtworkDistanceMatrixes(self):
        """
        :Return:
            List with all artworkDistanceMatrixes, Type: json List[<class 'dict'>]
        """
        # data = self.db_users.find({}, {"_id": 0})
        dataList = self.db_artworkDistanceMatrixes.find({})
        dataList = loads(dumps(list(dataList)))
        return dataList
        
    def getArtworkDistanceMatrix(self, attribute, similarity):
        """
        :Parameters:
            attribute: name of the column the similarity measure is applied to
                Type: <class 'str'>
            similarity: name of the similarity measure (e.g., EqualSimilarity, EmotionSimilarity)
                Type: <class 'str'>
        :Return:
            DistanceMatrix json associated to the two parameters,  Type: <class 'dict'>
        """
        data = {}
        data = self.db_artworkDistanceMatrixes.find({"attribute": attribute, "similarity": similarity}, {"_id": 0})
        
        data = loads(dumps(list(data)))
        if len(data) == 0:
            return {}
        return data[0]
    
    def updateDistanceMatrix(self, artworkDistanceMatrixJSON):
        key = {'attribute': artworkDistanceMatrixJSON['attribute'], 'similarity': artworkDistanceMatrixJSON['similarity']}
        self.db_artworkDistanceMatrixes.update_one(key,{"$set": artworkDistanceMatrixJSON},upsert=True)

 
    def drop(self):
        """
            Deletes all data in collection
        """
        self.db_artworkDistanceMatrixes.delete_many({})

    def deleteDistanceMatrix(self, artworkDistanceMatrixJSON):
        """
        :Parameters:
            artworkDistanceMatrixJSON: DistanceMatrix/s, Type: <class 'dict'> OR List[<class 'dict'>]
        """
        self.db_artworkDistanceMatrixes.delete_one(artworkDistanceMatrixJSON)

        
        
