# Authors: José Ángel Sánchez Martín
import os
import json
import pandas as pd

import numpy as np

from cmSpice.algorithms.similarity.similarityDAO import SimilarityDAO
from cmSpice.algorithms.similarity.complexSimilarityDAO import ComplexSimilarityDAO
from cmSpice.dao.dao_json import DAO_json
from cmSpice.utils.dataLoader import DataLoader
from cmSpice.utils.artworksLoader import ArtworkLoader

import statistics
from statistics import mode

from cmSpice.dao.dao_db_interactionDistances import DAO_db_interactionDistances


from itertools import combinations
from itertools import combinations_with_replacement

import traceback
from cmSpice.logger.logger import getLogger



class InteractionSimilarityDAO(SimilarityDAO):
    """
    Class to compute the interaction similarity between two users
    
    a) It computes the distanceMatrix between the objects the users interacted with (interaction objects (IO))
    b) For each IO userA interacted with, it gets the IO userB interacted with most similar to it.
    c) It computes the similarity between interaction attributes on these two IOs (e.g., emotions associated to IO(A) vs emotions associated to IO(B))
    """

#-------------------------------------------------------------------------------------------------------------------------------
#   Artwork Similarity
#-------------------------------------------------------------------------------------------------------------------------------

    def initializeArtworkDistanceMatrix(self):
        
        """
        # Interaction object dao and dataframe
        self.IO_dao = self.getInteractionObjectDAO()
        self.IO_data = self.getInteractionObjectData()
        """

        # Distance information
        self.distanceDict = self.computeIODistanceMatrix()
                
        #self.IO_distanceIndex = list(map(int, self.distanceDict['index']))
        self.IO_distanceIndex = self.distanceDict['index']
        self.IO_distanceMatrix = self.distanceDict['distanceMatrix']
        self.IO_data = self.distanceDict['data']

        """
        print("self.IO_distanceMatrix")
        print(self.IO_distanceMatrix)
        print("\n")
        
        matrix = self.IO_distanceMatrix.copy()
        matrix[matrix == 0.0] = 1.0
        matrix[matrix == 0.12] = 1.0
        
        # Get the two artworks with the highest similarity (In order to get high similarity artworks in iconclass)
        ind = np.unravel_index(np.argmin(matrix, axis=None), matrix.shape)
        """

    def computeIODistanceMatrix(self):
        """
        Method to calculate the distance matrix between all interaction objects included in data.

        Returns
        -------
        IO_distanceDict: dict
            Includes distance between interaction objects
                index:
                    IO index
                distanceMatrix: np.array
                    Matrix that contains all similarity values.
        """
        # Calculate interaction object (IO) similarity
        similarity_functions = self.perspective['similarity_functions']
        daoJson = self.getInteractionObjectDAO()

        # Compute similarity between artworks
        IO_similarityMeasure = ComplexSimilarityDAO(daoJson,similarity_functions)        
        IO_distanceMatrix = IO_similarityMeasure.matrix_distance_explanation()
        IO_data = IO_similarityMeasure.data

        # To get self.dominantAttributes
        self.dominantAttributes = IO_similarityMeasure.getSimilarityMeasuresDict()
        
        # Export _id (id artefact) and distance matrix to json file
        IO_distanceDict = {}
        IO_distanceDict['index'] = list(map(str, IO_similarityMeasure.data['id'].tolist()))
        IO_distanceDict['distanceMatrix'] = IO_distanceMatrix
        IO_distanceDict['data'] = IO_data
        
        return IO_distanceDict

        
    def getInteractionObjectDAO(self):        
        route = DataLoader.fileRoute('artworks.json')
        if route:
            daoJson = DAO_json(route)
            return daoJson
        else:
            # TODO: Change by Logger
            print("Unable load artworks.json")
            return None
        # loader = ArtworkLoader(os.environ['TYPE'], True, "https://api2.mksmart.org/object/2a2a5c9a-a8ce-4977-ba09-f4134c95d744", "0a7eccb2-997d-47d0-8c9f-05be9afc9772")
        # outputData = loader.getArtworks()
    
    def getInteractionObjectData(self):
        daoJson = self.getInteractionObjectDAO()
        return daoJson.getPandasDataframe()

