# Authors: José Ángel Sánchez Martín

from itertools import product
import numpy as np
import importlib
import json
import math

from cmSpice.algorithms.similarity.similarityDAO import SimilarityDAO


class NumberSimilarityDAO (SimilarityDAO):

    def distanceItems(self, valueA, valueB):
        """
        Method to obtain the distance between two valid values given by the similarity measure.
        e.g., sadness vs fear in plutchickEmotionSimilarity

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
        # https://math.stackexchange.com/questions/1481401/how-to-compute-similarity-between-two-numbers
        try:
            valueA = int(valueA)
            valueB = int(valueB)
            
            distance = (abs(valueA - valueB)) / max(valueA,valueB)
            similarity = 1 - distance
            
            """
            print("similarity number: " + str(similarity))
            print("distance number: " + str(distance))
            """
            
            return distance
        except Exception as e:
            print("\n\n\n")
            print(str(e))
            print("number similarity error: valueA: " + str(valueA) + ", valueB: " + str(valueB))
            return 1.0

    # Year: nulls (example: fourth artwork must be considered 0.0)

    def dominantValue(self, valueA, valueB):
        return [str(valueA), str(valueB)]