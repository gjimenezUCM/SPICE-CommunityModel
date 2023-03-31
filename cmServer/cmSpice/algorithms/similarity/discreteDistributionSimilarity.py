# Authors: José Ángel Sánchez Martín


import os
from inspect import getsourcefile
#from os.path import abspath, dirname
import numpy as np

from cmSpice.algorithms.similarity.similarityDAO import SimilarityDAO

class DiscreteDistributionSimilarity(SimilarityDAO):

    def __init__(self, dao, similarityFunction):
        """
        Construct of similarity objects for which the similarity values between items are sorted according to a discrete distribution encoded by a list

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
        self.similarityDict = self.initializeDiscreteDistributionDict()

    def initializeDiscreteDistributionDict(self):
        similarityDict = {
            "demographics.water_electricity": ['very worried', 'worried', 'neutral', 'unworried', 'very unworried'],
            "demographics.food": ['very worried', 'worried', 'neutral', 'unworried', 'very unworried'],
            "demographics.consumption": ['very worried', 'worried', 'neutral', 'unworried', 'very unworried']
        }
        return similarityDict

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
        distance = 1.0
        if (keyA != keyA or keyB != keyB):
            distance = 1.0
        elif (self.similarityColumn in self.similarityDict):
            if (keyA in self.similarityDict[self.similarityColumn] and keyB in self.similarityDict[self.similarityColumn]):
                indexA = self.similarityDict[self.similarityColumn].index(keyA)
                indexB = self.similarityDict[self.similarityColumn].index(keyB)

                maxDifference = max(1, len(self.similarityDict[self.similarityColumn]) - 1)
                distance = (abs(indexA - indexB)) / maxDifference
        else:
            distance = 1.0

        return distance
