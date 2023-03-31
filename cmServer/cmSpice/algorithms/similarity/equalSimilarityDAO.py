# Authors: José Ángel Sánchez Martín
import os
import json

import numpy as np
import itertools

from cmSpice.algorithms.similarity.similarityDAO import SimilarityDAO

class EqualSimilarityDAO(SimilarityDAO):
    """
    Class to check if two attribute values are equal
    """
    
    def distanceItems(self, valueA, valueB):
        """
        Method to obtain the distance between two valid values given by the similarity measure.

        Parameters
        ----------
        valueA : object
            Value of first element corresponding to elemA in self.data
        valueB : object
            Value of first element corresponding to elemB in self.data

        Returns
        -------
        double
            Distance between the two values.
        """
        if (isinstance(valueA, dict) and isinstance(valueB, dict) and len(valueA) > 0 and len(valueB) > 0):
            emotionsListA = [key for key, value in valueA.items() if value == max(valueA.values())]
            emotionsListB = [key for key, value in valueB.items() if value == max(valueB.values())]

            intersectionList = list(set(emotionsListA) & set(emotionsListB))

            if (len(intersectionList) > 0):
                distance = 0.0
            else:
                distance = 1.0
        elif (isinstance(valueA, list) and isinstance(valueB, list) and len(valueA) > 0 and len(valueB) > 0):
            setA = set(valueA)
            setB = set(valueB)

            intersection = setA.intersection(setB)
            union = setA.union(setB)

            distance = 1 - (len(intersection) / len(union))
        elif (valueA != valueB):
            distance = 1.0
        else:
            distance = 0.0

        return distance

#-------------------------------------------------------------------------------------------------------------------------------
#   To calculate dominant value
#-------------------------------------------------------------------------------------------------------------------------------
       
    # def dominantValue(self, valueA, valueB):
    #     #return valueA
    #     if isinstance(valueA, dict):
    #         return [valueA, valueB]
    #     if self.similarityColumn == 'id':
    #         return [{valueA: self.artworkA['id'].to_list()[0]}, {valueB: self.artworkB['id'].to_list()[0]}]
    #     else:
    #         return [valueA, valueB]
        
        
    
    
    