#-------------------------------------------------------------------------------------------------------------------------------
#   Interaction Similarity - artwork similarity
#-------------------------------------------------------------------------------------------------------------------------------
  
    def getSimilarIOIndex(self, objectA, IOB):
        """
        Method to obtain the index of the object in IOB that is most similar to objectA
        
        Distance between IOs in the database are calculated beforehand (distanceMatrix). 
        Only IOs above a given x (0.7) are considered similar. If IOB doesn't include a similar object to objectA, the function returns -1.

        Parameters
        ----------
        objectA : object (int, String...)
            IDs of an object userA interacted with
        elemB : list
            List of IDs belonging to the objects userB interacted with.

        Returns
        -------
        double
            Index in the list IOB of the object userB interacted with that is most similar to objectB 
            -1 if all objects in IOB are not similar to objectA
        """
        # https://www.w3resource.com/python-exercises/numpy/python-numpy-exercise-31.php
        # https://stackoverflow.com/questions/15287084/numpy-find-the-values-of-rows-given-an-array-of-indexes
        # https://stackoverflow.com/questions/33678543/finding-indices-of-matches-of-one-array-in-another-array
        
        
        # Sometimes objectA is not in the artworks catalogue (ask about this)
        try:
            # Convert to string the object ids because in some cases artwork data has string ids while interactions have int ids
            objectA = str(objectA)
            IOB = list(map(str, IOB))
            
            """
            print("type object A: " + str(type(objectA)))
            print("type IO_distanceIndex: " + str(type(self.IO_distanceIndex[0])))
            print("objectA: " + str(objectA))
            print("IOB: " + str(IOB))
            print("\n")
            """
        
            objectAIndex = self.IO_distanceIndex.index(str(objectA))
            distanceMatrix_IOB_indexes = np.nonzero(np.in1d(self.IO_distanceIndex,IOB))[0]
            distanceMatrix_IOB_values = self.IO_distanceMatrix[objectAIndex, distanceMatrix_IOB_indexes]
            mostSimilarIOIndex2 = distanceMatrix_IOB_values.argmin()

            objectId = self.IO_distanceIndex[distanceMatrix_IOB_indexes[mostSimilarIOIndex2]]
            mostSimilarIOIndex = IOB.index(objectId)
            # print("objectId")
            # print(objectId)
            # print("IOB")
            # print(IOB)
            # print("most similar index")
            # print(mostSimilarIOIndex)
            # print("\n")
            mostSimilarIO = IOB[mostSimilarIOIndex]  

            
            
            """
            print("type object A: " + str(type(objectA)))
            print("type IO_distanceIndex: " + str(type(self.IO_distanceIndex[0])))
            print("objectA: " + str(objectA))
            print("IOB: " + str(IOB))
            print("\n")
            print("IO_distanceIndex: " + str(self.IO_distanceIndex))
            print(self.IO_distanceMatrix)
            print("\n")
            print("objectA index: " + str(objectAIndex))
            print("distanceMatrix_IOB_indexes: " + str(distanceMatrix_IOB_indexes))
            print("distanceMatrix_IOB_values: " + str(distanceMatrix_IOB_values))
            print("minimumDistance index: " + str(mostSimilarIOIndex))
            print("minimumDistance value: " + str(distanceMatrix_IOB_values[mostSimilarIOIndex]))
            print("most similar IO: " + str(mostSimilarIO))
            print("\n\n\n")
            
            """
            
            # Get index of elements above a given threshold (let is say 0.5)
            
            
            # If the best match is still dissimilar
            similarThreshold = 0.35
            similarThreshold = 0.65
            similarThreshold = 0.5

            if ('weightArtworks' in self.perspective['algorithm']):
                """
                print("check similarity threshold perspective")
                print(self.perspective['algorithm']['weightArtworks'])
                print(type(self.perspective['algorithm']['weightArtworks']))
                print("\n")

                print("similarThreshold: " + str(similarThreshold))
                """

                similarThreshold = float(self.perspective['algorithm']['weightArtworks'])

                """
                print("similarThreshold: " + str(similarThreshold))
                print("\n")
                """
            
            distanceThreshold = 1 - similarThreshold

            #similarThreshold = 0.3
            #similarThreshold = 0.8
            #similarThreshold = 0.6
            #similarThreshold = 500.0
            if (distanceMatrix_IOB_values[mostSimilarIOIndex2] > distanceThreshold):
                mostSimilarIOIndex = -1
                
            """
            """

            # return mostSimilarIOIndex, distanceMatrix_IOB_indexes, distanceMatrix_IOB_values, objectAIndex, mostSimilarIOIndex2, objectId
            return mostSimilarIOIndex
        
        except ValueError:
            
            # print("exception ")
            # print("type object A: " + str(type(objectA)))
            # """
            # """
            # print("objectA: " + str(objectA))
            # print("IO_distanceIndex: " + str(self.IO_distanceIndex))
            
            # objectAIndex = self.IO_distanceIndex.index(str(objectA))
            # print("objectA index: " + str(objectAIndex))
            # distanceMatrix_IOB_indexes = np.nonzero(np.in1d(self.IO_distanceIndex,IOB))[0]
            # print("distanceMatrix_IOB_indexes: " + str(distanceMatrix_IOB_indexes))
            # distanceMatrix_IOB_values = self.IO_distanceMatrix[objectAIndex, distanceMatrix_IOB_indexes]
            # print("distanceMatrix_IOB_values: " + str(distanceMatrix_IOB_values))
            # mostSimilarIOIndex = distanceMatrix_IOB_values.argmin()
            # print("most similar IO Index: " + str(mostSimilarIOIndex))
            # mostSimilarIO = IOB[mostSimilarIOIndex]
            # print("most similar IO: " + str(mostSimilarIO))
            
            print("end exception")
            
            return -1
            
        
        """
        """

