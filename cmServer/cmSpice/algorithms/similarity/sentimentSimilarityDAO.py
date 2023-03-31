# Authors: José Ángel Sánchez Martín
import os
import json

import numpy as np

from cmSpice.algorithms.similarity.tableSimilarityDAO import TableSimilarityDAO

class SentimentSimilarityDAO(TableSimilarityDAO):
    
    def distanceValues(self, sentimentsDictA, sentimentsDictB):
        """
        Method to obtain the distance between two valid values given by the similarity measure.

        Parameters
        ----------
        sentimentsDictA : dict
            Keys: String
                Positive, Negative, Neutral
            Values: double
                Confidence Level
        sentimentsDictB : dict
            Keys: String
                Positive, Negative, Neutral
            Values: double
                Confidence Level

        Returns
        -------
        double
            Distance between the two values.
        """
        """
        print("sentiment similarity dao")
        print(sentimentsDictA)
        print(sentimentsDictB)
        print("\n")
        """
        if len(sentimentsDictA) <= 0 or len(sentimentsDictB) <= 0:
            return 1.0
        else:
            sentimentA = max(sentimentsDictA, key=sentimentsDictA.get).lower()
            sentimentB = max(sentimentsDictB, key=sentimentsDictB.get).lower()

            result = super().distanceValues(sentimentA, sentimentB)

            """
            print("result sentiment similarity")
            print(result)
            print("\n")
            """

            return result
        
        
    def dominantValue(self, sentimentsDictA, sentimentsDictB):
        """
        Method to obtain the dominant sentiment for A and B
        Parameters
        ----------
        sentimentsDictA : dict
            Keys: String
                Positive, Negative, Neutral
            Values: double
                Confidence Level
        sentimentsDictB : dict
            Keys: String
                Positive, Negative, Neutral
            Values: double
                Confidence Level

        Returns
        -------
        String
            Dominant sentiment
        """
        if (len(sentimentsDictA) <= 0):
            sentimentA = ""
        else:
            sentimentA = max(sentimentsDictA, key=sentimentsDictA.get).lower()
            
        if (len(sentimentsDictB) <= 0):
            sentimentB = ""
        else:
            sentimentB = max(sentimentsDictB, key=sentimentsDictB.get).lower()
        
        return sentimentA, sentimentB

    def getSimilarityTableName(self):
        return 'sentiment'

