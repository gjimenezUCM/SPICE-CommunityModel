# Authors: José Ángel Sánchez Martín

import numpy as np
import pandas as pd
# Import math library
import math

from cmSpice.algorithms.similarity.similarityDAO import SimilarityDAO

class SetSimilarity(SimilarityDAO):
    """
    Similarity between two sets of elements.
    """

    def __init__(self,dao,col):
        """Construct of Similarity objects.

        Parameters
        ----------
        dao : dao object class
            DAO which processes and provides the data required by the similarity measure.
        
        """
        super().__init__(dao)
        
        self.col = col

    def distance(self,elemA, elemB):
        
            
        #print(self.data)
        """Method to obtain the distance between two element.

        Parameters
        ----------
        elemA : int
            Id of first element. This id should be in self.data.
        elemB : int
            Id of second element. This id should be in self.data.

        Returns
        -------
        double
            Distance between the two elements.
        """
        
        # Get string separated by ,
        valueA = self.data.loc[elemA][self.col]
        valueB = self.data.loc[elemB][self.col]
        
        # Convert to list
        listA = valueA.split(", ")
        listB = valueB.split(", ")
        listA = list(filter(None, listA))
        listB = list(filter(None, listB))

        # sets
        setA = set(listA)
        setB = set(listB)

        return self.getDistanceBetweenItems(setA, setB)

    def distanceItems(self, setA, setB):
        """
        Method to obtain the distance between two sets.

        Parameters
        ----------
        itemA : int
            First age
        itemB : int
            Second age

        Returns
        -------
        double
            Distance between the two elements.
        """

        # Get intersection
        intersection = setA.intersection(setB)
        union = setA.union(setB)
        
        # Similarity = size intersection / size union
        """
        print("\n")
        print(elemA)
        print(elemB)
        print("\n")
        print(setA)
        print(setB)
        print(intersection)
        print(union)
        print("\n")
        """
        return 1 - (len(intersection) / len(union))

        