#-------------------------------------------------------------------------------------------------------------------------------
#   Interaction Similarity
#-------------------------------------------------------------------------------------------------------------------------------

    def validatePerspective(self):
        """
        Validates if the perspective and the data are compatible.
        If not, the Community Model aborts and an informative error message is displayed to the user

        Parameters
        ----------

        """
        for citizenAttribute in self.perspective['user_attributes']:
            if (citizenAttribute['att_name'] not in self.data.columns):
                raise NameError('The perspective includes the explicit attribute ' + str(citizenAttribute['att_name']) + ', but this attribute is not in the data')

        for interactionSimilarity in self.perspective["interaction_similarity_functions"]:
            interactionAttribute = interactionSimilarity['sim_function']['on_attribute']['att_name']
            interactionAttributeOrigin = interactionAttribute + "_origin"
            interactionAttributeText = interactionAttribute.rsplit(".",1)[0] + ".text"

            if (interactionAttribute not in self.data.columns):
                raise NameError("User data doesn't include the attribute " + str(interactionAttribute) + " encoded in the perspective")
            elif (interactionAttributeOrigin not in self.data.columns):
                raise NameError("User data doesn't include the artwork associated to the attribute " + str(interactionAttribute) + " encoded in the perspective")
            elif (interactionAttributeText not in self.data.columns):
                raise NameError("User data doesn't include the text associated to the attribute " + str(interactionAttribute) + " encoded in the perspective")

    def __init__(self, dao, perspective):
        """Construct of TaxonomySimilarity objects.

        Parameters
        ----------
        data : pd.DataFrame
            Dataframe where index is ids of elements, columns a list of taxonomy member and
            values contain the number of times that a taxonomy member is in an element.
        """
        super().__init__(dao)
        self.perspective = perspective

        # Validate perspective with data format
        self.validatePerspective()

        self.initializeArtworkDistanceMatrix()
        
        """
        self.dominantAttributes = {}
        #for similarityFunction in self.perspective["interaction_similarity_functions"] + self.perspective["similarity_functions"]:
        for similarityFunction in self.perspective["similarity_functions"]:
            similarityFeature = similarityFunction['sim_function']['on_attribute']['att_name']
            similarityMeasure = similarityFunction['sim_function']['name']
            self.dominantAttributes[similarityFeature] = self.initializeFromPerspective(self.IO_dao, similarityFunction)
        """
        
        # Interaction similarity function
        self.similarityFunction = self.perspective["interaction_similarity_functions"][0]
        self.similarityColumn = self.similarityFunction['sim_function']['on_attribute']['att_name']
        
        # Interaction attributes
        self.interactionAttribute = self.similarityFunction['sim_function']['on_attribute']['att_name']
        self.interactionAttributeOrigin = self.interactionAttribute + "_origin"
        self.interactionAttributeText = self.interactionAttribute.rsplit(".",1)[0] + ".text"
        # For DMH
        self.interactionAttributeSource = self.interactionAttribute + '_source'

        # Fill na (interaction attributes)


        # Citizen attributes
        self.citizenAttributes = []
        for citizenAttribute in self.perspective['user_attributes']:
            self.citizenAttributes.append(citizenAttribute['att_name'])
        
        print("self.attribute: " + str(self.interactionAttribute))
        print("self.attribute (Origin): " + str(self.interactionAttributeOrigin))
        print("self.attribute (text): " + str(self.interactionAttributeText))
        print("self.data.columns: " + str(list(self.data.columns)))
        print("\n")

        print("self perspective")
        print(self.perspective)
        print("self.interactionSimilarityFunction")
        print(self.similarityFunction)
        print("\n")
        
        self.interactionSimilarityMeasure = self.initializeFromPerspective(dao, self.similarityFunction)

        print("checking self.interactionSimilarityFunction")
        print(self.interactionSimilarityMeasure.similarityFunction)
        print("\n")
        

        # Remove the interactions with emotion with interactionSimilarityMeasure empty
        IOColumn = self.similarityFunction['sim_function']['interaction_object']['att_name']
        df = self.data.copy()

        print("dsfdsfsdf")

        # Check element count
        print("\n")
        print(df[[self.interactionAttribute]])
        print("\n")
        print(df[[self.interactionAttributeOrigin]])
        print("\n")
        print(df[[self.interactionAttributeText]])
        print("\n")

        # explodeColumns = [self.interactionAttribute, self.interactionAttributeOrigin, self.interactionAttributeText]
        explodeColumns = [self.interactionAttribute, self.interactionAttributeOrigin, self.interactionAttributeText, self.interactionAttributeSource]
        df2 = df.explode(explodeColumns)

        df3 = df2.loc[ df2[self.similarityColumn].str.len() != 0 ]
        
        # Remove NaN values
        df3 = df3.dropna(subset=[self.interactionAttribute])
        
        # Remove False emotion
        
        # Remove interactions with artworks that are not in artworks.json
        df3 = df3.loc[ df3[self.interactionAttributeOrigin].isin(self.IO_data['id'].to_list()) ]

        print("df3")
        print(df3)
        print("\n\n")

        # Flag artwork is enabled (detect communities interacting with one specific artwork)
        # This flag is not added by the perspective configuration tool (for now, it is given manually)
        # if ('communityDetectionForArtwork' in self.perspective):
        # ["35230"] works
        if (self.checkSameArtworksFilter()):
            print("enter check same artwork filter")
            print("df3")
            print(df3)
            print("\n\n")
            df3 = self.applySameArtworksFilter(df3)
            print("df3")
            print(df3)
            print("\n\n")
                

        print("df3 after artwork flag")
        print(df3)
        print("\n\n")
        
        groupList = []
        groupList.append('userid')
        groupList.extend(self.citizenAttributes)

        # Df3 perspective
        print("df3 perspective")
        print(df3[['userid', self.interactionAttribute, self.interactionAttributeOrigin, self.interactionAttributeText]])
        print("\n")
        
        print("groupby groupList")
        print(groupList)
        print("\n\n")
            
        df4 = df3.groupby(groupList).agg(list)         
        df4 = df4.reset_index() 
        
        """
        Reset userid to str (to stop encoding problems)
        """
        df4['userid'] = df4['userid'].astype(str)
        
        
        # Add columns to save dominant interaction attributes
        for dominantAttribute in self.dominantAttributes:
            # artwork similarity functions
            df4[dominantAttribute + 'DominantInteractionGenerated'] = self.initializeInteractionInformationColummn(df4)
            
        # interaction similarity functions
        df4[self.similarityColumn + 'DominantInteractionGenerated'] = self.initializeInteractionInformationColummn(df4)
        df4[self.similarityColumn + 'DistanceDominantInteractionGenerated'] = self.initializeInteractionInformationColummn(df4)
        # artworks we could match with a similar artwork
        df4['dominantArtworksDominantInteractionGenerated'] = self.initializeInteractionInformationColummn(df4)
        
        self.data = df4.copy()

        # If self.data only has one user, throw exception
        if (len(self.data) <= 1):
            raise ValueError('Less than 2 interactions were found for the provided parameters. Clustering is impossible')

