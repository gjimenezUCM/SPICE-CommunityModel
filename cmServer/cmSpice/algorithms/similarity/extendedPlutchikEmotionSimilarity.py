# Authors: José Ángel Sánchez Martín
import os

from cmSpice.algorithms.similarity.extendedPlutchikEmotionSimilarityDAO import ExtendedPlutchikEmotionSimilarityDAO

import itertools

"""
Extension of the Plutchik wheel of emotions to include the second level of emotions in addition to the basic ones
"""

"""
Use at least two emotions to perform the similarity
"""
class ExtendedPlutchikEmotionSimilarity(ExtendedPlutchikEmotionSimilarityDAO):
    
    def distanceValues(self, emotionsDictA, emotionsDictB):
        """
        Method to obtain the distance between two combination of emotions
        
        a) Get common emotions.
        b) For the different emotions (diffA, diffB), compute distance between each element in diffA and the most similar emotion in diffB

        Parameters
        ----------
        emotionsDictA : dict
            Dict of Plutchik emotions (key: emotion; value: confidence level)
        emotionsDictB : dict
            Dict of Plutchik emotions (key: emotion; value: confidence level)

        Returns
        -------
        double
            Distance between the two combination of emotions.
        """
        if (isinstance(emotionsDictA, dict) == False or isinstance(emotionsDictB, dict) == False):
            self.lowestDistancePair = ["",""]
            return 1.0 

        emotionsDictA = dict([(x.replace("emotion:",""), y) for x, y in emotionsDictA.items() ])
        emotionsDictB = dict([(x.replace("emotion:",""), y) for x, y in emotionsDictB.items() ])
        
        if (len(emotionsDictA) <= 0 or len(emotionsDictB) <= 0):
            return 1.0
        else:

            # Sort emotions by value
            sorted_emotionsDictA = {k: v for k, v in sorted(emotionsDictA.items(), key=lambda item: item[1], reverse=True)}
            sorted_emotionsDictB = {k: v for k, v in sorted(emotionsDictB.items(), key=lambda item: item[1], reverse=True)}
        
            numValues = 3
            numValues = 1
            emotionsListA = list(dict(itertools.islice(sorted_emotionsDictA.items(),numValues)).keys())
            emotionsListB = list(dict(itertools.islice(sorted_emotionsDictB.items(),numValues)).keys())

            """
            print("emotionsListA: " + str(emotionsListA))
            print("emotionsListB: " + str(emotionsListB))
            print("before calling distance between lists")
            print("\n")
            """

            distance = self.distanceBetweenLists(emotionsListA, emotionsListB)

            """
            print("emotion similarity")
            print("emotionsDictA")
            print(emotionsDictA)
            print("emotionsDictB")
            print(emotionsDictB)
            print("sorted A")
            print(sorted_emotionsDictA)
            print("emotionsListA: " + str(emotionsListA))
            print("emotionsListB: " + str(emotionsListB))
            print("distance between lists: " + str(distance))
            print("\n")
            """

            return distance

    def distanceListElements(self, elementA, elementB):
        """
        Distance between two MFT_values.
        Specialization of the inherited function for calculating distance between list members

        Parameters
        ----------
        elementA : String
            MFT_Value name (String)
        
        elementB : String
            MFT_Value name (String)

        Returns
        -------
        double
            Distance between the MFT_Values
        """
        
        # Fix value String
        emotionA = elementA.lower().replace(" ", "")
        emotionB = elementB.lower().replace(" ", "")
        
        return self.getDistanceBetweenItems(emotionA, emotionB)

    def dominantValue(self, emotionsDictA, emotionsDictB):
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
        
        """
        emotionsDictA = dict([(x.replace("emotion:",""), y) for x, y in emotionsDictA.items() if x.startswith('emotion:')])
        emotionsDictB = dict([(x.replace("emotion:",""), y) for x, y in emotionsDictB.items() if x.startswith('emotion:')])
        """
        return [self.lowestDistancePair[0], self.lowestDistancePair[1]]

    
    
    