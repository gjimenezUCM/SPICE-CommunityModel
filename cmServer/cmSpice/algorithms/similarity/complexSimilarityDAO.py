# Authors: José Ángel Sánchez Martín
from cmSpice.algorithms.similarity.similarityDAO import SimilarityDAO

import numpy as np
from cmSpice.dao.dao_db_artworkDistanceMatrixes import DAO_db_artworkDistanceMatrixes

class ComplexSimilarityDAO(SimilarityDAO):

    def validatePerspective(self, similarityDict):
        """
        Validates if the perspective and the data are compatible.
        If not, the Community Model aborts and an informative error message is displayed to the user

        Parameters
        ----------
        similarityDict : dict
            Perspective JSON object encoding the artwork similarity measures
        """
        #for artworkSimilarity in self.perspective['similarity_functions']:
        for artworkSimilarity in similarityDict:
            attribute = artworkSimilarity['sim_function']['on_attribute']['att_name']
            if ('name' not in artworkSimilarity["sim_function"]):
                raise NameError('Similarity measure was not provided for ' + str(attribute))
            if (attribute not in self.data.columns):
                raise NameError("Data doesn't include the attribute " + str(attribute) + " encoded in the perspective")

    def __init__(self,dao,similarityDict):
        """Construct of Similarity objects.

        Parameters
        ----------
        dao : dao to obtain data from database
        similarityDict: dictionary
            Dictionary with keys (similarity measure classes) and values (weight of that similarity measure)
        
        """
        super().__init__(dao)

        self.validatePerspective(similarityDict)
        
        # self.similarityDict = {}
        # for similarityFunction in similarityDict:
        #     similarityMeasure = self.initializeFromPerspective(dao,similarityFunction)
        #     self.similarityDict[similarityMeasure] = similarityFunction['sim_function']

        self.similarityDict = {}
        self.similarityMeasureDict = {}
        for similarityFunction in similarityDict:        
            similarityMeasure = self.initializeFromPerspective(dao,similarityFunction)
            self.similarityDict[similarityMeasure] = similarityFunction['sim_function']

            attributeName = similarityFunction['sim_function']['on_attribute']['att_name']
            self.similarityMeasureDict[attributeName] = similarityMeasure
        

    def getSimilarityMeasuresDict(self):
        """
        Get similarity measures used by this one

        Parameters
        ----------


        Returns
        -------



        """
        return self.similarityMeasureDict


    def distance(self,elemA, elemB):
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
        complexDistance = 0
        complexWeight = 0
        for similarity, similarityFunction in self.similarityDict.items():
            weight = similarityFunction.get('weight',0.5)
            
            simDistance = similarity.distance(elemA,elemB)

            """
            print("similarity")
            print(similarity)
            print("elemA")
            print(elemA)
            print("elemB")
            print(elemB)
            """
            
            """
            # Create a column in self.data with the dominant value
            dominantValue = similarity.dominantElemValue(elemA, elemB, idColumn = 'index')
            
            print("dominant value")
            print(dominantValue)
            print("\n")
            """
            
            """
            print("similarity: " + str(similarity))
            print("similarityFunction: " + str(similarityFunction))
            print("elemA: " + str(self.data.loc[elemA]['userid']))
            print("elemB: " + str(self.data.loc[elemB]['userid']))
            print("sim distance: " + str(simDistance))
            print("\n")
            """
            
            # Different mode (return 1 - originalDistance)
            # Already done at the time the similarity is calculated
            #simDistance = similarity.dissimilarFlag(simDistance)
            simDistance2 = simDistance * weight
            
            complexDistance += simDistance2
            complexWeight = complexWeight + weight 
            
        # print("complexDistance: " + str(complexDistance))
        
        complexDistance = complexDistance / complexWeight
        
        # print("complexDistance: " + str(complexDistance))
        # print("\n")
        
        return complexDistance

