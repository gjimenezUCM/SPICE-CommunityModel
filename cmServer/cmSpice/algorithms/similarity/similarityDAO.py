# Authors: José Ángel Sánchez Martín
from itertools import product
import numpy as np
import importlib
import json

from itertools import combinations
from itertools import combinations_with_replacement

import math

import traceback
from cmSpice.logger.logger import getLogger

class SimilarityDAO:
    """Class to define the functions to be implemented to calculate
    the similarity between elements.
    """
    
    def __init__(self, dao, similarityFunction = {}):
        """Construct of Similarity objects.

        Parameters
        ----------
        dao : dao object class
            DAO which processes and provides the data required by the similarity measure.
        
        """
        self.dao = dao
        self.similarityFunction = similarityFunction
        if (len(similarityFunction) > 0):
            self.similarityColumn = similarityFunction['on_attribute']['att_name']
        else:
            self.similarityColumn = ""
            
        self.data = self.dao.getPandasDataframe()

        # To explain communities (dominant values in list attributes)
        self.lowestDistancePair = ["",""]

        self.elemA = ""
        self.elemB = ""

    """
    Distance functions:

    From more specific to more generic
    """
    def distanceItems(self, itemA, itemB):
        """
        Method to obtain the distance between two valid items of the similarity measure 
        Example: emotionSimilarity (joy, anger, sadness...)

        Basic distance function: all similarity measures inheriting from similarityDAO must
        implement this function

        Parameters
        ----------
        itemA : object
            First valid element we can use the similarity measure on
        valueB : object
            Second valid element we can use the similarity measure on

        Returns
        -------
        double
            Distance between the two items.
        """
        return 1.0

    def getDistanceBetweenItems(self, itemA, itemB):
        """
        Method to call additional logic after the function overwrite of "distanceItems()" in the children classes
        
        Basic distance function: ultimately called by any distance function in any similarity measure

        Parameters
        ----------
        itemA : object
            First valid element we can use the similarity measure on
        valueB : object
            Second valid element we can use the similarity measure on

        Returns
        -------
        double
            Distance between the two values.
        """
        if (self.isNaN(itemA) or self.isNaN(itemB)):
            return 1.0
        else:
            distance = self.distanceItems(itemA, itemB)
            distance = self.dissimilarFlag(distance)

            return distance

    def distanceValues(self, valueA, valueB):
        """
        Method to obtain the distance between two pandas cell valiues [row, similarityColumn]

        Defaults to getDistanceBetweenItems(self, itemA, itemB) if it is not overwritten by the 
        similarity measure child

        Parameters
        ----------
        valueA : object
            Value of first element corresponding to elemA in self.data
            e.g: GAM emotions: {"serenity": 1.0, "anger": 0.8}
        valueB : object
            Value of first element corresponding to elemB in self.data

        Returns
        -------
        double
            Distance between the two values.
        """
        return self.getDistanceBetweenItems(valueA, valueB)

    def distance(self,elemA, elemB):
        """
        Method to obtain the distance between two pandas cell values

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
        try:

            valueA = self.data.loc[elemA][self.similarityColumn]
            valueB = self.data.loc[elemB][self.similarityColumn]

            self.elemA = elemA
            self.elemB = elemB

            if (self.isNaN(valueA) or self.isNaN(valueB)):
                return 1.0
            else:
                return self.distanceValues(valueA, valueB)

        
        except Exception as e:

            logger = getLogger(__name__)
            logger.error(traceback.format_exc())

            return 1.0
    
    """
    Distance functions:

    Distance between lists
    """

    def isNaN(self, value):
        #return isinstance(value, float) and math.isnan(value)
        return value != value

#-------------------------------------------------------------------------------------------------------------------------------
#   To calculate similarity between two lists of different length
#-------------------------------------------------------------------------------------------------------------------------------
    
    def distanceListElements(self, elementA, elementB):
        return self.getDistanceBetweenItems(elementA, elementB)

    def mostSimilarListElement(self, listElementA, listB):
        """
        Gets the most similar element to another among the members of a list

        """
        """
        #print("checking most similar list element")
        #print(listElementA)
        #print(listB)
        #print("\n")
        """

        listElementB = ""
        lowestDistance = 1.0
        for listElement in listB:
            distance = self.distanceListElements(listElementA,listElement)
            if (distance <= lowestDistance):
                lowestDistance = distance
                listElementB = listElement
        
        return listElementB

    def distanceBetweenLists(self, listA, listB):
        """
        Auxiliary function to set the comparison between two lists of different length

        """
        similarityListA = listA
        similarityListB = listB

        if (len(listB) > len(listA)):
            similarityListA = listB
            similarityListB = listA
        elif (len(listA) == len(listB) and self.elemA > self.elemB):
            similarityListA = listB
            similarityListB = listA


        #print("distance between lists")
        #print("similarityListA: " + str(similarityListA))
        #print("similarityListB: " + str(similarityListB))
        #print("\n")

        # Store pair (elementA, elementB) with the most similarity to work as the dominantAttribute
        self.lowestDistancePair = ["",""]
        self.lowestDistance = 1.0

        # Calculate distance
        totalDistance = 0
        if (len(similarityListB) > 0):
            for listElementA in similarityListA:
                listElementB = self.mostSimilarListElement(listElementA, similarityListB)
                distance = self.distanceListElements(listElementA,listElementB)
                totalDistance += distance

                if (distance < self.lowestDistance):
                    self.lowestDistancePair = [listElementA, listElementB]
                    self.lowestDistance = distance
                #print("elementA: " + str(listElementA))
                #print("elementB: " + str(listElementB))
                #print("distance: " + str(distance))
                #print("\n")
            totalDistance = totalDistance / len(similarityListA)
        else:
            totalDistance = 1.0

        if (similarityListA != listA):
            listElementA = self.lowestDistancePair[0]
            listElementB = self.lowestDistancePair[1]
            self.lowestDistancePair = [listElementB, listElementA]

        return totalDistance

    
    
    """
    Other functions:
    """

    def dissimilarFlag(self, distance):
        """
        Method to apply [dissimilar] similarity measures

        It is always called by getDistanceBetweenItems(self, itemA, itemB)

        Parameters
        ----------
        distance : double
            Original distance obtained by applying the similarity measure normally.

        Returns
        -------
        double
            New distance between the two elements.
        """


        """
        #print("dissimilar flag function")
        #print("distance")
        #print(distance)
        #print("self similarity function")
        #print(self.similarityFunction)
        """

        if ('dissimilar' in self.similarityFunction and self.similarityFunction['dissimilar'] == True):
            ##print("apply dissimilar to " + self.similarityFunction["on_attribute"]['att_name'])
            distance = 1 - distance
        """
        #print("distance")
        #print(distance)
        #print("\n")
        """

        return distance
        

    

    def similarity(self,elemA, elemB):
        """Method to obtain the similarity between two element.

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
        pass

    def matrix_distance(self):
        """Method to calculate the matrix of distance between all element included in data.

        Returns
        -------
        np.array
            Matrix that contains all similarity values.
        """
        users = self.data.index
        pairs = product(range(len(users)), repeat=2)
        
        # This checks 0,1 and 1,0
        # Change it to only check 0,1 and assign the same to 1,0
        matrix = np.zeros((len(users), len(users)))
        for p in pairs:
            dist = self.distance(users[p[0]], users[p[1]])
            matrix[p[0], p[1]] = dist
            """
            #print("user1: " + str(users[p[0]]))
            #print("user2: " + str(users[p[1]]))
            #print("distance: " + str(dist))
            """


        # Reduce the matrix to 2 decimals
        matrix = np.round(matrix,2)
        
        self.distanceMatrix = matrix

        return matrix

    
        
    def updateDistanceMatrix(self, userIds, distanceMatrix):
        """
        Method to update the distance matrix with the new elements included in the data.
            
        Parameters
        ----------
            distanceMatrix : np.ndarray
                Previous distance matrix 
            userIds : list
                Includes the ids of the users to update.

        Returns
        -------
            np.ndarray
                Matrix that contains all distance values.
        """
        #print("update distance matrix")
        # https://www.geeksforgeeks.org/python-make-pair-from-two-list-such-that-elements-are-not-same-in-pairs/
        # https://www.statology.org/numpy-add-column/
        # https://stackoverflow.com/questions/8486294/how-do-i-add-an-extra-column-to-a-numpy-array
        # https://www.statology.org/pandas-get-index-of-row/
        # https://www.geeksforgeeks.org/python-program-to-get-all-pairwise-combinations-from-a-list/
        indexes = self.data.index
        updateIndexes = self.data[self.data['userid'].isin(userIds)].index #.tolist()
        pairs = product(indexes,updateIndexes)
        
        ##print(self.data)
        
        matrix = np.zeros((len(indexes), len(indexes)))
        matrix[0:distanceMatrix.shape[0],0:distanceMatrix.shape[1]] = distanceMatrix
        
        ##print(matrix)
        
        for p in pairs:
            """
            #print("\n")
            #print("pairs")
            #print(p[0])
            #print(p[1])
            #print("\n")
            """
            dist = self.distance(p[0],p[1])
            matrix[p[0], p[1]] = dist
            matrix[p[1],p[0]] = dist
        
        
        
        # Reduce the matrix to 2 decimals
        matrix = np.round(matrix,2)
        self.distanceMatrix = matrix
        
        #print(matrix)
        
        return matrix


    def matrix_similarity(self):
        """Method to calculate the matrix of similarity between all element included in data.

        Returns
        -------
        np.ndarray
            Matrix that contains all similarity values.
        """
        users = self.data.index
        pairs = product(range(len(users)), repeat=2)

        matrix = np.zeros((len(users), len(users)))
        for p in pairs:
            dist = self.similarity(users[p[0]], users[p[1]])
            matrix[p[0], p[1]] = dist

        return matrix
    

