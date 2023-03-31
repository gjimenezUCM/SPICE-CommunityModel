# Authors: José Ángel Sánchez Martín


import os
from inspect import getsourcefile
#from os.path import abspath, dirname
import numpy as np

from cmSpice.algorithms.similarity.similarityDAO import SimilarityDAO
from cmSpice.dao.dao_csv import DAO_csv


class TableSimilarityDAO(SimilarityDAO):

    def __init__(self, dao, similarityFunction):
        """
        Construct of similarity objects for which the similarity values between items are given in a .csv

        Parameters
        ----------
        dao : dao_db_users class
            DAO which retrieves the user data
        similarityFunction: dict class including
            att_name: name of the attribute (column) the similarity measure is used upon
            weight: weight of the similarity measure
        """
        super().__init__(dao, similarityFunction)
        self.similarityCol = similarityFunction['on_attribute']['att_name']
        self.getSimilarityTable()

    def getSimilarityTableName(self):
        return self.similarityCol
        
    def getSimilarityTable(self):
        dao_csv = DAO_csv(os.path.dirname(os.path.abspath(getsourcefile(lambda:0))) + "/distanceTables/" + self.getSimilarityTableName() + ".csv")
        self.similarityTable = dao_csv.getPandasDataframe().set_index('Key')

    def distanceValues(self, keyA, keyB):
        return self.getDistanceBetweenItems(keyA, keyB)

    def distanceItems(self, keyA, keyB):
        """
        Method to obtain the distance between two table keys or labels.

        Parameters
        ----------
        keyA : String
            
        keyB : String
            

        Returns
        -------
        double
            Distance between the two table keys.
        """
        # Property was not given (nan)
        if (keyA != keyA or keyB != keyB):
            return 1.0
            
        # Key doesnt exist in the table
        if ({keyA, keyB}.issubset(self.similarityTable.columns) == False):
            return 1.0
            
        distance = self.similarityTable.loc[keyA][keyB]
        return distance