#-------------------------------------------------------------------------------------------------------------------------------
#   Optimize matrix_distance
#-------------------------------------------------------------------------------------------------------------------------------

    def matrix_distance(self):
        """
        Method to calculate the matrix of distance between all element included in data.

        Returns
        -------
        distanceMatrix: np.array
            Matrix that contains all similarity values.

        """
        users = self.data.index
        pairs = combinations_with_replacement(range(len(users)), r=2)

        # This checks 0,1 and 1,0
        # Change it to only check 0,1 and assign the same to 1,0
        distanceMatrix = np.zeros((len(users), len(users)))
        dominantValueMatrix = np.zeros((len(users), len(users))).tolist()

        for p in pairs:    
            dist = self.distance(p[0], p[1])

            distanceMatrix[p[0], p[1]] = dist
            distanceMatrix[p[1], p[0]] = dist

        # Reduce the distanceMatrix to 2 decimals
        distanceMatrix = np.round(distanceMatrix,2)
        
        self.distanceMatrix = distanceMatrix

        return self.distanceMatrix

#-------------------------------------------------------------------------------------------------------------------------------
#   Optimize distance
#-------------------------------------------------------------------------------------------------------------------------------

    def distance(self,elemA, elemB):
        """
        Method to obtain the distance between two element.

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
        userInteractionA = self.data.loc[elemA]
        userInteractionB = self.data.loc[elemB]
                
        """
        print(userInteractionA['userid'])
        print(userInteractionB['userid'])
        """

        # Get interaction objects (IO) the user interacted with
        # print(self.similarityFunction)
        
        # Get ids of artworks the user interacted with
        IOColumn = self.interactionAttribute + "_origin"
        #IOColumn = self.similarityFunction['sim_function']['interaction_object']['att_name']
        IOA = userInteractionA[IOColumn]
        IOB = userInteractionB[IOColumn]
        
        IOA = list(map(str, IOA))
        IOB = list(map(str, IOB))
        
        """
        print("IO Columns")
        print(IOColumn)
        print(IOA)
        print(IOB)
        print("\n\n\n")
        """
        
        """
        """
        
        
        self.exchanged = False
        
        if (len(IOB) > len(IOA)):
            self.exchanged = True
            # elemA, elemB = self.exchangeElements(elemA, elemB)
            IOA, IOB = self.exchangeElements(IOA,IOB)
            userInteractionA, userInteractionB = self.exchangeElements(userInteractionA, userInteractionB)
        """
        """

        return self.distanceInteraction(elemA, elemB, userInteractionA, userInteractionB, IOA, IOB)
        
    
    def distanceInteraction(self, elemA, elemB, userInteractionA, userInteractionB, IOA, IOB):
        # Set largest list to be A and the other B
        #self.exchanged = False
        
        # Initialize distance
        distanceTotal = 0
        distanceNumber = 0

        # Dominant interaction attribute value
        dominantInteractionAttribute = ""
        dominantInteractionAttributeDistance = 1.0

        dominantInteractionAttributes = []
        dominantInteractionAttributeDistances = {}
        
        # # Artwork implicit attributes
        # dominantValues = {}
        # for dominantAttribute in self.dominantAttributes:
        #     dominantValues[dominantAttribute] = ""
        #     if (self.dominantAttributes[dominantAttribute].dominantValueType() == "list"):
        #         dominantValues[dominantAttribute] = []
        # Similar artworks users are compared with
        dominantArtworks = []

        # List of lists: first list of dominant interaction attribute (citizenA), second (citizenB)                  
        # Save data
        interaction_dominantInteractionAttributes = [ [], [] ]
        interaction_dominantArtworks = [ [], [] ]

        # Dict with all the information about the dominant values associated to the artworks/interaction attribute with influence in the similarity betweemn the two users
        interactionInformation = [ {}, {} ]
        for interactionInformationAttribute in list(self.dominantAttributes.keys()) + [self.similarityColumn, 'dominantArtworks']:
            interactionInformation[0][interactionInformationAttribute] = []
            interactionInformation[1][interactionInformationAttribute] = []

        try:

            # For each IO in A, get most similar IO in B
            for objectIndexA in range(len(IOA)):
                objectA = IOA[objectIndexA]
                objectIndexB = self.getSimilarIOIndex(objectA, IOB)
                # objectIndexB, distanceMatrix_IOB_indexes, distanceMatrix_IOB_values, objectAIndex, objectBIndexMatrix, objectId = self.getSimilarIOIndex(objectA, IOB)
                objectB = IOB[objectIndexB]

                # # Print object information
                # if (userInteractionA['userid'] == '2JfmseEG' and userInteractionB['userid'] == 'jTb1qXEo'):
                #     print("checking user interaction 2JfmseEG")
                #     print("object A")
                #     print(IOA)
                #     print(objectIndexA)
                #     print(objectA)
                #     print("\n")
                #     print("object B")
                #     print(IOB)
                #     print(objectIndexB)
                #     print(objectB)
                #     print("\n")
                #     print("Extra information getSimilarIOIndex")
                #     print("distance matrix")
                #     print(self.IO_distanceMatrix)
                #     print("distance matrix indexes")
                #     print(self.IO_distanceIndex)
                #     print("objectAIndex")
                #     print(objectAIndex)
                #     print("object B Index Matrix")
                #     print(objectBIndexMatrix)
                #     print("object id")
                #     print(objectId)
                #     print("distanceMatrix_IOB_indexes")
                #     print(distanceMatrix_IOB_indexes)
                #     print("distanceMatrix_IOB_values")
                #     print(distanceMatrix_IOB_values)
                #     print("\n")
                #     print("\n")


                # A MATCHING SIMILAR ARTWORK WAS FOUND
                if (objectIndexB != -1):

                    # Retrieve the data from the database (if it exists)
                    getDatabaseConditions = {}
                    getDatabaseConditions['attribute'] = self.similarityColumn
                    getDatabaseConditions['similarity'] = self.similarityFunction['sim_function']['name']
                    getDatabaseConditions['citizen1'] = userInteractionA['userid']
                    getDatabaseConditions['artwork1'] = objectA
                    getDatabaseConditions['citizen2'] = userInteractionB['userid']
                    getDatabaseConditions['artwork2'] = objectB

                    daoInteractionDistances = DAO_db_interactionDistances()
                    databaseObject = daoInteractionDistances.getInteractionDistance(getDatabaseConditions)

#-------------------------------------------------------------------------------------------------------------------------------
#   Get interaction attribute distance & dominant interaction attribute
#-------------------------------------------------------------------------------------------------------------------------------
  
                    # Get interaction similarity feature associated to IO A and IO B
                    interactionFeatureA = userInteractionA[self.similarityColumn][objectIndexA]
                    interactionFeatureB = userInteractionB[self.similarityColumn][objectIndexB]
                    
                    if (len(databaseObject) > 0):
                        distance = databaseObject['distance']
                        dominantInteractionAttributesList = databaseObject['dominantValue']
                    else:
                        
                        # Calculate distance between them
                        distance = self.interactionSimilarityMeasure.distanceValues(interactionFeatureA, interactionFeatureB)

                        # Add dominant interaction value to list (e.g., emotions = {joy: 3, sadness: 4, trust: 1} -> sadness
                        dominantInteractionAttributesList = self.interactionSimilarityMeasure.dominantValue(interactionFeatureA, interactionFeatureB)

                        
                    dominantInteractionAttributeA = dominantInteractionAttributesList[0]
                    dominantInteractionAttributeB = dominantInteractionAttributesList[1]

                    #dominantInteractionAttributeDistance = self.interactionSimilarityMeasure.dominantDistance(interactionFeatureA, interactionFeatureB)
                    dominantInteractionAttributeDistance = self.interactionSimilarityMeasure.getDistanceBetweenItems(dominantInteractionAttributeA, dominantInteractionAttributeB)

#-------------------------------------------------------------------------------------------------------------------------------
#   Save interaction information
#-------------------------------------------------------------------------------------------------------------------------------

                    # if (self.exchanged):
                    #     dominantInteractionAttributeA, dominantInteractionAttributeB = self.exchangeElements(dominantInteractionAttributeA, dominantInteractionAttributeB)
                    #     objectA, objectB = self.exchangeElements(objectA, objectB)

                    interactionInformation[0][self.similarityColumn].append(dominantInteractionAttributeA)
                    interactionInformation[0]['dominantArtworks'].append(objectA)
                    
                    interactionInformation[1][self.similarityColumn].append(dominantInteractionAttributeB)
                    interactionInformation[1]['dominantArtworks'].append(objectB)

#-------------------------------------------------------------------------------------------------------------------------------
#   Get dominant values (artworks)
#-------------------------------------------------------------------------------------------------------------------------------

                    # Get dominant value (for each similarity measure attribute) associated to the 2 artworks: objectA and objectB
                    indexA = self.IO_data.loc[ self.IO_data['id'] == objectA ].index.values.astype(int)[0]
                    indexB = self.IO_data.loc[ self.IO_data['id'] == objectB ].index.values.astype(int)[0]

                    for dominantAttribute in self.dominantAttributes:
                        column = self.dominantValueColumn(name = dominantAttribute)
                        dominantValueMatrix = self.IO_data[column].tolist()

                        dominantValueA = dominantValueMatrix[indexA][indexB]
                        dominantValueB = dominantValueMatrix[indexB][indexA]

                        # dominantValues[dominantAttribute] = dominantValueA
                        
                        interactionInformation[0][dominantAttribute].append(dominantValueA)
                        interactionInformation[1][dominantAttribute].append(dominantValueB)

#-------------------------------------------------------------------------------------------------------------------------------
#   Distance between dominant interaction attribute (add later)
#-------------------------------------------------------------------------------------------------------------------------------

                    # # Add dominant interaction attributes
                    # dominantInteractionAttributes.append(dominantInteractionAttribute)
                    #dominantInteractionAttributeDistances.append(dominantInteractionAttributeDistance)
                    if dominantInteractionAttributeA not in dominantInteractionAttributeDistances:
                        dominantInteractionAttributeDistances[dominantInteractionAttributeA] = []
                    dominantInteractionAttributeDistances[dominantInteractionAttributeA].append(dominantInteractionAttributeDistance)


#-------------------------------------------------------------------------------------------------------------------------------
#   Save data in database
#-------------------------------------------------------------------------------------------------------------------------------

                    # Save data in database
                    getDatabaseConditions['objectA'] = self.IO_data.loc[ self.IO_data['id'] == objectA ]['tittle'].to_list()[0]
                    getDatabaseConditions['indexA'] = str(indexA)
                    getDatabaseConditions['dominantValueA'] = dominantValueA
                    getDatabaseConditions['objectB'] = self.IO_data.loc[ self.IO_data['id'] == objectB ]['tittle'].to_list()[0]
                    getDatabaseConditions['indexB'] = str(indexB)
                    getDatabaseConditions['dominantValueB'] = dominantValueB

                    getDatabaseConditions['distance'] = distance
                    getDatabaseConditions['dominantValue'] = dominantInteractionAttributesList

                    daoInteractionDistances.updateInteractionDistance(getDatabaseConditions)

                    distanceNumber += 1
                    distanceTotal += distance



                # NO SIMILAR ARTWORK    
                else:
                    distance = 1
                

                # distanceTotal += distance
                
            # Mean average        
            # distanceTotal /= len(IOA)
            if (distanceNumber == 0):
                distanceTotal = 1.0
            else:
                distanceTotal = distanceTotal / (max(1, distanceNumber))

            
            
        except Exception as e:

            logger = getLogger(__name__)
            logger.error(traceback.format_exc())
            
            distanceTotal = 1.0



            # print("\n\n\n")
            # print("Exception dominant attribute")
            # print(str(e))
            # """
            # print("elemA: " + str(elemA))
            # print("elemB: " + str(elemB))
            # """
            # print("userA: " + str(userInteractionA['userid']))
            # print("userB: " + str(userInteractionB['userid']))
            # print("IOA: " + str(IOA))
            # print("IOB: " + str(IOB))
            # print("interactionsA: " + str(userInteractionA[self.similarityColumn]))
            # print("interactionsB: " + str(userInteractionB[self.similarityColumn]))
            # print("objectIndexA: " + str(objectIndexA))
            # print("len IOA: " + str(len(IOA)))
            # print("IOA: " + str(IOA))
            # print(userInteractionA['userid'])

            # raise Exception(e)
            
            # # Get interaction similarity feature associated to IO A and IO B
            # interactionFeatureA = userInteractionA[self.similarityColumn][objectIndexA]
            # interactionFeatureB = userInteractionB[self.similarityColumn][objectIndexB]
            
            """
            print("interactionFeatureA: " + str(interactionFeatureA))
            print("interactionFeatureB: " + str(interactionFeatureB))
                    
            print("\n\n\n")
            """

            
