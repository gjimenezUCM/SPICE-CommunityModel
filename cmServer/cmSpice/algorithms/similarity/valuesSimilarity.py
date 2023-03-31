# Authors: José Ángel Sánchez Martín
from cmSpice.algorithms.similarity.tableSimilarityDAO import TableSimilarityDAO

class ValuesSimilarity(TableSimilarityDAO):

    def __init__(self, dao, similarityFunction):
        """
        Similarity class for moral values specified by the MFT (Moral Foundations Theory)

        Parameters
        ----------
        dao : dao object class
            DAO which processes and provides the data required by the similarity measure.
        similarityFunction: json dict
            Encodes the similarity function parameters (column it is applied to, weight...)
        """
        super().__init__(dao, similarityFunction)

    def getSimilarityTableName(self):
        return "mftHaidt"

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
        distance = self.distanceBetweenLists(valueA, valueB)
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
        mftValueA = elementA.lower().replace(" ", "")
        mftValueB = elementB.lower().replace(" ", "")

        #print("distance between elements values")
        #print("mftvalueA: " + str(mftValueA))
        #print("mftvalueB: " + str(mftValueB))
        #print("\n")

        return self.getDistanceBetweenItems(mftValueA, mftValueB)

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
        return [self.lowestDistancePair[0], self.lowestDistancePair[1]]

    def dominantDistance(self, mftValuesListA, mftValuesListB):
        """
        Method to obtain the distance between the two dominant values encoding the interaction between A and B
        
        Used to explain dissimilar communities

        Parameters
        ----------
        mftValuesListA : dict
            Dict of Plutchik emotions (key: emotion; value: confidence level)
        mftValuesListB : dict
            Dict of Plutchik emotions (key: emotion; value: confidence level)

        Returns
        -------
        double
            Distance
        """
        dominantItemA, dominantItemB = self.dominantInteractionAttribute(mftValuesListA, mftValuesListB)
        return self.getDistanceBetweenItems(dominantItemA, dominantItemB)
        