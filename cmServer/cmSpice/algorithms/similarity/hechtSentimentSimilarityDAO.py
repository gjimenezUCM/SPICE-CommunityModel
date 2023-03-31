

import os
from inspect import getsourcefile
#from os.path import abspath, dirname

import numpy as np

from cmSpice.dao.dao_csv import DAO_csv
from cmSpice.algorithms.similarity.tableSimilarityDAO import TableSimilarityDAO

class HechtSentimentSimilarityDAO(TableSimilarityDAO):


    
    def getSimilarityTable(self):
        dao_csv = DAO_csv(os.path.dirname(os.path.abspath(getsourcefile(lambda:0))) + "/distanceTables/" + "sentiment" + ".csv")
        self.similarityTable = dao_csv.getPandasDataframe().set_index('Key')

    def distanceValues(self, emotionsA, emotionsB):
        """
        Method to obtain the distance between two combination of emotions
        
        Compute distance between the first emotion in each list
        
        Parameters
        ----------
        emotionsA : String
            Emotions separated by ;
        emotionsB : String
            Emotions separated by ;

        Returns
        -------
        double
            Distance between the two combination of emotions.
        """
        if (isinstance(emotionsA, str) == False or isinstance(emotionsB, str) == False):
            return 1.0
            
        emotionA = emotionsA.split(";")[0].lower()
        emotionB = emotionsB.split(";")[0].lower()
        
        return super().distanceValues(emotionA, emotionB)

    def dominantInteractionAttribute(self, emotionsA, emotionsB):
        """
        Method to obtain the dominant value in each combination of emotions
        
        Parameters
        ----------
        emotionsDictA : dict
            Dict of Plutchik emotions (key: emotion; value: confidence level)
        emotionsDictB : dict
            Dict of Plutchik emotions (key: emotion; value: confidence level)

        Returns
        -------
        String
            Dominant emotion for A and B
        """

        if (isinstance(emotionsA, str) == False or isinstance(emotionsB, str) == False):
            return "", ""

        emotionA = emotionsA.split(";")[0].lower()
        emotionB = emotionsB.split(";")[0].lower()

        return [emotionA, emotionB]

    def dominantValue(self, emotionsA, emotionsB):     
        return self.dominantInteractionAttribute(emotionsA, emotionsB) 
        

            