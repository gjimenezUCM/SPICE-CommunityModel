# Authors: José Ángel Sánchez Martín
from cmSpice.algorithms.similarity.valuesSimilarity import ValuesSimilarity

import itertools

class SameValuesDictSimilarity(ValuesSimilarity):
    """
    Handles similarity between values when the data is given by a dict
    """
    def distanceItems(self, valuesListA, valuesListB):
        """
        Method to obtain the distance between two ages.

        Parameters
        ----------
        valuesListA : List
            First age
        valuesListB : List
            Second age

        Returns
        -------
        double
            Distance between the two elements.
        """
        if (len(valuesListA) <= 0 or len(valuesListB) <= 0):
            return 1.0
        elif (valuesListA[0] != valuesListB[0]):
            return 1.0
        else: 
            self.lowestDistancePair = [valuesListA[0], valuesListA[0]]
            return 0.0
    
    def distanceValues(self, valueA, valueB):
        """
        Method to obtain the distance between two lists of moral values. Only mft values are considered.

        Parameters
        ----------
        elemA : list
            Values list: includes mft and folk values.
            e.g.:
                "Values": [
                    "mft:Fairness",
                    "folk:Helping",
                    "folk:Impartial",
                    "folk:Understanding",
                    "mft:Care",
                    "folk:Novelty",
                    "bhv:Benevolence",
                    "folk:Intuitive"
                ], 
        elemB : list
            Values list: includes mft and folk values. 
        Returns
        -------
        double
            Distance between the two elements.
        """
        # Sort dict by confidence score
        sorted_valuesDictA = {k: v for k, v in sorted(valueA.items(), key=lambda item: item[1], reverse=True)}
        sorted_valuesDictB = {k: v for k, v in sorted(valueB.items(), key=lambda item: item[1], reverse=True)}

        # Keep "numValues" of them
        numValues = 1
        valuesListA = list(dict(itertools.islice(sorted_valuesDictA.items(),numValues)).keys())
        valuesListB = list(dict(itertools.islice(sorted_valuesDictB.items(),numValues)).keys())

        return self.getDistanceBetweenItems(valuesListA, valuesListB)

    def dominantValue(self, mftValuesListA, mftValuesListB):
        """
        Method to obtain the dominant value for A and B
        Parameters
        ----------
        mftValuesListA : List <String>
            
        mftValuesListB : List <String>

        Returns
        -------
        String, String
            Predominant valueA, Predominant valueB (pair of most similar ones)
        """
        return self.lowestDistancePair[0], self.lowestDistancePair[1]
        