#-------------------------------------------------------------------------------------------------------------------------------
#   Auxiliar functions
#-------------------------------------------------------------------------------------------------------------------------------

    def initializeFromPerspective(self, dao, similarityFunction):
        similarityName = similarityFunction['sim_function']['name']
        similarityFile = "cmSpice.algorithms.similarity." + similarityName[0].lower() + similarityName[1:]
        similarityModule = importlib.import_module(similarityFile)
        similarityClass = getattr(similarityModule,similarityName)
        similarityMeasure = similarityClass(dao,similarityFunction['sim_function'])
        
        return similarityMeasure
        
    def dominantValueType(self):
        if (len(self.similarityFunction) <= 0):
            return "String"
        else:
            return self.similarityFunction['on_attribute']['att_type'].lower()
    
    def exchangeElements(self, elemA, elemB):
        aux = elemA
        elemA = elemB
        elemB = aux
        
        return elemA, elemB

    


    
    def exportDistanceMatrix(self, distanceMatrix, exportFile):
        distanceMatrix = distanceMatrix.tolist()
        
        with open(exportFile, "w") as outfile:
            json.dump(distanceMatrix, outfile, indent=4)    
    
    def importDistanceMatrix(self, importFile):
        with open(importFile, 'r', encoding='utf8') as f:
            distanceMatrix = json.load(f)
                
        return np.asarray(distanceMatrix)
        


        
