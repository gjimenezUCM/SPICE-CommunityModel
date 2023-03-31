# Authors: José Ángel Sánchez Martín
from cmSpice.algorithms.similarity.similarityDAO import SimilarityDAO

import pandas as pd
import os

class ColorSimilarity(SimilarityDAO):
    """
    Class to calculate the similarity between two colors
    """
    
    def __init__(self, dao, similarityFunction = {}):
        """
        Construct of ColorSimilarity objects.

        Parameters
        ----------
        data : pd.DataFrame
            Dataframe where index is ids of elements, columns a list of taxonomy member and
            values contain the number of times that a taxonomy member is in an element.
        """
        super().__init__(dao,similarityFunction)

        name = "delta_e_cie2000"
        self.dfDistance = self.loadDeltaSimValuesFromDistFile(name)
        #print("self.dfDistance")
        #print(self.dfDistance.loc[self.dfDistance['c1'] == 'GREEN'])
        #print(self.dfDistance)
        print("\n")

    def loadDeltaSimValuesFromDistFile (self, name):
        """
        Loads distances between colors

        Parameters
        ----------
        name : String
            Csv file with the similarities between colors

        Returns
        -------
        pd.DataFrame
            Pandas Dataframe with the distance between color1 and color2
        """
        #route = os.path.join(os.path.dirname(__file__), f'distanceTables/colorSimilarity/distvalues-{name}.csv')
        route = os.path.join(os.path.dirname(__file__), f'distanceTables/colorSimilarity/distanceMatrix-{name}.csv')
        """
        print("route colors: " + str(route))
        """
        dfDistance = pd.read_csv(route, sep=";") 
        #dfDistance = pd.read_csv(route)
        return dfDistance

    def distanceValues(self, valueA, valueB):
        """
        Distance between two lists of colors

        Parameters
        ----------
        valueA : List
            List of color names (String)
        
        valueB : List
            List of color names (String)

        Returns
        -------
        double
            Distance between the two lists of colors
        """
        
        """
        print("valueA: " + str(valueA))
        print("valueB: " + str(valueB))
        #print(self.dfDistance)
        print("\n\n")
        """
        distance = self.distanceBetweenLists(valueA, valueB)
        return distance

    def distanceItems(self, elementA, elementB):
        """
        Distance between two colors.
        Specialization of the inherited function for calculating distance between list members

        Parameters
        ----------
        elementA : String
            Color name (String)
        
        elementB : String
            Color name (String)

        Returns
        -------
        double
            Distance between the colors
        """
        # Fix color String
        colorA = elementA.upper().replace(" ", "")
        colorB = elementB.upper().replace(" ", "")

        """
        print("colorA: " + str(colorA))
        print("colorB: " + str(colorB))
        
        """

        # Color similarity data doesn't contain the same combination in inverse order. Thus, we check both.
        # It seems like it is sorted alphabetically. Consequently, c1 should be the color with lower value and c2 the one with higher value.
        # However, to make it generic we will check both of them.
        """
        print("self.distance_df")
        print(self.dfDistance)
        print(self.dfDistance.columns)
        print("\n")
        similarityRow_df = self.dfDistance.loc[self.dfDistance['c1'] == colorA]
        print("similarityRow_df")
        print(similarityRow_df)
        print("\n")
        """
        """
        similarityRow_df = self.dfDistance.loc[(self.dfDistance['c1'] == colorA) & (self.dfDistance['c2'] == colorB)]
        if (similarityRow_df.empty):
            similarityRow_df = self.dfDistance.loc[(self.dfDistance['c1'] == colorB) & (self.dfDistance['c2'] == colorA)]
        """
        """
        print("columns")
        print(self.dfDistance.columns)
        print("\n")
        """
        if (colorA in self.dfDistance.columns and colorB in self.dfDistance.columns):
            similarityRow_df = self.dfDistance.loc[(self.dfDistance['c1'] == colorA)]
            
            """
            print("similarityRow_df")
            print(similarityRow_df)
            print("\n")
            
            print("similarity row value")
            print(similarityRow_df['simvalue'].item())
            print("\n")
            number = 5.0 + similarityRow_df['simvalue'].item()
            print("number")
            print(number)
            print("\n")
            """
            if (similarityRow_df.empty):
                return 1.0
            else:
                # The .csv contains similarity between colors (not distance)
                return 1 - similarityRow_df[colorB].item()
        else:
            return 1.0

#-------------------------------------------------------------------------------------------------------------------------------
#   To calculate dominant value
#-------------------------------------------------------------------------------------------------------------------------------
       
    def dominantValue(self, valueA, valueB):
        dominantValues = []
        # dominantValues.append(self.getDominantList(self.lowestDistancePair[0], self.artworkA))
        # dominantValues.append(self.getDominantList(self.lowestDistancePair[1], self.artworkB))

        dominantValues.append(self.getDominantList(valueA, self.artworkA))
        dominantValues.append(self.getDominantList(valueB, self.artworkB))

        return dominantValues

        """
        return valueA

        distance = self.distanceValues(valueA, valueB)
        return {self.lowestDistancePair[0]: self.artworkA['id'].to_list()[0]}
        """

    def getDominantList(self, value, artwork):
        dominantList = []
        for valueElement in value:
            value = valueElement.upper().replace(" ", "")
            
            valueDict = {}
            valueDict[value] = {}
            valueDict[value][value] = [ artwork['id'] ]

            dominantList.append(valueDict)

        return dominantList

    def getDominantListMostRepresentativeColour(self, value, artwork):
        dominantList = []
        value = value.upper().replace(" ", "")
        valueDict = {}
        valueDict[value] = {}
        valueDict[value][value] = [ artwork['id'] ]

        dominantList.append(valueDict)

        return dominantList



