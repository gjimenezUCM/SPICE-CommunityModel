
#--------------------------------------------------------------------------------------------------------------------------
#    Python libraries
#--------------------------------------------------------------------------------------------------------------------------

import os
import pandas as pd
import numpy as np
import importlib

from inspect import getsourcefile
from os.path import abspath
import sys

#--------------------------------------------------------------------------------------------------------------------------
#    Custom Class
#--------------------------------------------------------------------------------------------------------------------------


# Community model tools
from cmSpice.core.communityJsonGenerator import CommunityJsonGenerator

# Community detection
from cmSpice.algorithms.clustering.explainedCommunitiesDetection import ExplainedCommunitiesDetection

# similarity measures
from cmSpice.algorithms.similarity.complexSimilarityDAO import ComplexSimilarityDAO

# dao
from cmSpice.dao.dao_csv import DAO_csv
from cmSpice.dao.dao_json import DAO_json
from cmSpice.dao.dao_db_users import DAO_db_users
from cmSpice.dao.dao_db_distanceMatrixes import DAO_db_distanceMatrixes
from cmSpice.dao.dao_db_communities import DAO_db_community
from cmSpice.dao.dao_db_similarities import DAO_db_similarity

from itertools import combinations_with_replacement
from itertools import combinations

from cmSpice.utils.dataLoader import DataLoader
import json

#--------------------------------------------------------------------------------------------------------------------------
#    Class
#--------------------------------------------------------------------------------------------------------------------------

class CommunitiesSimilarityModel():

    def __init__(self,perspectiveId, communityModel):
        """
        Construct of Community Model objects.

        Parameters
        ----------
            perspectiveId:
                id of the perspective to which the communities we want to calculate similarity on belong
        """
        self.perspectiveId = perspectiveId
        self.data = communityModel.getData()
        self.distanceMatrix = communityModel.getDistanceMatrix()
        # Remove last community (users without community)
        self.communities = communityModel.getCommunityVisualizationJSON()['communities'].copy()
        if (len(self.communities) > 0):
            if (self.communities[-1]['community-type'] != 'implicit'):
                self.communities.pop(-1)

        self.updateCommunitiesSimilarityCollection()
        
#--------------------------------------------------------------------------------------------------------------------------
#   Compute similarity between communities
#--------------------------------------------------------------------------------------------------------------------------
    
    def updateCommunitiesSimilarityCollection(self):
        daoSimilarities = DAO_db_similarity()
        # daoCommunities = DAO_db_community()
        
        # # Get all the communities associated to the new perspective
        # communitiesA = daoCommunities.getCommunitiesPerspective(self.perspectiveId)
        communitiesA = self.communities

        # Get index of the medoid explanation
        # indexMedoidExplanation = self.getIndexMedoidExplanation(communitiesA)

        # Compute similarity between the perspective communities
        # pairs = combinations_with_replacement(range(len(communitiesA)), r=2)
        pairs = combinations(range(len(communitiesA)), r=2)

        for p in pairs:
            communityA = communitiesA[p[0]]
            communityB = communitiesA[p[1]]

            # similarity = self.similarityCommunities(communityA, communityB)
            similarity = self.similarityCommunitiesAllAttributes(communityA, communityB)

            # Insert it in the two different orders
            similarityJson = {
                "similarity-function": "similarityMedoidCommunities",
                "value": similarity,
            }
            daoSimilarities.updateSimilarity(communityA['id'], communityB['id'], similarityJson)
            daoSimilarities.updateSimilarity(communityB['id'], communityA['id'], similarityJson)

#--------------------------------------------------------------------------------------------------------------------------
#   Distance between communities (medoid implicit attributes)
#--------------------------------------------------------------------------------------------------------------------------
    
    def distanceCommunities(self, communityA, communityB):
        # Get medoids (dm: distance matrix)
        # medoidA = communityA['explanations'][indexMedoidExplanation]['explanation_data']['id']
        # medoidB = communityB['explanations'][indexMedoidExplanation]['explanation_data']['id']

        distance = 1.0

        try:

            # Get representative citizen

            # centroidA = communityA['centroid']
            # centroidB = communityB['centroid']

            medoidA = communityA['medoid']
            medoidB = communityB['medoid']

            # Get distance between the medoids (implicit attributes [interaction attributes])
            userList = self.data['userid'].to_list()
            medoidA_distanceMatrixIndex = userList.index(medoidA)
            medoidB_distanceMatrixIndex = userList.index(medoidB)

            distance = self.distanceMatrix[medoidA_distanceMatrixIndex, medoidB_distanceMatrixIndex]

        except Exception as e:

            print("Error calculating similarities between communities")
            raise Exception(e)

        return distance

    def similarityCommunities(self, communityA, communityB):
        return 1 - self.distanceCommunities(communityA, communityB)
    