#-------------------------------------------------------------------------------------------------------------------------------
#   To calculate dominant value in interaction attributes (always dict)
#-------------------------------------------------------------------------------------------------------------------------------
       
    def dominantInteractionAttribute(self, dictA, dictB):
        """
        Method to obtain the dominant sentiment for A and B
        Parameters
        ----------
        dictA : dict
            Keys: String
            Values: double
                Confidence Level
        dictB : dict
            Keys: String

            Values: double
                Confidence Level

        Returns
        -------
        String
            Dominant key
        """
        keyA = ""
        keyB = ""

        if (isinstance(dictA, dict)):
            if (len(dictA) <= 0):
                keyA = ""
            else:
                keyA = max(dictA, key=dictA.get).lower()
                
            if (len(dictB) <= 0):
                keyB = ""
            else:
                keyB = max(dictB, key=dictB.get).lower()
        elif (isinstance(dictA, list)):
            if (len(dictA) > 0):
                keyA = dictA[0]
            if (len(dictB) > 0):
                keyA = dictB[0]
        
        return keyA, keyB
    
#-------------------------------------------------------------------------------------------------------------------------------
#   To calculate dominant value between two values (in order to explain communities)
#-------------------------------------------------------------------------------------------------------------------------------
    
    def dominantElemValue(self, elemA, elemB, idColumn = 'id'):
        # Get artwork information
        if (idColumn != 'index'):
            #print("dominant elem value " + str(idColumn))
            self.artworkA = self.data.loc[ self.data[idColumn] == elemA ]
            self.artworkB = self.data.loc[ self.data[idColumn] == elemB ]

            #valueA = self.data.loc[elemA][self.similarityColumn].to_list()[0]
            #valueB = self.data.loc[elemB][self.similarityColumn].to_list()[0]
            valueA = self.artworkA[self.similarityColumn].to_list()[0]
            valueB = self.artworkB[self.similarityColumn].to_list()[0]
        else:
            #print("dominant elem value 2 " + str(idColumn))
            self.artworkA = self.data.loc[elemA]
            self.artworkB = self.data.loc[elemB]

            valueA = self.artworkA[self.similarityColumn]
            valueB = self.artworkB[self.similarityColumn]

            """
            print("artworkA: " + str(self.artworkA))
            print("artworkB: " + str(self.artworkB))
            print("valueA: " + str(valueA))
            print("valueB: " + str(valueB))
            print("\n")
            """

        # Check NaN
        if (self.isNaN(valueA) or self.isNaN(valueB)):
            return ['','']
        else:
            return self.dominantValue(valueA,valueB)
        
    def dominantValue(self, valueA, valueB):
        keyA = ""
        keyB = ""

        if self.similarityColumn == 'id':
            return [{valueA: self.artworkA['id']}, {valueB: self.artworkB['id']}]
        elif (isinstance(valueA, dict) and isinstance(valueB, dict)):
            if (len(valueA) > 0 and len(valueB) > 0):
                emotionsListA = [key for key, value in valueA.items() if value == max(valueA.values())]
                emotionsListB = [key for key, value in valueB.items() if value == max(valueB.values())]

                intersectionList = list(set(emotionsListA) & set(emotionsListB))
                if (len(intersectionList) > 0):
                    keyA = intersectionList[0]
                    keyB = intersectionList[0]
                else:
                    keyA = emotionsListA[0]
                    keyB = emotionsListB[0]

            return [keyA, keyB]
        elif (isinstance(valueA, list)):
            if (len(valueA) > 0):
                keyA = valueA[0]
            if (len(valueB) > 0):
                keyA = valueB[0]

            return [keyA, keyB]

        else:

            return [str(valueA), str(valueB)]

    def dominantValueColumn(self, name = ""):
        """
        Column name associated to dominant values

        Parameters
        ----------
        name: String
            Suffix of the column name

        Returns
        -------
        String
            Column name
        """
        if (name == ""):
            name = self.similarityColumn
        return name + 'DominantInteractionGenerated'
        return "dominantValue_" + name


    def dominantDistance(self, dominantItemA, dominantItemB):
        """
        Method to obtain the distance between the two dominant items encoding the interaction between A and B
        
        Used to explain dissimilar communities

        Parameters
        ----------
        dominantItemA : object

        dominantItemB : object
            Dict of Plutchik emotions (key: emotion; value: confidence level)

        Returns
        -------
        double
            Distance
        """
        return 1.0