#-------------------------------------------------------------------------------------------------------------------------------
#   Optimize calculations
#-------------------------------------------------------------------------------------------------------------------------------
    
    def matrix_distance(self):
        return self.matrix_distance_explanation()

    def matrix_distance_explanation(self):
        #print("matrix distance explanation complexSimilarity")

        # Calculate final distanceMatrix
        users = self.data.index
        complexWeight = 0
        complexDistanceMatrix = np.zeros((len(users), len(users)))

        """
        print("complexDistanceMatrix")
        print(complexDistanceMatrix)
        print("\n")
        """

        # For each similarity measure, get distanceMatrix and dominantValues associated
        for similarity, similarityFunction in self.similarityDict.items():
            # Import distance matrix, dominantValueMatrix
            distanceMatrix, dominantValueMatrix = self.computeSimilarityMatrixes(similarity, similarityFunction)

            """
            print(distanceMatrix)
            print(dominantValueMatrix)
            print("\n")
            """

            # Save distanceMatrix, dominantValueMatrix in the database
            self.saveDatabaseDistanceMatrix(similarityFunction, distanceMatrix, dominantValueMatrix)

            # Update complex distance matrix
            weight = similarityFunction.get('weight',0.5)
            complexWeight = complexWeight + weight 
            complexDistanceMatrix += (distanceMatrix * weight)

            """
            print("complexDistanceMatrix")
            print(complexDistanceMatrix)
            print("\n")
            """

            # Update self.data with the information from dominantValueMatrix
            dominantValueColumn = similarity.dominantValueColumn()
            self.data[ dominantValueColumn ] = dominantValueMatrix

            """
            print("check dominant value column")
            print(self.data[['userid', dominantValueColumn]])
            print("\n")
            """


        complexDistanceMatrix /= complexWeight

        """
        print("final complexDistanceMatrix")
        print(complexDistanceMatrix)
        print("\n")
        """

        self.distanceMatrix = complexDistanceMatrix

        return complexDistanceMatrix

    def saveDatabaseDistanceMatrix(self, similarity, distanceMatrix, dominantValueMatrix):
        print("save database matrix")
        databaseObject = {}
        databaseObject['attribute'] = similarity['on_attribute']['att_name']
        databaseObject['similarity'] = similarity['name']
        if ('Beliefs.beliefJ' in self.data.columns):
            databaseObject['index'] = self.data['userid'].tolist()
        else:
            databaseObject['index'] = self.data['id'].tolist()
        databaseObject['distanceMatrix'] = distanceMatrix.tolist()
        databaseObject['dominantValueMatrix'] = dominantValueMatrix

        print("save it")

        daoArtworkDistanceMatrixes = DAO_db_artworkDistanceMatrixes()
        daoArtworkDistanceMatrixes.updateDistanceMatrix(databaseObject)


        print("end save database matrix")
        print("\n")

    def computeSimilarityMatrixes(self, similarity, similarityFunction):
        attribute = similarityFunction['on_attribute']['att_name']
        similarityName = similarityFunction['name']

        daoArtworkDistanceMatrixes = DAO_db_artworkDistanceMatrixes()
        databaseObject = daoArtworkDistanceMatrixes.getArtworkDistanceMatrix(attribute, similarityName)
        print("compute similarity matrixes")
        print(len(databaseObject))
        print("\n")
        print(attribute)
        print(similarityName)
        print("end compute similarity matrixes")
        print("\n")
        
        # For now, if self.data has more/less artworks than the cached version, recompute it.
        # Later, an update will be done to just recompute the differences between the new data and the cached version
        if (len(databaseObject) > 0 and len(self.data) == len(databaseObject['distanceMatrix'])):
            print("load precomputed distance matrix")
            distanceMatrix = np.asarray(databaseObject['distanceMatrix'])
            dominantValueMatrix = databaseObject['dominantValueMatrix']
        else:
            print("similarity measure is not in database")
            print(similarity)
            print("\n")

            distanceMatrix, dominantValueMatrix = similarity.matrix_distance_explanation()

        return distanceMatrix, dominantValueMatrix
