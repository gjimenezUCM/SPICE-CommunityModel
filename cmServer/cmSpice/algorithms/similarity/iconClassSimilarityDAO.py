# Authors: José Ángel Sánchez Martín
import os
from cmSpice.algorithms.similarity.similarityDAO import SimilarityDAO

class IconClassSimilarityDAO(SimilarityDAO):
    
    def __init__(self, dao, similarityFunction):
        """Construct of TaxonomySimilarity objects.

        Parameters
        ----------
        data : pd.DataFrame
            Dataframe where index is ids of elements, columns a list of taxonomy member and
            values contain the number of times that a taxonomy member is in an element.
        """
        super().__init__(dao, similarityFunction)
        self.similarityColumn = similarityFunction['on_attribute']['att_name']

        # Number of similar iconclass themes to consider for the similarity between artworks. 
        self.numberThemes = 2



    def elemLayer(self,elem):
        return len(elem)
    
    def getIconclassParent(self, elemA, elemB):
        return os.path.commonprefix([elemA, elemB])
    
    def distanceItems(self,elemA,elemB):
        """Method to obtain the distance between two taxonomy members.

        Parameters
        ----------
        elemA : object
            Id of first element. This id should be in self.data.
        elemB : object
            Id of second element. This id should be in self.data.

        Returns
        -------
        double
            Similarity between the two taxonomy members.
        """
        
        # Get first common characters 
        commonAncestor = self.getIconclassParent(elemA, elemB)
        maxLayer = max(self.elemLayer(elemA), self.elemLayer(elemB))
        if (maxLayer <= 0):
            sim = 0
        else:
            sim = self.elemLayer(commonAncestor) / maxLayer
            
        return 1 - sim
        
    def iconClassBestMatch(self, elemA, iconClassListB):
        """        
        a) It finds the iconClass elem in iconClassListB with the largest common prefix with elemA (most similar)
        
        Parameters
        ----------
        elemA: String
            Iconclass id belonging to artwork A
        iconClassListB: list
            List of iconclass id belonging to artwork B
        
        Returns
        -------
            longestPrefixElemB: String
                Iconclass id in iconClassListB that is most similar to elemA
        """
        longestPrefix = ""
        longestPrefixElemB = ""
        for elemB in iconClassListB:
            prefix = self.getIconclassParent(elemA, elemB)
            if (len(prefix) > len(longestPrefix) or (len(prefix) == len(longestPrefix) and len(longestPrefixElemB) > len(elemB))):
                longestPrefix = prefix
                longestPrefixElemB = elemB
                
        return longestPrefixElemB

    def iconClassDistance(self, elemA, iconClassListB):
        """
        Computes the distance between an iconClass elem from artwork A and the iconClass elements from artwork B
        
        a) It finds the iconClass elem in iconClassListB with the largest common prefix with elemA and compares it.
        b) If none are found, distance is set to 1.
        
        Parameters
        ----------
        elemA: String
            Iconclass id belonging to artwork A
        iconClassListB: list
            List of iconclass id belonging to artwork B
        
        Returns
        -------
            distance: float
        """
        longestPrefixElemB = self.iconClassBestMatch(elemA, iconClassListB)
        distance = self.getDistanceBetweenItems(elemA,longestPrefixElemB)

        distanceDict = {}
        distanceDict['elemA'] = elemA
        distanceDict['elemB'] = longestPrefixElemB
        distanceDict['distance'] = distance

        return distanceDict

    def distanceValues(self, iconClassListA, iconClassListB):
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
        """
        print("iconclassListA: " + str(iconClassListA))
        print("iconclassListB: " + str(iconClassListB))
        print("\n")
        """
        
        
        # Set largest list to be A and the other B
        if (len(iconClassListB) > len(iconClassListA)):
            iconClassListA, iconClassListB = self.exchangeElements(iconClassListA, iconClassListB)

        # Compare each element of valueA with the element from B with the biggest common prefix
        # If none from B share a common prefix, distance is equal to 1
        self.distanceList = []
        for elemA in iconClassListA:
            distanceDict = self.iconClassDistance(elemA,iconClassListB)
            self.distanceList.append(distanceDict)

        # Take into account only the [numberThemes] lowest distances
        self.distanceList = sorted(self.distanceList, key=lambda d: d['distance']) 
        distanceTotal = 0
        number = min(self.numberThemes, len(self.distanceList))
        number = max(number,1)
        for i in range(number):
            distanceTotal += self.distanceList[i]['distance']
        distanceTotal /= number

        return distanceTotal

#-------------------------------------------------------------------------------------------------------------------------------
#   To calculate dominant value between two values (in order to explain communities)
#-------------------------------------------------------------------------------------------------------------------------------
    
    def dominantValue(self, iconClassListA, iconClassListB):
        dominantValues = []
        artworkA = self.artworkA
        artworkB = self.artworkB
        if (len(iconClassListB) > len(iconClassListA)):
            iconClassListA, iconClassListB = self.exchangeElements(iconClassListA, iconClassListB)
            artworkA, artworkB = self.exchangeElements(self.artworkA, self.artworkB)

        dominantValues.append(self.extractDominantValue(iconClassListA, iconClassListB, artworkA, artworkB))
        dominantValues.append(self.extractDominantValue(iconClassListA, iconClassListB, artworkA, artworkB))

        return dominantValues


    def extractDominantValue(self, iconClassListA, iconClassListB, artworkA, artworkB):
        explainable_iconclassValues = []
        
        
        try:

            number = min(self.numberThemes, len(self.distanceList))
            for i in range(number):
                elemA = self.distanceList[i]['elemA']
                longestPrefixElemB = self.distanceList[i]['elemB']
                commonParent = self.getIconclassParent(elemA, longestPrefixElemB)
                maxLayer = max(self.elemLayer(elemA), self.elemLayer(longestPrefixElemB))
                parentLayer = self.elemLayer(commonParent)
                commonParent = commonParent.split("(")[0]

                if (parentLayer != 0):
                    # New explanation: add information about the iconclassIDs (children) from which this new one (parent) is derived 
                    commonParentDict = {}
                    commonParentDict[commonParent] = {}
                    commonParentDict[commonParent][elemA] = [ artworkA['id'] ]
                    if (longestPrefixElemB not in commonParentDict[commonParent]):
                        commonParentDict[commonParent][longestPrefixElemB] = []
                    commonParentDict[commonParent][longestPrefixElemB].append( artworkB['id'] )

                    explainable_iconclassValues.append(commonParentDict)
            

        except Exception as e:
            print("exception")
            print(e)

        
        return explainable_iconclassValues
    

    
    
    
    
    
    
    
    
    