#-------------------------------------------------------------------------------------------------------------------------------
#   Optimize calculations
#-------------------------------------------------------------------------------------------------------------------------------
    
    def matrix_distance_explanation(self):
        """
        Method to calculate the matrix of distance and dominant values (for explanations) between all element included in data.

        Returns
        -------
        distanceMatrix: np.array
            Matrix that contains all similarity values.
        dominantValueMatrix: np.array
            Matrix that contains all dominant values used for community explanation
        
        """
        print("matrix distance explanation")
        users = self.data.index
        pairs = combinations_with_replacement(range(len(users)), r=2)

        # This checks 0,1 and 1,0
        # Change it to only check 0,1 and assign the same to 1,0
        distanceMatrix = np.zeros((len(users), len(users)))
        dominantValueMatrix = np.zeros((len(users), len(users))).tolist()
        """
        print("dominantValueMatrix")
        print(type(dominantValueMatrix))
        print(dominantValueMatrix)
        print("\n")
        """

        for p in pairs:
            """
            print("elems")
            print(p[0])
            print(p[1])
            print("\n")
            """
            
            #dist = self.distance(users[p[0]], users[p[1]])
            dist = self.distance(p[0], p[1])

            distanceMatrix[p[0], p[1]] = dist
            distanceMatrix[p[1], p[0]] = dist

            #dominantValues = self.dominantElemValue(users[p[0]], users[p[1]])
            dominantValues = self.dominantElemValue(p[0], p[1], idColumn = 'index')

            dominantValueMatrix[p[0]][p[1]] = dominantValues[0]
            dominantValueMatrix[p[1]][p[0]] = dominantValues[1]


            """
            #print("user1: " + str(users[p[0]]))
            #print("user2: " + str(users[p[1]]))
            #print("distance: " + str(dist))
            """


        print("distance matrix")
        print(distanceMatrix)
        print("\n")
        print("dominantValueMatrix")
        print(dominantValueMatrix)
        print("\n")


        # Reduce the distanceMatrix to 2 decimals
        distanceMatrix = np.round(distanceMatrix,2)
        
        self.distanceMatrix = distanceMatrix
        self.dominantValueMatrix = dominantValueMatrix

        return distanceMatrix, dominantValueMatrix