#--------------------------------------------------------------------------------------------------------------------------
#   Distance between communities (centroid implicit and explicit attributes)
#--------------------------------------------------------------------------------------------------------------------------
    
    def distanceCommunitiesAllAttributes(self, communityA, communityB):
        distance = 1.0

        try:

            # Get distance based on implicit attributes
            distanceImplicit = self.distanceCommunities(communityA, communityB)

            # Get distance based on explicit attributes
            distanceExplicit = 0.0
            numberExplicitAttributes = 0
            attributesDict = self.explicitAttributesDict()

            centroidDataA = communityA['centroid']
            centroidDataB = communityB['centroid']

            for explicitAttribute in centroidDataA["explicit_community"]:
                if explicitAttribute in attributesDict:
                    numberExplicitAttributes += 1

                    attributeValueA = centroidDataA["explicit_community"][explicitAttribute]
                    attributeValueB = centroidDataB["explicit_community"][explicitAttribute]
                    distanceExplicit += self.distanceExplicitAttribute(attributesDict[explicitAttribute], attributeValueA, attributeValueB)
                    
            distanceExplicit /= max(numberExplicitAttributes, 1)

            # Final distance: Same weight (implicit/explicit)
            distance = 0.7 * distanceImplicit + 0.3 * distanceExplicit

        except Exception as e:

            print("Error calculating similarities between communities")
            raise Exception(e)

        return distance

    def similarityCommunitiesAllAttributes(self, communityA, communityB):
        return 1 - self.distanceCommunitiesAllAttributes(communityA, communityB)

#--------------------------------------------------------------------------------------------------------------------------
#   Explicit attributes order (similarity between them is calculated based on the position in the list)
#   If it is not in the dict, similarity is calculated using EqualSimilarity (equal: 0, any different value: 1)
#--------------------------------------------------------------------------------------------------------------------------
    
    def explicitAttributesDict(self):
        explicitDict =  {
            "Demographics.DemographicsEducationType": [],
            "Demographics.DemographicsGender": [],
            "Demographics.DemographicsGrade": [],
            "Demographics.DemographicsIdentity": [],
            "Demographics.DemographicsPolitics": ['VL', 'L', 'C', 'R', 'VR'],
            "Demographics.DemographicsReligous": ['S', 'M', 'R', 'VR', 'H'],
            "Demographics.DemographicsPrepDuration": [],
            "Demographics.School": [],
            "Demographics.ParticipantType": [],
            "Beliefs.RHMSChange": ["high", "medium", "low"],
            "Beliefs.RHMSPrep": ["high", "medium", "low"],
            "Beliefs.RHMSPost": ["high", "medium", "low"],
            "Beliefs.AOTChange": ["high", "medium", "low"],
            "Beliefs.AOTPrep": ["high", "medium", "low"],
            "Beliefs.AOTPost": ["high", "medium", "low"],

            "demographics.Gender": [],
            "demographics.Age": [],
            "demographics.RelationshipWithArt": [],
            "demographics.RelationshipWithMuseum": [],
            "demographics.ContentInLIS": [],

            "demographics.explicit-community": []
        }

        return explicitDict

    def distanceExplicitAttribute(self, explicitAttributeList, attributeValueA, attributeValueB):
        if (attributeValueA in explicitAttributeList and attributeValueB in explicitAttributeList):
            indexA = explicitAttributeList.index(attributeValueA)
            indexB = explicitAttributeList.index(attributeValueB)

            denominator = max(len(explicitAttributeList) - 1, 1)
            result = (abs(indexA - indexB)) / denominator
        else:
            result = float(attributeValueA != attributeValueB)

        return result

    def similarityExplicitAttribute(self, explicitAttributeList, attributeValueA, attributeValueB):
        return 1 - self.distanceExplicitAttribute(explicitAttributeList, attributeValueA, attributeValueB)

        
#--------------------------------------------------------------------------------------------------------------------------
#  Alternative similarity between communities. 
#  To use it instead of the centroid linkage, replace "self.distanceCommunities" with one of the functions below
#--------------------------------------------------------------------------------------------------------------------------
    
    def singleLinkage(self, communityA, communityB):
        usersA = communityA['users']
        usersB = communityB['users']
        userList = self.data['userid'].to_list()

        userIndexA = [userList.index(x) for x in usersA]
        userIndexB = [userList.index(x) for x in usersB]

        distanceMatrix_singleLinkage = self.distanceMatrix[np.ix_(userIndexA,userIndexB)]
        clusterRepresentativeIndex = np.argmin(distanceMatrix_singleLinkage)

        singleLinkageUserA = clusterRepresentativeIndex / np.shape(distanceMatrix_singleLinkage)[1]
        singleLinkageUserB = clusterRepresentativeIndex % np.shape(distanceMatrix_singleLinkage)[1]
        
        return np.min(distanceMatrix_singleLinkage)

    def completeLinkage(self, communityA, communityB):
        usersA = communityA['users']
        usersB = communityB['users']
        userList = self.data['userid'].to_list()

        userIndexA = [userList.index(x) for x in usersA]
        userIndexB = [userList.index(x) for x in usersB]

        distanceMatrix_completeLinkage = self.distanceMatrix[np.ix_(userIndexA,userIndexB)]
        clusterRepresentativeIndex = np.argmax(distanceMatrix_completeLinkage)

        singleLinkageUserA = clusterRepresentativeIndex / np.shape(distanceMatrix_completeLinkage)[1]
        singleLinkageUserB = clusterRepresentativeIndex % np.shape(distanceMatrix_completeLinkage)[1]
        
        return np.max(distanceMatrix_completeLinkage)

    def averageLinkage(self, communityA, communityB):
        usersA = communityA['users']
        usersB = communityB['users']
        userList = self.data['userid'].to_list()

        userIndexA = [userList.index(x) for x in usersA]
        userIndexB = [userList.index(x) for x in usersB]

        distanceMatrix_averageLinkage = self.distanceMatrix[np.ix_(userIndexA,userIndexB)]

        return np.mean(distanceMatrix_averageLinkage)

    