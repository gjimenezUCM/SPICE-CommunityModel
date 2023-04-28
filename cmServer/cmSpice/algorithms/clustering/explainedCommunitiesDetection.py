# Authors: José Ángel Sánchez Martín
import numpy as np
import statistics

import pandas as pd

import json

from pandas.api.types import is_numeric_dtype


from cmSpice.dao.dao_api_iconclass import DAO_api_iconclass

import traceback
from cmSpice.logger.logger import getLogger

logger = getLogger(__name__)


class ExplainedCommunitiesDetection:
    """Class to search all communities that all members have a common
    propertie. This algorithm works with clustering techniques.
    """

    def __init__(self, algorithm, data, distanceMatrix, perspective = {}):
        """Method to configure the detection algorithm.

        Args:
            data (DataFrame): Data used to apply the similarity measure between
            users.
            algorithm (Class): Class of clustering technique.
            sim (str/Class, optional): Similarity function used in clustering
            technique. Defaults to 'euclidean'.
        """
        # To get iconclass data
        self.daoAPI_iconclass = DAO_api_iconclass()
        
        # Initialization
        self.algorithm = algorithm
        self.data = data.copy()
        self.distanceMatrix = distanceMatrix
        self.perspective = perspective
        
        self.user_attributes = []
        self.interaction_attributes = []
        self.artwork_attributes = []
        
        if (len(self.perspective) == 0):
            self.explanaible_attributes = self.data.columns
            
        else:
        
            # user's explicit attributes
            for userAttribute in self.perspective['user_attributes']:
                self.user_attributes.append(userAttribute['att_name'])
                
            # user's interaction features
            for similarityFunction in self.perspective['interaction_similarity_functions']:
                self.interaction_attributes.append(similarityFunction['sim_function']['on_attribute']['att_name'])
                
            # artwork's similarity features
            for similarityFunction in self.perspective['similarity_functions']:
                self.artwork_attributes.append(similarityFunction['sim_function']['on_attribute']['att_name'])

            # explainable attributes
            self.explanaible_attributes = []              
            if (self.explainInteractionAttributes() == False):
                self.explanaible_attributes = self.artwork_attributes
            else:
                self.explanaible_attributes = self.interaction_attributes

            # dissimilar attributes
            self.dissimilar_attributes = []
            self.dissimilar_atributes_dict = {}
            for similarityFunction in self.perspective['interaction_similarity_functions'] + self.perspective['similarity_functions']:
                if ('dissimilar' in similarityFunction['sim_function'] and similarityFunction['sim_function']['dissimilar'] == True):
                    self.dissimilar_attributes.append(similarityFunction['sim_function']['on_attribute']['att_name'])
                    self.dissimilar_atributes_dict[similarityFunction['sim_function']['on_attribute']['att_name']] = similarityFunction
        


    def filterFalsePositives(self, userCommunityLabels):
        """
        Rearranges false positives (users without community interactions) inside a community into users without community

        Args:
            userCommunityLabels: List of community labels associated to the users of self.data
                List 

        Returns:

        """
        # Clustering algorithms cause false positives while dealing with extreme similarity values (0).
        # Assign all these false positives (users with similarity 0 (distance 1) with all the other users in the community) to users without community    
        uniqueLabels = set(userCommunityLabels)
        uniqueLabels = sorted(uniqueLabels)
        falsePositives = []
        for community in uniqueLabels:
            falsePositives_df = self.complete_data.loc[ self.complete_data['community'] == community ]
            if (len(falsePositives_df) > 1):
                falsePositives_index = falsePositives_df['real_index'].tolist()
                falsePositives_userid = falsePositives_df.index.values.tolist()

                distanceMatrix_community = self.distanceMatrix[np.ix_(falsePositives_index,falsePositives_index)]

                # Sum
                distanceMatrix_community_sum = np.sum(distanceMatrix_community,axis=1).tolist()


                # Get false positives (distance 1 to all other users in the community (vs itself it is 0))
                falsePositiveDistance = len(falsePositives_df) - 1
                falsePositivesCommunity = [falsePositives_index[i] for i in range(len(distanceMatrix_community_sum)) if distanceMatrix_community_sum[i] == falsePositiveDistance]
                falsePositives.extend(falsePositivesCommunity)

        falsePositiveCommunity = uniqueLabels[-1] + 1
        for key in falsePositives:
            userCommunityLabels[key] = falsePositiveCommunity
            falsePositiveCommunity += 1

        # Reset community id (to start from 0)
        uniqueLabels = set(userCommunityLabels)      
        uniqueLabels = sorted(uniqueLabels)
        userCommunityLabels = [uniqueLabels.index(x) for x in userCommunityLabels]

        self.complete_data['community'] = userCommunityLabels

        return userCommunityLabels

    def correctCommunityCheck(self, community):
        """
        Checks if the community includes citizens that are unrelated to 1+ other members
        If it does, the community cannot be explained

        Args:
            community: pd.DataFrame

        Returns:
            isExplainable: True/False

        """
        falsePositives_index = community['real_index'].tolist()
        distanceMatrix_community = self.distanceMatrix[np.ix_(falsePositives_index,falsePositives_index)]

        isExplainable = True
        rows = distanceMatrix_community.shape[0]
        rowIndex = 0
        while isExplainable and rowIndex < rows:
            maxDistanceCounter = np.count_nonzero(distanceMatrix_community[rowIndex] == 1.0)
            if (maxDistanceCounter >= (rows / 2) ):
                isExplainable = False
            rowIndex += 1

        return isExplainable


    def search_all_communities(self, answer_binary=False, percentage=1.0):
        """Method to search all explainable communities.

        Args:
            answer_binary (bool, optional): True to indicate that a common property
            occurs only when all answers are 1.0. Defaults to False.
            percentage (float, optional): Value to determine the minimum percetage of
            commons answers to detect a community. Defaults to 1.0.

        Returns:
            int: Number of communities detected.
            dict: Dictionary where each user is assigned to a community.
        """
        try:

            maxCommunities = len(self.data)
            n_communities = min(1, maxCommunities)
            n_clusters = n_communities
            finish_search = False

            # Special case: not enough data (1 or less users)
            # This can happen if we filter by an artwork and only 1 or less users interacted with it.
            if (maxCommunities <= 1):
                finish_search = True
                result2 = []
                result = {}
                for user in self.data.index:
                    result[user] = 0
                    result2.append(0)

                complete_data = self.data.copy()
                complete_data['community'] = result.values()
                self.complete_data = complete_data

                # Comprobamos que para cada grupo existe al menos una respuesta en común
                self.communities = complete_data.groupby(by='community')

            while not finish_search:
                community_detection = self.algorithm(self.data)
                userCommunityLabels = community_detection.calculate_communities(distanceMatrix = self.distanceMatrix, n_clusters=n_communities)
                result = userCommunityLabels

                # Process community data (explanation)
                complete_data = self.data.copy()
                complete_data['community'] = userCommunityLabels
                self.complete_data = complete_data

                # Filter false positives
                userCommunityLabels = self.filterFalsePositives(userCommunityLabels)

                # Associate each element with its cluster/community
                ids_communities = {}
                for i in range(len(self.data.index)):
                    ids_communities[self.data.index[i]] = userCommunityLabels[i]

                result2 = list(ids_communities.values())
                result = ids_communities
                self.resultAlgorithm = result2
                self.idsCommunities = result

                # Try to simplifyInteractionAttributes directly in complete_data
                complete_data = self.simplifyInteractionAttributesCompleteData(complete_data, len(set(result2)), printing = False)

                # Comprobamos que para cada grupo existe al menos una respuesta en común
                explainables = []
                self.communities = complete_data.groupby(by='community')
                
                n_clusters = len(set(result2))
                n_communities_before = n_communities

                # Cannot be explained with implicit
                if (n_clusters < n_communities):
                    # Set n_communities = n_clusters (communities could not be explained)
                    #finish_search = True 
                    #n_communities = n_clusters
                    pass

                else:
                    
                    n_communities = n_clusters

                    # for c in range(n_communities):
                    for c in range(n_clusters):
                        community = self.communities.get_group(c)
                        #community = self.simplifyInteractionAttributes(community, printing = False)
                        explainables.append(self.is_explainable(community, answer_binary, percentage))


                    # finish_search = sum(explainables) == n_communities
                    finish_search = sum(explainables) == n_clusters
                
                # Each datapoint belongs to a different cluster  
                if (n_communities == maxCommunities):
                    finish_search = True
                    
                if not finish_search:
                    n_communities += 1

            # Set communities to be equal to clusters (if it is bigger, then at least one community cannot be explained)
            n_communities = n_clusters
            # Get medoids
            medoids_communities = self.getMedoidsCommunities(result2)
            
            communityDict = {}
            communityDict['number'] = n_communities
            communityDict['users'] = result
            communityDict['medoids'] = medoids_communities
            communityDict['percentage'] = percentage
            communityDict['userAttributes'] = self.user_attributes
            # For HECHT
            if ('Beliefs.beliefJ' in self.data.columns or 'demographics.food' in self.data.columns):
                communityDict['implicitAttributes'] = self.explanaible_attributes
            else:
                communityDict['implicitAttributes'] = []
            
            return complete_data, communityDict

        except Exception as e:
            logger.error(traceback.format_exc())

            communityDict = {}

            return self.data, communityDict
    
    def explainInteractionAttributes(self):
        return len(self.perspective['interaction_similarity_functions']) > 0

    def simplifyInteractionAttributesCompleteData(self, completeData_df, n_communities, printing = False):
        self.communities = completeData_df.groupby(by='community')
        communities = []

        for c in range(n_communities):
            community = self.communities.get_group(c)
            community = self.simplifyInteractionAttributes(community, printing = False)

            communities.append(community)

        df = pd.concat(communities)
        completeData_df = df.sort_values(by=['real_index'])

        return completeData_df
            
    def simplifyInteractionAttributes(self, community, printing = False):
        """
        Method to obtain the dominant value in the list of interaction attribute values with the other community members.
        
        Parameters
        ----------
        community : pd.dataframe
            Community member information

        Returns
        -------
        community: pd.dataframe
            Updated dataframe including the dominant value for each user-interaction attribute pair in new columns.
            Column name = community_ + 'interaction attribute label'
        """
                    
        df = community.copy()
        #for col in self.explanaible_attributes:
        # Include similarity features between artworks too
        #for col in self.explanaible_attributes + self.artwork_attributes + ['dominantArtworks']:
        # Add distance between emotions for dissimilar emotions
        simplify_cols = self.explanaible_attributes + self.artwork_attributes
        if (self.explainInteractionAttributes() == True):
            simplify_cols += ['dominantArtworks'] 

        simplify_cols = list(set(simplify_cols))

        for col in simplify_cols:  
            col2 = col + 'DominantInteractionGenerated'

            # Get row index of community members
            communityMemberIndexes = np.nonzero(np.in1d(self.data.index,community.index))[0]

            # Transform attribute list to fit community members
            df.loc[:, ('community_' + col)] = community.apply(lambda row: self.extractDominantInteractionAttribute(row, col2, communityMemberIndexes), axis = 1)
        
        return df
    
    def getMostFrequentElementsList(self, array, k):
        df=pd.DataFrame({'Number': array, 'Value': array})
        df['Count'] = df.groupby(['Number'])['Value'].transform('count')
        
        df1 = df.copy()
        df1 = df1.sort_values(by=['Count'], ascending=False)
        df1 = df1.drop_duplicates(['Number'])
                
        return df1.head(k)[['Number','Count']].to_dict('records')
    
    def extractDominantInteractionAttribute(self, row, col2, communityMemberIndexes):
        try:

            # Skip itself
            communityMembers_interactionAttributeList = [row[col2][i] for i in communityMemberIndexes if row[col2][i] != '' and i != row['real_index']]
            
            communityMembers_interactionAttributeList = [x for x in communityMembers_interactionAttributeList if (isinstance(x,dict) == False or isinstance(x,list) == False) or len(x) > 0]

            validCommunityIndexes = [i for i in communityMemberIndexes if row[col2][i] != '' and i != row['real_index']]

                        
            if (len(communityMembers_interactionAttributeList) > 0):
                communityMembers_validInteractionAttributeList = [x for x in communityMembers_interactionAttributeList if (isinstance(x,dict) == True or isinstance(x,list) == True) and len(x) > 0]


                if col2 == 'dominantArtworksDominantInteractionGenerated':
                    communityMembers_validInteractionAttributeList = [x for x in communityMembers_interactionAttributeList if len(x) > 0]
                    if (len(communityMembers_validInteractionAttributeList) > 0):
                        np_array = np.asarray(communityMembers_validInteractionAttributeList, dtype=object)
                        array2 = list(np.hstack(np_array)) #if (len(np_array) > 0)
                    else:
                        array2 = communityMembers_validInteractionAttributeList
                        
                    return list(set(array2))
                

                # Testing new iconclass attribute
                # Now, we get dictionaries with keys (iconclassIDs) and values (arrays indicating the [iconclassIDs artworkA, artworkB] they originate from)
                elif ('iconclassArrayIDs' in col2):
                    communityMembers_validInteractionAttributeList = [x for x in communityMembers_interactionAttributeList if len(x) > 0]

                    if (len(communityMembers_validInteractionAttributeList) > 0):
                        
                        return self.extractDominantAttributeDictExplanation(communityMembers_validInteractionAttributeList)

                    else:
                        return {}

                # Dominant attributes of the form 
                # dict: key (attribute); value (list of artwork(s) id(s) they reference)
                # Example: SAME ARTWORKS 
                # key: artwork id; value: [artwork id]
                elif (self.checkDictExplanation(communityMembers_validInteractionAttributeList)):

                    # Print
                    return self.extractDominantAttributeDictExplanation(communityMembers_validInteractionAttributeList)


                #elif (isinstance(communityMembers_interactionAttributeList[0],str)):
                elif (isinstance(communityMembers_interactionAttributeList[0],list) == False):

                    newList = []
                    for element in communityMembers_interactionAttributeList:
                        if (isinstance(element,dict)):
                            newList.extend(list(element.keys()))
                        elif (isinstance(element,str)):
                            newList.append(element)
                    communityMembers_interactionAttributeList = newList


                    if ('Distance' in col2):
                        return communityMembers_interactionAttributeList
                    else:
                        return statistics.mode(communityMembers_interactionAttributeList)







                # iconclass attribute (OLD) Not used anymore
                else:

                    communityMembers_validInteractionAttributeList = [x for x in communityMembers_interactionAttributeList if (isinstance(x,dict) == True or isinstance(x,list) == True) and len(x) > 0]
                    result = []
                    for interactionAttribute in communityMembers_validInteractionAttributeList:
                        result.extend(interactionAttribute)

                    # Return the 3 most frequent elements
                    result = self.getMostFrequentElementsList(result,5)
                    result = [ x['Number'] for x in result ]
                        
                    if (row['community'] == 6 and 1==2):
                        print("community 6")
                        print("col2: " + str(col2))
                        print("index: " + str(row['real_index']))
                        print("userName: " + str(row['userNameAuxiliar']))
                        artworks = [row['dominantArtworksDominantInteractionGenerated'][i] for i in communityMemberIndexes if row['dominantArtworksDominantInteractionGenerated'][i] != '' and i != row['real_index']]
                        print("dominantArtworks: " + str(row['dominantArtworksDominantInteractionGenerated']))
                        print("dominantArtworks community: " + str(artworks))
                        print("\n")
                    
                    return result

            else:
                return ''

        except Exception as e:
            logger.error(traceback.format_exc())

            return ''
        
    
    def checkDictExplanation(self, communityMembers_validInteractionAttributeList):
        return len(communityMembers_validInteractionAttributeList) > 0 and isinstance(communityMembers_validInteractionAttributeList[0],list) == True and isinstance(communityMembers_validInteractionAttributeList[0][0],dict) == True

    def extractDominantAttributeDictExplanation(self, communityMembers_validInteractionAttributeList):
        # First, create a combined dictionary containing all the arrays of pairs each iconclassIDs originates from
        iconclassDictionary = {}
        for interactionAttribute in communityMembers_validInteractionAttributeList:
            for interactionAttributeDict in interactionAttribute:
                for interactionAttributeKey in interactionAttributeDict:
                    if (interactionAttributeKey not in iconclassDictionary):
                        iconclassDictionary[interactionAttributeKey] = []
                    iconclassDictionary[interactionAttributeKey].append(interactionAttributeDict[interactionAttributeKey])
        
        for iconclassID in iconclassDictionary:
            set_of_jsons = {json.dumps(d, sort_keys=True) for d in iconclassDictionary[iconclassID]}
            iconclassDictionary[iconclassID] = [json.loads(t) for t in set_of_jsons]



        # Select x (5) keys with the highest number of results
        # using sorted() + join() + lambda
        # Sort dictionary by value list length
        sorted_iconclassDictionary = sorted(iconclassDictionary, key = lambda key: len(iconclassDictionary[key]))

        res = '#separator#'.join(sorted_iconclassDictionary)

        # From most frequent to less frequent
        result = res.split('#separator#')


        result.reverse()

        # Get children associated to the keys 
        result2 = []
        result2 = {k:iconclassDictionary[k] for k in result[0:5:1] if k in iconclassDictionary}

        return result2

    def is_explainable(self, community, answer_binary=False, percentage=1.0):
        try:
            if ('Beliefs.beliefJ' in self.data.columns):
                return self.is_explainable_AND(community, answer_binary, percentage)
            else:
                return self.is_explainable_OR(community, answer_binary, percentage)
        except Exception as e:
            logger.error("Error determining the explainability of the following community")
            logger.error(community)
            logger.error(traceback.format_exc())

            return False

    def is_explainable_OR(self, community, answer_binary=False, percentage=1.0):
        try:
            explainable_community = False

            # Users without community
            if (len(community) <= 1):
                explainable_community = True
            elif (self.correctCommunityCheck(community)):

                #for col in community.columns.values:
                for col2 in self.explanaible_attributes:
                    if col2 != 'community' and explainable_community == False:
                        if (self.explainInteractionAttributes()):
                            col = "community_" + col2
                        else:
                            #col = col2
                            col = "community_" + col2
                        
                        explainableAttribute = False
                        if answer_binary:
                            explainableAttribute = (len(community[col]) * percentage)  <= community[col].sum()
                        else:
                            explainableAttribute = (len(community[col]) * percentage) <= community[col].value_counts().max()

                        if (col2 in self.dissimilar_attributes):
                            explainableAttribute = not explainableAttribute


                        explainable_community |= explainableAttribute

            isExplainableResult = explainable_community

        except Exception as e:
            logger.error("Error determining the explainability of the following community")
            logger.error(community)
            logger.error(traceback.format_exc())

            isExplainableResult = True

        return isExplainableResult
    

    def is_explainable_AND(self, community, answer_binary=False, percentage=1.0):
        explainable_community = False

        # Users without community
        if (len(community) <= 1):
            explainable_community = True
        elif (self.correctCommunityCheck(community)):

            explainable_community = True

            for col2 in self.explanaible_attributes:
                if col2 != 'community' and explainable_community == True:
                    if (self.explainInteractionAttributes()):
                        col = "community_" + col2
                    else:
                        #col = col2
                        col = "community_" + col2

                    explainableAttribute = False
                    if answer_binary:
                        explainableAttribute = (len(community[col]) * percentage)  <= community[col].sum()
                    else:
                        explainableAttribute = (len(community[col]) * percentage) <= community[col].value_counts().max()

                    if (col2 in self.dissimilar_attributes):
                        explainableAttribute = not explainableAttribute

                    explainable_community = explainableAttribute


        return explainable_community
    
    
    def getMedoidsCommunities(self, clusteringResult):
        """
        Calculates the community medoid (Representative member)
            
        Parameters
        ----------
            clusteringResult [array]
                Array with the communities each data.row belongs to

        Returns
        -------
            communitiesMedoids [<class 'dict'>]
                Dictionary with keys (community id) and values (pandas dataframe with the medoid row)
        """
        
        # Get cluster representative (medoid)
        # The one with the smallest distance to each other datapoint in the cluster
        communities_members = {}
        for i in range(len(clusteringResult)):
            communities_members.setdefault(clusteringResult[i],[]).append(i)
        
        medoids_communities = {}
        for key in communities_members.keys():
            clusterIxgrid = np.ix_(communities_members[key],communities_members[key])
            clusterDistanceMatrix = self.distanceMatrix[clusterIxgrid]
            clusterRepresentativeIndex = np.argmin(np.sum(clusterDistanceMatrix, axis=1))
            clusterRepresentative = communities_members[key][clusterRepresentativeIndex]
            
            medoids_communities[key] = self.data.index[clusterRepresentative]

        return medoids_communities
    
    # Get the percentage of most frequent value for each feature.
    def secondExplanation(self,community):
        modePropertiesCommunity = {}

        for attribute in self.explanaible_attributes:
            counts = community[attribute].value_counts(normalize=True).mul(100)
            modeAttribute = community[attribute].value_counts().idxmax()
            modePropertiesCommunity[attribute] = {}
            modePropertiesCommunity[attribute]['representative'] = modeAttribute
            modePropertiesCommunity[attribute]['percentage'] = counts[modeAttribute]
    
        return modePropertiesCommunity
    
    
    
    def get_community(self, id_community, answer_binary=False, percentage=1.0):
        """Method to obtain all information about a community.

        Args:
            id_community (int): Id or name of community returned by detection method.
            answer_binary (bool, optional): True to indicate that a common property
            occurs only when all answers are 1.0. Defaults to False. Defaults to False.

        Returns:
            dict: All data that describes the community:
                - name: name of community.
                - members: list of index included in this community.
                - properties: common properties of community. It is a dictionary where:
                    each property is identified by column_name of data, and the value is
                    the common value in this column.
        """
        try:
                    
            community = self.communities.get_group(id_community)

            community_user_attributes = community[self.user_attributes]

            community_data = {'name': id_community}
            community_data['percentage'] = str(percentage * 100) + " %"
            community_data['members'] = community['userid'].tolist()
            
            community_data['data'] = community
     

            explainedCommunityProperties = dict()       

            community_attributes = list(set(self.explanaible_attributes + self.artwork_attributes))
            for col2 in community_attributes:
                if col2 != 'community':
                    if (self.explainInteractionAttributes()):
                        col = "community_" + col2
                    else:
                        col = "community_" + col2

                    if answer_binary:
                        if (len(community[col]) * percentage) <= community[col].sum():
                            explainedCommunityProperties[col] = community[col].value_counts().index[0]

                    else:
                    
                        array = community[col].tolist()   
                        array = [x for x in array if (isinstance(x,dict) == False or isinstance(x,list) == False) or len(x) > 0]


                        if (len(array) > 0 and isinstance(array[0],dict)):


                            # Combine all dictionaries inside the array into one dictionary
                            iconclassDictionary = {}
                            for dictionary in array:
                                for dictionaryKey in dictionary:
                                    if (dictionaryKey not in iconclassDictionary):
                                        iconclassDictionary[dictionaryKey] = []
                                    iconclassDictionary[dictionaryKey].extend(dictionary[dictionaryKey])


                            if (col != "community_" + "id"):
                                for key in iconclassDictionary:

                                    set_of_jsons = {json.dumps(d, sort_keys=True) for d in iconclassDictionary[key]}
                                    iconclassDictionary[key] = [json.loads(t) for t in set_of_jsons]



                            # Sort dictionary
                            res = '#separator#'.join(sorted(iconclassDictionary, key = lambda key: len(iconclassDictionary[key])))
                            result = res.split('#separator#')
                            result.reverse()

                            # Get x more frequent keys
                            result2 = []
                            result2 = {k:iconclassDictionary[k] for k in result[0:5:1] if k in iconclassDictionary}

                            result3 = {}


                            visualizationExplanationList = []

                            # Prepare explanation text for each of the selected keys
                            for iconclassID in result2:
                                iconclassText = ""
                                if (col == "community_" + "iconclassArrayIDs"):
                                    iconclassText = self.daoAPI_iconclass.getIconclassText(iconclassID)

                                # Get array of dicts {key: iconclassID, value: artwork it originates from}
                                np_array = np.asarray(result2[iconclassID], dtype=object)
                                iconclassChildren = list(np.hstack(np_array))

                                # basic explanation
                                iconclassExplanation = iconclassText + " " + "[" + str(iconclassID) + "]"

                                
                                
                                artworksExplanation = []

                                # New format for explanations
                                visualizationExplanation = {}
                                visualizationExplanation["key"] = iconclassExplanation

                                # key includes children keys (dict value): iconclass, ontology
                                if (isinstance(iconclassChildren[0],dict) == True):

                                    # Group iconclassChildren into a combined dictionary (values with the same key are added to an array)
                                    iconclassChildrenCombinedDictionary = {}
                                    for dictionary in iconclassChildren:
                                        for key, value in dictionary.items():
                                            if (key not in iconclassChildrenCombinedDictionary):
                                                iconclassChildrenCombinedDictionary[key] = []
                                            iconclassChildrenCombinedDictionary[key].extend(value)
                                            iconclassChildrenCombinedDictionary[key] = list(set(iconclassChildrenCombinedDictionary[key]))

               
                                    artworks_iconclassID = []
                                    for iconclassChild in iconclassChildrenCombinedDictionary:
                                        artworks_iconclassID.extend(iconclassChildrenCombinedDictionary[iconclassChild])
                                    artworks_iconclassID = set(artworks_iconclassID)


                                    iconclassExplanation += " - Artworks: " + str(len(artworks_iconclassID))
                                    visualizationExplanation["artworks"] = str(len(artworks_iconclassID))
                                    if (iconclassID in iconclassChildrenCombinedDictionary):
                                        artworksExplanation.extend(iconclassChildrenCombinedDictionary[iconclassID])
                                    iconclassChildrenText = []
                                    if (len(iconclassChildrenCombinedDictionary) > 1):

                                        iconclassExplanation += ". This identifier is the common parent of the following labels: "
                                        for iconclassChild in iconclassChildrenCombinedDictionary:
                                            iconclassChildText = ""
                                            # Iconclass: Get description of the iconclassID through the Iconclass API
                                            if (col == "community_" + "iconclassArrayIDs"):
                                                iconclassChildText = self.daoAPI_iconclass.getIconclassText(iconclassChild)
                                            # Instead of showing list artworks, just the number of them
                                            iconclassChildText += " (" + ", ".join(iconclassChildrenCombinedDictionary[iconclassChild]) + ")"

                                            artworksExplanation.extend(iconclassChildrenCombinedDictionary[iconclassChild])
                                            iconclassChildrenText.append(iconclassChildText + " " + "[" + str(iconclassChild) + "]")
                                        iconclassExplanation += "; ".join(iconclassChildrenText)
                                        iconclassExplanation += ""

                                result3[iconclassExplanation] = list(set(artworksExplanation))

                                visualizationExplanation["label"] = iconclassExplanation
                                visualizationExplanation["data"] = list(set(artworksExplanation))
                                visualizationExplanationList.append(visualizationExplanation)
                            
                            explainedCommunityProperties[col] = dict()
                            explainedCommunityProperties[col]["label"] = 'Community representative properties of the implicit attribute ' + "(" + str(col2) + ")" + ":"
                            explainedCommunityProperties[col]["explanation"] = visualizationExplanationList
                            explainedCommunityProperties[col]["explanation_type"] = 'implicit_attributes_list'


                        # For list types (artworks and iconclass)
                        elif (len(array) > 0 and isinstance(array[0],list)):

                            
                            np_array = np.asarray(array, dtype=object)

                            array2 = list(np.hstack(np_array))
                            
                            
                            result = self.getMostFrequentElementsList(array2,5)
                            result = [ x['Number'] for x in result ]
                            
                            result2 = {}
                            
                            
                            # Iconclass attribute
                            if (col == "community_" + "iconclassArrayIDs"):
                                for iconclassID in result:
                                    iconclassText = self.daoAPI_iconclass.getIconclassText(iconclassID)
                                    result2[str(iconclassID) + " " + iconclassText] = 0.0
                            # Other array attributes
                            else:
                                for element in result:
                                    result2[str(element)] = 100.0 / len(result)
                            
                                                        
                            explainedCommunityProperties[col] = dict()
                            explainedCommunityProperties[col]["label"] = 'Community representative properties of the implicit attribute ' + "(" + str(col2) + ")" + ":"
                            explainedCommunityProperties[col]["explanation"] = result2
                            explainedCommunityProperties[col]["explanation_type"] = 'implicit_attributes_map' 
                        
                        # For string types
                        else:

                            # Remove empty string
                            df = community.copy()
                            if (is_numeric_dtype(df[col])):
                                df[col] = df[col].astype(str)
                            df[col] = df[col].replace(['', 'unknown'], 'unknown')
                            df2 = df.copy()
                            percentageColumn = df2[col].value_counts(normalize=True) * 100
                            percentageColumnDict = percentageColumn.to_dict()
                            
                            explainedCommunityProperties[col] = dict()
                            explainedCommunityProperties[col]["label"] = 'Percentage distribution of the implicit attribute ' + "(" + str(col2) + ")" + ":"
                            explainedCommunityProperties[col]["explanation"] = percentageColumnDict
                            explainedCommunityProperties[col]["explanation_type"] = 'implicit_attributes_map'

            if ('explanation_type' not in explainedCommunityProperties):
                community_data['explanation_type'] = 'implicit_attributes'
            
            community_data['explanation'] = explainedCommunityProperties

        except Exception as e:
            logger.error(traceback.format_exc())

            
            explainedCommunityProperties[col] = dict()
            explainedCommunityProperties[col]["label"] = 'Community representative properties of the implicit attribute ' + "(" + str(col2) + ")" + ":"
            explainedCommunityProperties[col]["explanation"] = {}
            explainedCommunityProperties[col]["explanation_type"] = "implicit_attributes"

            community_data['explanation'] = explainedCommunityProperties
            
    
            
        return community_data
    
    
    
        