#-------------------------------------------------------------------------------------------------------------------------------
#   Update pandas table with new information (dominant attribute)
#-------------------------------------------------------------------------------------------------------------------------------
        
        if (self.exchanged):
            interactionInformation.reverse()

        self.updateInteractionInformationColumns(elemA, elemB, interactionInformation[0])
        self.updateInteractionInformationColumns(elemB, elemA, interactionInformation[1])
             
        return distanceTotal


    def initializeInteractionInformationColummn(self, df4):
        # return [[] for _ in range(len(df4))]
        # return [[] for _ in range(len(df4))]
        return [ [ [] for _ in range(len(df4)) ] for _ in range(len(df4))]
    
    def updateInteractionInformationColumns(self, elemA, elemB, interactionInformationDict):
        """
        Updates the Pandas Dataframe with information related to the interaction in order to be used for explaining the communities

        Parameters
        ----------
        elemA: int
            Index associated to the citizen A to update. This id should be in self.data.
        elemB: int
            Index associated to the citizen B for which we are calculating its similarity with A. This id should be in self.data. 
        interactionInformationDict: dict
            keys: interaction (e.g., emotions, sentiments) and artworks (e.g., materials) similarity attributes
            values: interaction (dominant emotion/sentiment (String)), artworks (list of Strings)

        Returns
        -------
        
        """
        try:
            
            #-------------------------------------------------------------------------------------------------------------------------------
            #   Simplify dominant interaction attribute
            #-------------------------------------------------------------------------------------------------------------------------------

            # Get most frequent element in dominantInteractionAttributes
            if (len(interactionInformationDict[self.similarityColumn]) > 0):
                dominantInteractionAttribute = mode(interactionInformationDict[self.similarityColumn])
                
                #distances = dominantInteractionAttributeDistances[dominantInteractionAttribute]
                #dominantInteractionAttributeDistance = (sum(distances)) / (len(distances))
            
            else:
                dominantInteractionAttribute = ""
                #dominantInteractionAttributeDistance = 1.0

            interactionInformationDict[self.similarityColumn] = dominantInteractionAttribute

            #-------------------------------------------------------------------------------------------------------------------------------
            #   Update pandas columns
            #-------------------------------------------------------------------------------------------------------------------------------

            for key in interactionInformationDict:
                column = key + 'DominantInteractionGenerated'
                value = interactionInformationDict[key]

                if (key != self.similarityColumn and key != 'dominantArtworks'):
                    if (len(interactionInformationDict[key]) > 0):
                        # if (isinstance(interactionInformationDict[key][0], str)):
                        #     #value = interactionInformationDict[key][-1]
                        #     value = mode(interactionInformationDict[key])

                        # print("updateInteractionInformationColumn")
                        # print(interactionInformationDict[key])

                        np_array = np.asarray(interactionInformationDict[key], dtype=object)
                        value = list(np.hstack(np_array)) #if (len(np_array) > 0)

                        # print("flatten")
                        # print(value)
                        # print("\n")

                        #value = interactionInformationDict[key][-1]
                    else:
                        #value = ''
                        value = interactionInformationDict[key]

                self.data.at[elemA, column][elemB] = value

        except Exception as e:

            logger = getLogger(__name__)
            logger.error(traceback.format_exc())
            





#-------------------------------------------------------------------------------------------------------------------------------
#   Filter (SAME ARTWORKS)
#-------------------------------------------------------------------------------------------------------------------------------
    
    # Flag artwork is enabled (detect communities interacting with one specific artwork)
    # This flag is not added by the perspective configuration tool (for now, it is given manually)
    # if ('communityDetectionForArtwork' in self.perspective):
    # ["35230"] works
    def checkSameArtworksFilter(self):
        return len(self.perspective['similarity_functions']) == 1 and len(self.perspective['similarity_functions'][0]['sim_function']['params']) > 0

    def applySameArtworksFilter(self, df3):
        # Filter self.data to only consider users interacting with that artwork
        # Remove interactions with artworks other than the one given by the 'communityDetectionForArtwork' flag
        artworkId = self.perspective['similarity_functions'][0]['sim_function']['params'][0]['artworkId']
        #logger.info("communityDetectionArtwork: " + str(artworkId))

        # Get ids
        artworkIds = []
        for element in self.perspective['similarity_functions'][0]['sim_function']['params']:
            artworkIds.append(element['artworkId'])

        
        print("apply same artworks filter")
        print(df3[[self.interactionAttributeOrigin]])
        print("\n")

        #dfArtworkFlag = df3.loc[ df3[self.interactionAttributeOrigin] == artworkId ]
        dfArtworkFlag = df3.loc[ df3[self.interactionAttributeOrigin].isin(artworkIds) ] 
        if (dfArtworkFlag.empty):
            df3 = df3.head(1)
            #logger.info("There are not interactions with the artwork with id " + str(artworkId))
        else:
            df3 = dfArtworkFlag.copy()

        print("after apply same artworks filter")
        print(df3[[self.interactionAttributeOrigin]])
        print("\n")

        return df3      
        
    
    
    