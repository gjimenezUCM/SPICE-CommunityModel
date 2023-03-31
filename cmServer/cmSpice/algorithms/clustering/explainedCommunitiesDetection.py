# Authors: José Ángel Sánchez Martín
import numpy as np
import statistics

import pandas as pd

import json

from pandas.api.types import is_numeric_dtype


from cmSpice.dao.dao_api_iconclass import DAO_api_iconclass

import traceback
from cmSpice.logger.logger import getLogger


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
            print("explanaible attributes")
            print(self.explainInteractionAttributes())
            print("\n")
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
        #uniqueLabels = set(ids_communities.values())      
        uniqueLabels = set(userCommunityLabels)
        uniqueLabels = sorted(uniqueLabels)
        falsePositives = []
        for community in uniqueLabels:
            falsePositives_df = self.complete_data.loc[ self.complete_data['community'] == community ]
            if (len(falsePositives_df) > 1):
                falsePositives_index = falsePositives_df['real_index'].tolist()
                falsePositives_userid = falsePositives_df.index.values.tolist()

                """


                print("self.distanceMatrix")
                print(self.distanceMatrix)
                print("\n")
                """

                """
                indexes = self.data.index
                updateIndexes = self.data[self.data['userid'].isin(userIds)].index #.tolist()
                pairs = product(indexes,updateIndexes)
                
                ##print(self.data)
                
                
                matrix = np.zeros((len(indexes), len(indexes)))
                matrix[0:distanceMatrix.shape[0],0:distanceMatrix.shape[1]] = distanceMatrix
                """

                ##print(matrix)

                distanceMatrix_community = self.distanceMatrix[np.ix_(falsePositives_index,falsePositives_index)]
        

                #distanceMatrix_community = self.distanceMatrix[falsePositives_index, falsePositives_index]


                # Sum
                distanceMatrix_community_sum = np.sum(distanceMatrix_community,axis=1).tolist()


                # Get false positives (distance 1 to all other users in the community (vs itself it is 0))
                falsePositiveDistance = len(falsePositives_df) - 1
                #falsePositivesCommunity = [falsePositives_userid[i] for i in range(len(distanceMatrix_community_sum)) if distanceMatrix_community_sum[i] == falsePositiveDistance]
                falsePositivesCommunity = [falsePositives_index[i] for i in range(len(distanceMatrix_community_sum)) if distanceMatrix_community_sum[i] == falsePositiveDistance]
                falsePositives.extend(falsePositivesCommunity)


        #         # Print debug
        #         print("community " + str(community))
        #         print("falsePositives_df")
        #         print(falsePositives_df[['real_index', 'community']])
        #         print("\n")
        #         print("false positives index")
        #         print(falsePositives_index)
        #         print("\n")
        #         print("false positives userid")
        #         print(falsePositives_userid)
        #         print("\n")

        #         # print("self.distanceMatrix")
        #         # print(self.distanceMatrix)
        #         # print("\n")

        #         # print("self distance matrix row 0")
        #         # print(self.distanceMatrix[ falsePositives_index[0] ])
        #         # print("\n")

        #         print("self.distanceMatrix community")
        #         print(distanceMatrix_community)
        #         print("\n")

        #         print("self.distanceMatrix community sum")
        #         print(distanceMatrix_community_sum)
        #         print("\n")

        #         print("false positives community")
        #         print(falsePositivesCommunity)
        #         print("\n")

        #         print("false positives final")
        #         print(falsePositives)
        #         print("\n")

        #     else:

        #         print("without community")
        #         print("falsePositives_df")
        #         print(falsePositives_df[['real_index', 'community']])
        #         print("\n")


        # print("total communities")
        # print(len(uniqueLabels))
        # print("\n")


        """
        print("falsePositives final")
        print(falsePositives)
        print("\n")
        """

        """
        print("ids_communities")
        print(ids_communities)
        print("\n")
        """

        """
        print("community labels")
        print(userCommunityLabels)
        print("\n")

        print("original community Labels")
        print(uniqueLabels)
        print("\n")
        """

        falsePositiveCommunity = uniqueLabels[-1] + 1
        for key in falsePositives:
            userCommunityLabels[key] = falsePositiveCommunity
            falsePositiveCommunity += 1
            """
            if key in ids_communities:
                ids_communities[key] = falsePositiveCommunity
                falsePositiveCommunity += 1
            else:
                print("false positive " + str(key) + " is not in ids_communities")
            """

        
        # falsePositiveCommunity = uniqueLabels[-1] + 1
        # for key in falsePositives:
        #     if key in ids_communities:
        #         ids_communities[key] = falsePositiveCommunity
        #         falsePositiveCommunity += 1
        #     else:
        #         print("false positive " + str(key) + " is not in ids_communities")

        # Reset community id (to start from 0)
        #uniqueLabels = set(ids_communities.values())      
        uniqueLabels = set(userCommunityLabels)      
        uniqueLabels = sorted(uniqueLabels)
        # for key in ids_communities:
        #     ids_communities[key] = uniqueLabels.index(ids_communities[key])
        userCommunityLabels = [uniqueLabels.index(x) for x in userCommunityLabels]

        """
        print("ids_communities falsePositive")
        print(ids_communities)
        print("\n")
        """

        """
        print("community labels falsePositive")
        print(userCommunityLabels)
        print("\n")

        print("complete data communities before correction")
        print(self.complete_data[['community']])
        print("\n")
        """

        #complete_data['community'] = ids_communities.values()
        self.complete_data['community'] = userCommunityLabels
        
        """
        print("complete data communities after correction")
        print(self.complete_data[['community']])
        print("\n")
        """

        """
        result2 = result
        result = ids_communities
        self.resultAlgorithm = result2
        self.idsCommunities = result
        """

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
            # maxDistanceCounter = distanceMatrix_community[rowIndex].count(1.0)
            maxDistanceCounter = np.count_nonzero(distanceMatrix_community[rowIndex] == 1.0)
            if (maxDistanceCounter >= (rows / 2) ):
                isExplainable = False
            rowIndex += 1

        return isExplainable

        # falsePositives_index = community['real_index'].tolist()
        # distanceMatrix_community = self.distanceMatrix[np.ix_(falsePositives_index,falsePositives_index)]

        # isExplainable = True
        # rows = distanceMatrix_community.shape[0]
        # rowIndex = 0
        # while isExplainable and rowIndex < rows:
        #     if (1.0 in distanceMatrix_community[rowIndex]):
        #         isExplainable = False
        #     rowIndex += 1

        # return isExplainable



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
        maxCommunities = len(self.data)
        n_communities = min(1, maxCommunities)
        n_clusters = n_communities
        finish_search = False

        print("search_all_communities")

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
            # print("search communities loop - n_communities: " + str(n_communities))
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
            
            """
            print("columns")
            print(complete_data.columns)
            print("\n")
            
            print("complete data simplify dominant")
            print(complete_data['community_' + 'dominantArtworks'])
            print("\n")
            
            print("complete data")
            print("columns")
            print(complete_data.columns)
            print("\n")
            print(complete_data[['userNameAuxiliar','ColourDominantInteractionGenerated']])
            print("\n")
            print(complete_data[['userNameAuxiliar','community_' + 'Colour']])
            print("\n")

            col = 'ColourDominantInteractionGenerated'
            x = list(complete_data[col].tolist())[0]
            print(col)
            print(x)
            print("\n")

            col = 'community_' + 'Colour'
            x = list(complete_data[col].tolist())[0]
            print(col)
            print(x)
            print("\n")
            """

            # Comprobamos que para cada grupo existe al menos una respuesta en común
            explainables = []
            self.communities = complete_data.groupby(by='community')
            
            
            #for c in range(n_communities):
            #n_clusters = min(n_communities,len(set(result2)))
            n_clusters = len(set(result2))
            n_communities_before = n_communities

            print("n_communities: " + str(n_communities))
            print("\n")

            # Cannot be explained with implicit
            if (n_clusters < n_communities):
                # Set n_communities = n_clusters (communities could not be explained)
                #finish_search = True 
                #n_communities = n_clusters

                """
                print("n clusters is less than communities")
                print("maxCommunities")
                print(str(maxCommunities))
                print("n clusters")
                print(str(n_clusters))
                print("n_communities before clusters")
                print(str(n_communities_before))
                print("n_communities")
                print(str(n_communities))
                print("explainables")
                print(str(sum(explainables)))
                print("\n")
                """



            else:
                

                

                n_communities = n_clusters


                """
                
                """

                # for c in range(n_communities):
                for c in range(n_clusters):
                    community = self.communities.get_group(c)
                    #community = self.simplifyInteractionAttributes(community, printing = False)
                    explainables.append(self.is_explainable(community, answer_binary, percentage))

                """
                print("maxCommunities")
                print(str(maxCommunities))
                print("n clusters")
                print(str(n_clusters))
                print("n_communities before clusters")
                print(str(n_communities_before))
                print("n_communities")
                print(str(n_communities))
                print("explainables")
                print(str(sum(explainables)))
                print("\n")
                """
                

                # finish_search = sum(explainables) == n_communities
                finish_search = sum(explainables) == n_clusters
            
            # Each datapoint belongs to a different cluster  
            if (n_communities == maxCommunities):
                finish_search = True
                
            if not finish_search:
                n_communities += 1
            """
            if finish_search:
                print("finish search")
                for c in range(n_communities):
                    community = self.communities.get_group(c)
                    print("community " + str(c))
                    print(community[['userNameAuxiliar','community']])
                    print("\n")
            """

        # Set communities to be equal to clusters (if it is bigger, then at least one community cannot be explained)
        n_communities = n_clusters
        # Get medoids
        medoids_communities = self.getMedoidsCommunities(result2)

        """
        print("end search_all_communities")
        print("maxCommunities")
        print(str(maxCommunities))
        print("n clusters")
        print(str(n_clusters))
        print("n_communities before clusters")
        print(str(n_communities_before))
        print("n_communities")
        print(str(n_communities))
        print("explainables")
        print(str(sum(explainables)))
        print("\n")
        """

        
        
        print("complete data communities")
        print(complete_data[['community']])
        print("\n")

        print("community unique")
        print(complete_data['community'].unique())
        print("\n")
        """
        """

        """
        print("complete data")
        print(self.complete_data)
        print("\n")
        """
        
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
        """
        print("simplify interaction attributes")
        print(community['community'].tolist())
        print("\n\n")
        """
        
        # This is not used anymore
        if (1 == 2 and self.explainInteractionAttributes() == False):
            return community
        else:
                    
            df = community.copy()
            #for col in self.explanaible_attributes:
            # Include similarity features between artworks too
            #for col in self.explanaible_attributes + self.artwork_attributes + ['dominantArtworks']:
            # Add distance between emotions for dissimilar emotions
            simplify_cols = self.explanaible_attributes + self.artwork_attributes
            if (self.explainInteractionAttributes() == True):
                simplify_cols += ['dominantArtworks'] 

            simplify_cols = list(set(simplify_cols))
            
            # for attribute in self.dissimilar_attributes:
            #     simplify_cols.append(attribute + "Distance")

            """
            print("simplify community")
            print(df)
            print("\n")
            print(df.columns)
            print("\n")

            
            print("simplify_cols")
            print(simplify_cols)
            print("\n")
            """
            for col in simplify_cols:  
                col2 = col + 'DominantInteractionGenerated'

                # Get row index of community members
                communityMemberIndexes = np.nonzero(np.in1d(self.data.index,community.index))[0]


                #communityMemberIndexes = np.nonzero(np.in1d(self.data.index,self.data.index))[0]

                """
                print("community")
                print(community)

                print("data index:")
                print(self.data.index)
                print("community index:")
                print(community.index)
                print("communityMemberIndexes: ")
                print(communityMemberIndexes)
                print("\n")
                """
                
                """
                if (printing):
                    print("col2: " + str(col2))
                    print(df[col2])
                    print("self.data.index: " + str(self.data.index))
                    print("community.index: " + str(community.index))
                    print("community member indexes: " + str(communityMemberIndexes))
                    print("\n\n")
                
                """   



                #print("simplify attribute: " + str(col2))
                
                # From the attribute list, consider only the ones between the members of the community
                # https://stackoverflow.com/questions/23763591/python-selecting-elements-in-a-list-by-indices
                # Transform attribute list to fit community members
                df.loc[:, ('community_' + col)] = community.apply(lambda row: self.extractDominantInteractionAttribute(row, col2, communityMemberIndexes), axis = 1)
                # df.loc[:, ('community_' + col)] = community.apply(lambda row: statistics.mode([row[col2][i] for i in communityMemberIndexes if row[col2][i] != '']), axis = 1)
            
                
            # if (1 == 2):
            #     print("dominantArtworks")
            #     print(df[['real_index','userNameAuxiliar', 'community_dominantArtworks']])
            #     print("\n")

            # """
            # if (printing):
            #     print('dominant artworks')
            #     print(df[['real_index', 'community_' + 'dominantArtworks']])
            #     print("\n")
            
            # """

            # if ('jTb1qXEo' in df['userNameAuxiliar'].tolist()):
            #     print("community attribute jTb1qXEo")
            #     print(df[['community_dominantArtworks']])
            #     print(df[['community_iconclassArrayIDs']])
            #     print("\n")

            
            return df
    
    def getMostFrequentElementsList(self, array, k):
        df=pd.DataFrame({'Number': array, 'Value': array})
        df['Count'] = df.groupby(['Number'])['Value'].transform('count')
        
        df1 = df.copy()
        df1 = df1.sort_values(by=['Count'], ascending=False)
        df1 = df1.drop_duplicates(['Number'])
        
        #return df1.head(k)['Number'].tolist()
        
        return df1.head(k)[['Number','Count']].to_dict('records')
    
    def extractDominantInteractionAttribute(self, row, col2, communityMemberIndexes):
        try:

            #communityMembers_interactionAttributeList = [row[col2][i] for i in communityMemberIndexes if row[col2][i] != '']
            # Skip itself
            communityMembers_interactionAttributeList = [row[col2][i] for i in communityMemberIndexes if row[col2][i] != '' and i != row['real_index']]
            
            # print("extract Dominant interaction attribute")
            # print(col2)
            # print(communityMembers_interactionAttributeList)
            # print("\n")
            
            communityMembers_interactionAttributeList = [x for x in communityMembers_interactionAttributeList if (isinstance(x,dict) == False or isinstance(x,list) == False) or len(x) > 0]
            
            # print(communityMembers_interactionAttributeList)
            # print("\n")

            validCommunityIndexes = [i for i in communityMemberIndexes if row[col2][i] != '' and i != row['real_index']]

            # if (row['userNameAuxiliar'] == 'jTb1qXEo' and col2 == 'dominantArtworksDominantInteractionGenerated' and 1 == 1):
            #     print("extract dominant interaction attribute")
            #     print(col2)
            #     print(row['real_index'])
            #     print(row['userNameAuxiliar'] )
            #     print(row['dominantArtworksDominantInteractionGenerated'])
            #     print(row['iconclassArrayIDsDominantInteractionGenerated'])
            #     print(communityMemberIndexes)
            #     array = []
            #     array2 = []
            #     for index in communityMemberIndexes:
            #         array.append(row['dominantArtworksDominantInteractionGenerated'][index])
            #         array2.append(row['iconclassArrayIDsDominantInteractionGenerated'][index])

            #     print(array)
            #     print(array2)

            #     print(communityMembers_interactionAttributeList)
            #     print("\n")

            #if (row['userNameAuxiliar'] == 'e4aM9WL7' and col2 == 'dominantArtworksDominantInteractionGenerated' and 1 == 2):
            if (row['userNameAuxiliar'] == 'x2AUnHqw' and col2 == 'dominantArtworksDominantInteractionGenerated' and 1 == 1):
            
            
                """
                print("username: " + row['userNameAuxiliar'])
                print("index: " + str(row['real_index']))
                print("community: " + str(row['community']))
                print("dominant artworks: " + str(row[col2]))
                print("communityMemberIndexes: " + str(communityMemberIndexes))
                print("communityMembers_interactionAttributeList")
                print(communityMembers_interactionAttributeList)
                print("\n")

                
                """
                        
            if (len(communityMembers_interactionAttributeList) > 0):
                communityMembers_validInteractionAttributeList = [x for x in communityMembers_interactionAttributeList if (isinstance(x,dict) == True or isinstance(x,list) == True) and len(x) > 0]

                # print(communityMembers_validInteractionAttributeList)
                # print("\n")

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
                # elif ('iconclassArrayIDs' in col2 or 'Materials' in col2 or 'Colour' in col2):
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
                
                    # return statistics.mode(communityMembers_interactionAttributeList)
                    # Sort key by length of the array
                    #communityMembers_validInteractionAttributeList = [x for x in communityMembers_interactionAttributeList if len(x) > 0]

                    # print ("function return")
                    # print(col2)
                    # print(communityMembers_validInteractionAttributeList)
                    # print("\n")

                    # Print
                    return self.extractDominantAttributeDictExplanation(communityMembers_validInteractionAttributeList)


                    
                    """
                    print("new dict explanation")
                    print("username: " + row['userNameAuxiliar'])
                    print("index: " + str(row['real_index']))
                    print("community: " + str(row['community']))
                    print("dominant artworks: " + str(row[col2]))
                    print("communityMemberIndexes: " + str(communityMemberIndexes))
                    print("communityMembers_interactionAttributeList")
                    print(communityMembers_interactionAttributeList)
                    print("\n")
                    """

                    """
                    """

                    # Flatten array of dicts into a dict
                    #res = {k: v for d in ini_dict for k, v in d.items()}
                    explanationDictionary = {}
                    for dictionary in communityMembers_validInteractionAttributeList:
                        for key in dictionary:
                            if (key not in explanationDictionary):
                                explanationDictionary[key] = []
                            explanationDictionary[key].append(dictionary[key])

                    
                    # Sort it by length of key
                    # Select x (5) keys with the highest number of results
                    # using sorted() + join() + lambda
                    # Sort dictionary by value list length
                    res = '#separator#'.join(sorted(explanationDictionary, key = lambda key: len(explanationDictionary[key])))

                    # From most frequent to less frequent
                    result = res.split('#separator#')
                    result.reverse()

                    
                    print("result")
                    print(result)
                    print("\n")
                    """
                    """

                    # Get children associated to the keys 
                    result2 = []
                    result2 = {k:explanationDictionary[k] for k in result[0:5:1] if k in explanationDictionary}

                    
                    print("result2")
                    print(result2)
                    print("\n")
                    """
                    """

                    return result2

                #elif (isinstance(communityMembers_interactionAttributeList[0],str)):
                elif (isinstance(communityMembers_interactionAttributeList[0],list) == False):

                    """
                    if ('Distance' in col2):
                        print("extract dominant distance dissimilar")
                        print(communityMembers_interactionAttributeList)
                        print("\n")
                        return communityMembers_interactionAttributeList
                    else:
                        return statistics.mode(communityMembers_interactionAttributeList)
                    """

                    """

                    print("year explanation")
                    print(col2)
                    print("username: " + row['userNameAuxiliar'])
                    print("index: " + str(row['real_index']))
                    print("community: " + str(row['community']))
                    print("dominant artworks: " + str(row[col2]))
                    print("communityMemberIndexes: " + str(communityMemberIndexes))
                    print("communityMembers_interactionAttributeList")
                    print(communityMembers_interactionAttributeList)
                    print("communityMembers_validInteractionAttributeList")
                    print(communityMembers_validInteractionAttributeList)
                    print("\n")

                    """

                    # print("year explanation")
                    # print(col2)
                    # print("username: " + row['userNameAuxiliar'])
                    # print("index: " + str(row['real_index']))
                    # print("community: " + str(row['community']))
                    # print("dominant artworks: " + str(row[col2]))
                    # print("communityMemberIndexes: " + str(communityMemberIndexes))
                    # print("communityMembers_interactionAttributeList")
                    # print(communityMembers_interactionAttributeList)
                    # print("communityMembers_validInteractionAttributeList")
                    # print(communityMembers_validInteractionAttributeList)
                    # print("\n")
                    newList = []
                    for element in communityMembers_interactionAttributeList:
                        if (isinstance(element,dict)):
                            newList.extend(list(element.keys()))
                        elif (isinstance(element,str)):
                            newList.append(element)
                    communityMembers_interactionAttributeList = newList

                    """
                    # Flatten
                    np_array = np.asarray(communityMembers_interactionAttributeList, dtype=object)
                    communityMembers_interactionAttributeList = list(np.hstack(np_array))
                    """

                    # print("flatten")
                    # print(communityMembers_interactionAttributeList)

                    # print("communityMembers_validInteractionAttributeList")
                    # print(communityMembers_validInteractionAttributeList)
                    # print("\n")

                    if ('Distance' in col2):
                        # print("extract dominant distance dissimilar")
                        # print(communityMembers_interactionAttributeList)
                        # print("\n")
                        return communityMembers_interactionAttributeList
                    else:
                        return statistics.mode(communityMembers_interactionAttributeList)







                # iconclass attribute (OLD) Not used anymore
                else:

                    # print("else explanation")
                    # print(col2)
                    # print("username: " + row['userNameAuxiliar'])
                    # print("index: " + str(row['real_index']))
                    # print("community: " + str(row['community']))
                    # print("dominant artworks: " + str(row[col2]))
                    # print("communityMemberIndexes: " + str(communityMemberIndexes))
                    # print("communityMembers_interactionAttributeList")
                    # print(communityMembers_interactionAttributeList)
                    # print("communityMembers_validInteractionAttributeList")
                    # print(communityMembers_validInteractionAttributeList)
                    # print("\n")

                    communityMembers_validInteractionAttributeList = [x for x in communityMembers_interactionAttributeList if (isinstance(x,dict) == True or isinstance(x,list) == True) and len(x) > 0]
                    #intersection = communityMembers_validInteractionAttributeList[0]
                    result = []
                    for interactionAttribute in communityMembers_validInteractionAttributeList:
                        #print("interactionAttribute: " + str(interactionAttribute))
                        # intersection = set(intersection).intersection(interactionAttribute)
                        # Union without repetition
                        #intersection = list(set(intersection) | set(lst2))
                        # Union with repetition
                        result.extend(interactionAttribute)

                    # Return the 3 most frequent elements
                    #print("result: " + str(result))
                    result = self.getMostFrequentElementsList(result,5)
                    result = [ x['Number'] for x in result ]
                    
                    #print(row.index)
                    #print("row: " + str(row['userNameAuxiliar']) + " ; " + str(communityMembers_validInteractionAttributeList))
                    
                    # print
                    """
                    if (row['community'] == 6):
                        print("community 6")
                        print("communityMemberIndexes: " + str(communityMemberIndexes))
                        print("attribute list: " + str(communityMembers_interactionAttributeList))
                        print("index: " + str(row['real_index']))
                        print("userName: " + str(row['userNameAuxiliar']))
                        print("result: " + str(result))
                        print("\n")
                    """
                    
                    """
                    print("community: " + str(row['community']))
                    print("col2: " + str(col2))
                    print("index: " + str(row['real_index']))
                    print("userName: " + str(row['userNameAuxiliar']))
                    print("attribute list (not empty): " + str(communityMembers_interactionAttributeList))
                    print("valid ones: " + str(communityMembers_validInteractionAttributeList))
                    print("result: " + str(result))
                    print("\n")
                    """
                    
                    
                    #artworks = [row['iconclassArrayIDsDominantInteractionGenerated'][i] for i in communityMemberIndexes if row['iconclassArrayIDsDominantInteractionGenerated'][i] != '' and i != row['real_index']]
                    #print("dominant iconclassArrayIDs: " + str(row['iconclassArrayIDsDominantInteractionGenerated']))
                    #print("dominant iconclassArrayIDs community: " + str(artworks))
                    #print("\n")
                        
                        
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

            logger = getLogger(__name__)
            logger.error(traceback.format_exc())

            return ''
        
    
    def checkDictExplanation(self, communityMembers_validInteractionAttributeList):
        return len(communityMembers_validInteractionAttributeList) > 0 and isinstance(communityMembers_validInteractionAttributeList[0],list) == True and isinstance(communityMembers_validInteractionAttributeList[0][0],dict) == True

    def extractDominantAttributeDictExplanation(self, communityMembers_validInteractionAttributeList):
        # print("new iconclass generation")
        # # print(col2)
        # print(communityMembers_validInteractionAttributeList)
        # print("\n")
        
        """
        """

        #print("simplify iconclassArrayIDs")
        # First, create a combined dictionary containing all the arrays of pairs each iconclassIDs originates from
        iconclassDictionary = {}
        for interactionAttribute in communityMembers_validInteractionAttributeList:
            for interactionAttributeDict in interactionAttribute:
                for interactionAttributeKey in interactionAttributeDict:
                    if (interactionAttributeKey not in iconclassDictionary):
                        iconclassDictionary[interactionAttributeKey] = []
                    iconclassDictionary[interactionAttributeKey].append(interactionAttributeDict[interactionAttributeKey])
        """
        print("username: " + row['userNameAuxiliar'])
        print("index: " + str(row['real_index']))
        print("community: " + str(row['community']))
        print("dominant artworks: " + str(row[col2]))
        print("communityMemberIndexes: " + str(communityMemberIndexes))
        print("communityMembers_interactionAttributeList")
        print(communityMembers_interactionAttributeList)
        print("communityMembers_validInteractionAttributeList")
        print(communityMembers_validInteractionAttributeList)
        print("\n")
        """
        
        """
        print("new iconclass generation 2")
        print(iconclassDictionary)
        print("\n")
        """
        
        # Up to now, it also takes the number of times the artwork appears. 
        # For example, a iconclassID (lovers) may only be linked to La Sirena, but La Sirena is interacted 
        # with more times than any other artwork.

        # Now, consider the number of different artworks linked to the iconclass ID

        
        for iconclassID in iconclassDictionary:
            """
            print("iconclassDictionary " + "(" + str(iconclassID) + ")" )
            print(iconclassDictionary[iconclassID])
            """
            #iconclassDictionary[iconclassID]= list(set(iconclassDictionary[iconclassID]))

            set_of_jsons = {json.dumps(d, sort_keys=True) for d in iconclassDictionary[iconclassID]}
            iconclassDictionary[iconclassID] = [json.loads(t) for t in set_of_jsons]

            #iconclassDictionary[iconclassID] = [dict(t) for t in {tuple(d.items()) for d in iconclassDictionary[iconclassID]}]

            """
            print(iconclassDictionary[iconclassID])
            print("\n")
        
            """
        

        # Select x (5) keys with the highest number of results
        # using sorted() + join() + lambda
        # Sort dictionary by value list length
        sorted_iconclassDictionary = sorted(iconclassDictionary, key = lambda key: len(iconclassDictionary[key]))
        """
        print("sorted iconclass dictionary")
        print(sorted_iconclassDictionary)
        print("\n")
        """



        res = '#separator#'.join(sorted_iconclassDictionary)

        # From most frequent to less frequent
        result = res.split('#separator#')
        """
        print("iconclass")
        print("iconclass chosen")
        print(result)
        """

        result.reverse()

        """
        print(result)
        print("\n")
        """

        
        """
        print("result")
        print(result)
        print("\n")
        """

        # Get children associated to the keys 
        result2 = []
        result2 = {k:iconclassDictionary[k] for k in result[0:5:1] if k in iconclassDictionary}

        """
        print("community: " + str(row['community']))
        print("iconclassDictionary")
        print(iconclassDictionary)
        print("\n")
        print("result2")
        print(result2)
        print("\n")
        """


        # Next work: include the artworks these iconclass IDs originate from in the explanations

        """
        print("final result (simplify iconclass)")
        print(result2)
        print("\n")
        """

        return result2


        
    def is_explainable(self, community, answer_binary=False, percentage=1.0):
        try:
            explainable_community = False

            """
            print("is explainable columns")
            print(community.columns)
            print("\n")
            """

            # Users without community
            if (len(community) <= 1):
                explainable_community = True
            elif (self.correctCommunityCheck(community)):
            
                """
                print("is_explainable")
                print(community)
                print("\n")
                print("self.explanaible_attributes: " + str(self.explanaible_attributes))
                print("\n")
                """
                
                #for col in community.columns.values:
                for col2 in self.explanaible_attributes:
                    if col2 != 'community' and explainable_community == False:
                        if (self.explainInteractionAttributes()):
                            col = "community_" + col2
                        else:
                            #col = col2
                            col = "community_" + col2
                            
                        
                        print("is_explainable")
                        print("col: " + str(col))
                        print("community " + str(community['community'].to_list()[0]))
                        print(community[col])
                        print("dissimilar attributes")
                        print(self.dissimilar_attributes)
                        print("\n")
                        """   
                        """

                        
                        # https://www.alphacodingskills.com/python/notes/python-operator-bitwise-or-assignment.php
                        # (x |= y) is equivalent to (x = x | y)
                        explainableAttribute = False
                        if answer_binary:
                            explainableAttribute = (len(community[col]) * percentage)  <= community[col].sum()
                        else:
                            explainableAttribute = (len(community[col]) * percentage) <= community[col].value_counts().max()


                        # print("explainable attribute")
                        # print(explainableAttribute)
                        # print("\n")

                        # Apply dissimilar
                        # First approximation (most frequent value appears below the community similarity percentage)
                        
                        if (col2 in self.dissimilar_attributes):
                            

                            explainableAttribute = not explainableAttribute

                            # print("apply dissimilar explanation")
                            # print(explainableAttribute)
                            # print("(len(community[col]) * percentage)")
                            # print(str((len(community[col]) * percentage)))
                            # print("community[col].value_counts().max()")
                            # print(str(community[col].value_counts().max()))
                            # print("\n")


                            # # Second approximation
                            # # Calculate the similarity average of the community members based on [col2] attribute. 
                            # # If it is higher or equal to percentage, the community can be explained
                            # print("checking distance")
                            # print(list(community.columns))
                            # print(community[[col + 'Distance']])
                            # print("\n")

                            # # Now filter distance column using the community 
                            # #distanceList = community[col2 + 'DistanceDominantInteractionGenerated'].to_list()
                            # distanceList = community[col + 'Distance'].to_list()
                            # # Community only has one user (users without community)
                            # if (len(distanceList) <= 1):
                            #     explainableAttribute = True
                            # else:

                            #     print("distanceList")
                            #     print(distanceList)
                            #     print(str(len(distanceList)))
                            #     print(str(len(distanceList[0])))
                            #     print(str(len(community)))
                            #     print("\n")

                            #     np_array = np.asarray(distanceList, dtype=object)
                            #     distanceList_flatten = list(np.hstack(np_array)) #if (len(np_array) > 0)
                            #     print("distanceList_flatten")
                            #     print(distanceList_flatten)
                            #     print(str(len(distanceList_flatten)))
                            #     print("\n")

                            #     distanceCommunity = sum(distanceList_flatten)
                            #     print("distance comunity")
                            #     print(str(distanceCommunity))
                            #     print("\n")

                            #     numberDistance = max(1, len(distanceList_flatten))

                            #     distanceCommunity = distanceCommunity / numberDistance
                            #     print("distance comunity final")
                            #     print(str(distanceCommunity))
                            #     print("\n")

                            #     self.distanceCommunity = distanceCommunity

                            #     if (distanceCommunity <= percentage):
                            #         print("less percentage")
                            #         explainableAttribute = True
                            #     else:
                            #         explainableAttribute = False







                        """
                        # Second approximation (better, not yet implemented)
                        # Maximize a distance function between the different values of the attribute.
                        if (col2 in self.dissimilar_attributes):
                            # Perfect case example (emotions): community with only two opposite emotions (joy, sadness)
                            # Distance value: 1.0
                            # If there are equal number of joy and sadness, the distance is 0.5




                            # Pick an emotion, value (compute the dissimilarity between all of them)
                        """


                        explainable_community |= explainableAttribute

                        # print("explainable community")
                        # print(explainable_community)
                        # print("\n")

                        # if (explainable_community == False):
                        #     print("fail explain community")
                        #     print(community)
                        #     print("\n")

                        #     print(col)
                        #     print((len(community[col])))
                        #     print(percentage)
                        #     print((len(community[col]) * percentage))
                        #     print(community[col].value_counts().max())
                        #     print("end fail explain community")
                        #     print("\n")


            isExplainableResult = explainable_community

        except Exception as e:

            logger = getLogger(__name__)
            logger.error("Error determining the explainability of the following community")
            logger.error(community)
            logger.error(traceback.format_exc())

            isExplainableResult = True

        # print("is_explainable function")
        # print("correct community")
        # print(self.correctCommunityCheck(community))
        # print("community " + str(community['community'].tolist()[0]))
        # print(community['community_interest.itMakesMeThinkAbout.emotions'])
        # print("isExplainableResult")
        # print(isExplainableResult)
        # if (isExplainableResult == False):
        #     print("Cannot explain this community")
        # print("\n")



        return isExplainableResult
    
    # Explainable AND
    def is_explainableAND(self, community, answer_binary=False, percentage=1.0):
        explainable_community = False

        """
        print("is explainable columns")
        print(community.columns)
        print("\n")
        """

        # Users without community
        if (len(community) <= 1):
            explainable_community = True
        elif (self.correctCommunityCheck(community)):
        
            """
            print("is_explainable")
            print(community)
            print("\n")
            print("self.explanaible_attributes: " + str(self.explanaible_attributes))
            print("\n")
            """

            explainable_community = True

            
            #for col in community.columns.values:
            for col2 in self.explanaible_attributes:
                if col2 != 'community' and explainable_community == True:
                    if (self.explainInteractionAttributes()):
                        col = "community_" + col2
                    else:
                        #col = col2
                        col = "community_" + col2
                        
                    
                    print("is_explainable")
                    print("col: " + str(col))
                    print("community " + str(community['community'].to_list()[0]))
                    print(community[col])
                    print("dissimilar attributes")
                    print(self.dissimilar_attributes)
                    print("\n")
                    """   
                    """

                    
                    # https://www.alphacodingskills.com/python/notes/python-operator-bitwise-or-assignment.php
                    # (x |= y) is equivalent to (x = x | y)
                    explainableAttribute = False
                    if answer_binary:
                        explainableAttribute = (len(community[col]) * percentage)  <= community[col].sum()
                    else:
                        explainableAttribute = (len(community[col]) * percentage) <= community[col].value_counts().max()

                    # Apply dissimilar
                    # First approximation (most frequent value appears below the community similarity percentage)
                    
                    if (col2 in self.dissimilar_attributes):
                        

                        explainableAttribute = not explainableAttribute

                        print("apply dissimilar explanation")
                        print(explainableAttribute)
                        print("(len(community[col]) * percentage)")
                        print(str((len(community[col]) * percentage)))
                        print("community[col].value_counts().max()")
                        print(str(community[col].value_counts().max()))
                        print("\n")


                        # Second approximation
                        # Calculate the similarity average of the community members based on [col2] attribute. 
                        # If it is higher or equal to percentage, the community can be explained
                        print("checking distance")
                        print(list(community.columns))
                        print(community[[col + 'Distance']])
                        print("\n")

                        # Now filter distance column using the community 
                        #distanceList = community[col2 + 'DistanceDominantInteractionGenerated'].to_list()
                        distanceList = community[col + 'Distance'].to_list()
                        # Community only has one user (users without community)
                        if (len(distanceList) <= 1):
                            explainableAttribute = True
                        else:

                            print("distanceList")
                            print(distanceList)
                            print(str(len(distanceList)))
                            print(str(len(distanceList[0])))
                            print(str(len(community)))
                            print("\n")

                            np_array = np.asarray(distanceList, dtype=object)
                            distanceList_flatten = list(np.hstack(np_array)) #if (len(np_array) > 0)
                            print("distanceList_flatten")
                            print(distanceList_flatten)
                            print(str(len(distanceList_flatten)))
                            print("\n")

                            distanceCommunity = sum(distanceList_flatten)
                            print("distance comunity")
                            print(str(distanceCommunity))
                            print("\n")

                            distanceCommunity = distanceCommunity / len(distanceList_flatten)
                            print("distance comunity final")
                            print(str(distanceCommunity))
                            print("\n")

                            self.distanceCommunity = distanceCommunity

                            if (distanceCommunity <= percentage):
                                print("less percentage")
                                explainableAttribute = True
                            else:
                                explainableAttribute = False







                    """
                    # Second approximation (better, not yet implemented)
                    # Maximize a distance function between the different values of the attribute.
                    if (col2 in self.dissimilar_attributes):
                        # Perfect case example (emotions): community with only two opposite emotions (joy, sadness)
                        # Distance value: 1.0
                        # If there are equal number of joy and sadness, the distance is 0.5




                        # Pick an emotion, value (compute the dissimilarity between all of them)
                    """


                    explainable_community = explainableAttribute

                    if (explainable_community == False):
                        print("fail explain community")
                        print(community)
                        print("\n")

                        print(col)
                        print((len(community[col])))
                        print(percentage)
                        print((len(community[col]) * percentage))
                        print(community[col].value_counts().max())
                        print("end fail explain community")
                        print("\n")


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
        
            print("get community: " + str(id_community))
            
            community = self.communities.get_group(id_community)
            #community = self.simplifyInteractionAttributes(community, printing = False)

            community_user_attributes = community[self.user_attributes]

            community_data = {'name': id_community}
            community_data['percentage'] = str(percentage * 100) + " %"
            #community_data['members'] = list(community_user_attributes.index.values)
            community_data['members'] = community['userid'].tolist()
            
            community_data['data'] = community
            
            """
            print("self.communities")
            print(community[['userNameAuxiliar','community']])
            print("\n")
            
            

            print("Dominant artworks get_community (explanation)")
            print(community["community_" + "dominantArtworks"])
            print("\n")
            """             

            explainedCommunityProperties = dict()       

            #for col in community.columns.values:
            #for col2 in self.explanaible_attributes:
            community_attributes = list(set(self.explanaible_attributes + self.artwork_attributes))
            for col2 in community_attributes:
                if col2 != 'community':
                    if (self.explainInteractionAttributes()):
                        col = "community_" + col2
                    else:
                        #col = col2
                        col = "community_" + col2

                   # print(community)
                    #print(len(community[col]))
                    #print('-', col, community[col].value_counts().index[0])
                    if answer_binary:
                        if (len(community[col]) * percentage) <= community[col].sum():
                            explainedCommunityProperties[col] = community[col].value_counts().index[0]
                            
                            
                            
                            # print('-', col, community[col].value_counts().index[0])
                    else:
                    
                        array = community[col].tolist()   
                        array = [x for x in array if (isinstance(x,dict) == False or isinstance(x,list) == False) or len(x) > 0]
                             
                        # For iconclass (list) types
                        #if (len(community[col] > 0 and isinstance(community[col][0],list))):



                        
                        """
                        print("\n")
                        print(community[col])
                        print(col)
                        print(type(community[col]))
                        print(type(community[col][0]))
                        print("\n")
                        
                        
                        """
                        """
                        if (col2 == "Colour"):
                            print("colour column array")
                            print("id_community: " + str(id_community))
                            print("check array")
                            print(array)
                            print("\n")
                        """

                        # Generic for dict types (iconclass, ontology, artwork id)
                        """
                        print("checking array")
                        print(array)
                        print(type(array[0]))
                        print(isinstance(array[0],dict))
                        print("\n")
                        """

                        if (len(array) > 0 and isinstance(array[0],dict)):
                            """
                            print("improved explanation for dict type explanations")
                            print("col: " + str(col))
                            print("community")
                            print(community.columns)
                            print("\n")
                            print(community[['userNameAuxiliar',col]])
                            print("\n")

                            print(array)
                            print("\n")

                            print("end new dict type explanations")
                            print("\n")
                            """

                            # Example array
                            # [{}, {'31D1': [['31D15', '31D12']]}] (iconclass)
                            # 
                            # {'44174': ['44174']} (id)

                            # Combine all dictionaries inside the array into one dictionary
                            iconclassDictionary = {}
                            for dictionary in array:
                                for dictionaryKey in dictionary:
                                    if (dictionaryKey not in iconclassDictionary):
                                        iconclassDictionary[dictionaryKey] = []
                                    iconclassDictionary[dictionaryKey].extend(dictionary[dictionaryKey])

                            """
                            print("explanation combined dictionary")
                            print(iconclassDictionary)
                            print("\n")
                            """

                            if (col != "community_" + "id"):
                                for key in iconclassDictionary:
                                    # print("iconclassDictionary " + "(" + str(key) + ")" )
                                    # print(iconclassDictionary[key])
                                    #iconclassDictionary[iconclassID]= list(set(iconclassDictionary[iconclassID]))

                                    set_of_jsons = {json.dumps(d, sort_keys=True) for d in iconclassDictionary[key]}
                                    iconclassDictionary[key] = [json.loads(t) for t in set_of_jsons]

                                    #iconclassDictionary[iconclassID] = [dict(t) for t in {tuple(d.items()) for d in iconclassDictionary[iconclassID]}]


                                    print(iconclassDictionary[key])
                                    print("\n")
                                    """
                                    """

                            # Sort dictionary
                            res = '#separator#'.join(sorted(iconclassDictionary, key = lambda key: len(iconclassDictionary[key])))
                            result = res.split('#separator#')
                            result.reverse()

                            # Get x more frequent keys
                            result2 = []
                            result2 = {k:iconclassDictionary[k] for k in result[0:5:1] if k in iconclassDictionary}

                            result3 = {}

                            """
                            print("result2 dictionary")
                            print(iconclassDictionary)
                            print("\n")
                            

                            print("community: " + str(id_community))
                            print("iconclassDictionary explanation")
                            print(iconclassDictionary)
                            print("\n")
                            print("result2 explanation")
                            print(result2)
                            print("\n")
                            """

                            # Prepare explanation text for each of the selected keys
                            for iconclassID in result2:
                                # print("checking iconclass id " + str(iconclassID))
                                iconclassText = ""
                                if (col == "community_" + "iconclassArrayIDs"):
                                    iconclassText = self.daoAPI_iconclass.getIconclassText(iconclassID)

                                # Get array of dicts {key: iconclassID, value: artwork it originates from}
                                np_array = np.asarray(result2[iconclassID], dtype=object)
                                iconclassChildren = list(np.hstack(np_array))

                                # print("iconclass children")
                                # print(iconclassChildren)
                                # print("\n")

                                # basic explanation
                                #iconclassExplanation = str(iconclassID) + " " + iconclassText
                                iconclassExplanation = iconclassText + " " + "[" + str(iconclassID) + "]"
                                
                                artworksExplanation = []

                                # key includes children keys (dict value): iconclass, ontology
                                if (isinstance(iconclassChildren[0],dict) == True):

                                    # Group iconclassChildren into a combined dictionary (values with the same key are added to an array)
                                    iconclassChildrenCombinedDictionary = {}
                                    for dictionary in iconclassChildren:
                                        for key, value in dictionary.items():
                                            #print("key: " + str(key) + "\n" + "value: " + str(value))
                                            if (key not in iconclassChildrenCombinedDictionary):
                                                iconclassChildrenCombinedDictionary[key] = []
                                            iconclassChildrenCombinedDictionary[key].extend(value)
                                            iconclassChildrenCombinedDictionary[key] = list(set(iconclassChildrenCombinedDictionary[key]))

                                    """
                                    Same as artworksExplanation
                                    Remove redundant code later
                                    """
                                    artworks_iconclassID = []
                                    for iconclassChild in iconclassChildrenCombinedDictionary:
                                        artworks_iconclassID.extend(iconclassChildrenCombinedDictionary[iconclassChild])
                                    artworks_iconclassID = set(artworks_iconclassID)


                                    iconclassExplanation += " - Artworks: " + str(len(artworks_iconclassID))
                                    if (iconclassID in iconclassChildrenCombinedDictionary):
                                        # Instead of showing list artworks, just the number of them
                                        #iconclassExplanation += " (" + ", ".join(iconclassChildrenCombinedDictionary[iconclassID]) + ")"
                                        # iconclassExplanation += " - Artworks: " + str(len(artworks_iconclassID))

                                        artworksExplanation.extend(iconclassChildrenCombinedDictionary[iconclassID])
                                    iconclassChildrenText = []
                                    if (len(iconclassChildrenCombinedDictionary) > 1):
                                        # print("iconclass combined dictionary")
                                        # print(iconclassChildrenCombinedDictionary)
                                        # print("\n")

                                        #iconclassExplanation += ". Obtained from the artwork's materials: "
                                        iconclassExplanation += ". This identifier is the common parent of the following labels: "
                                        for iconclassChild in iconclassChildrenCombinedDictionary:
                                            iconclassChildText = ""
                                            # Iconclass: Get description of the iconclassID through the Iconclass API
                                            if (col == "community_" + "iconclassArrayIDs"):
                                                iconclassChildText = self.daoAPI_iconclass.getIconclassText(iconclassChild)
                                            # Instead of showing list artworks, just the number of them
                                            iconclassChildText += " (" + ", ".join(iconclassChildrenCombinedDictionary[iconclassChild]) + ")"
                                            #iconclassChildText += " - Artworks: " + str(len(iconclassChildrenCombinedDictionary[iconclassChild]))

                                            artworksExplanation.extend(iconclassChildrenCombinedDictionary[iconclassChild])
                                            #iconclassChildrenText.append(str(iconclassChild) + " " + iconclassChildText)
                                            iconclassChildrenText.append(iconclassChildText + " " + "[" + str(iconclassChild) + "]")
                                        iconclassExplanation += "; ".join(iconclassChildrenText)
                                        iconclassExplanation += ""

                                # key references a basic array value: artwork id
                                else:
                                    
                                    """
                                    
                                    print("list explanation")
                                    iconclassChildren = list(set(iconclassChildren))
                                    print("iconclass children")
                                    print(iconclassChildren)
                                    print("\n")
                                    iconclassChildrenCombinedDictionary = {iconclassChildren[0]: iconclassChildren}
                                    print("iconclass children combined dictionary")
                                    print(iconclassChildrenCombinedDictionary)
                                    print("\n")
                                    print("artworksExplanation")
                                    print(artworksExplanation)
                                    print("\n")
                                    artworksExplanation.extend(iconclassChildrenCombinedDictionary[iconclassID])
                                    print("artworksExplanation 2")
                                    print(artworksExplanation)
                                    print("\n")
                                    """
                                    #iconclassChildren = {}


                                """
                                print("iconclass children combined")
                                print(iconclassChildrenCombinedDictionary)
                                print("\n")
                                """
                                
                                
                                

                                #result3[iconclassExplanation] = 0.0
                                """
                                print("new dict explanation")
                                print(iconclassExplanation)
                                print(iconclassChildrenCombinedDictionary[iconclassID])
                                print("\n")
                                """
                                result3[iconclassExplanation] = list(set(artworksExplanation))
                                

                            # print("result3 dict explanation: " + str(result3))
                            
                            
                            #explainedCommunityProperties[col] = "\n".join(result2)
                            
                            explainedCommunityProperties[col] = dict()
                            explainedCommunityProperties[col]["label"] = 'Community representative properties of the implicit attribute ' + "(" + str(col2) + ")" + ":"
                            explainedCommunityProperties[col]["explanation"] = result3

                            

                        # For iconclass
                        elif (col == "community_" + "iconclassArrayIDs"):
                            print("improved explanation for iconclass")
                            print("\n")

                            print(array)
                            print("\n")

                            print("end new iconclass")
                            print("\n")

                            # Example array
                            # [{}, {'31D1': [['31D15', '31D12']]}]

                            # Combine all into one dictionary
                            iconclassDictionary = {}
                            for dictionary in array:
                                for dictionaryKey in dictionary:
                                    if (dictionaryKey not in iconclassDictionary):
                                        iconclassDictionary[dictionaryKey] = []
                                    iconclassDictionary[dictionaryKey].extend(dictionary[dictionaryKey])

                            # Sort dictionary
                            res = '#separator#'.join(sorted(iconclassDictionary, key = lambda key: len(iconclassDictionary[key])))
                            result = res.split('#separator#')
                            result.reverse()

                            # Get x more frequent keys
                            result2 = []
                            result2 = {k:iconclassDictionary[k] for k in result[0:5:1] if k in iconclassDictionary}

                            result3 = {}
                            for iconclassID in result2:
                                iconclassText = self.daoAPI_iconclass.getIconclassText(iconclassID)
                                # Get array of dicts {key: iconclassID, value: artwork it originates from}
                                np_array = np.asarray(result2[iconclassID], dtype=object)
                                iconclassChildren = list(np.hstack(np_array))

                                print("iconclass children")
                                print(iconclassChildren)
                                print("\n")

                                # Group iconclassChildren into a combined dictionary (values with the same key are added to an array)
                                iconclassChildrenCombinedDictionary = {}
                                for dictionary in iconclassChildren:
                                    for key, value in dictionary.items():
                                        if (key not in iconclassChildrenCombinedDictionary):
                                            iconclassChildrenCombinedDictionary[key] = []
                                        iconclassChildrenCombinedDictionary[key].extend(value)
                                        iconclassChildrenCombinedDictionary[key] = list(set(iconclassChildrenCombinedDictionary[key]))

                                print("iconclass children combined")
                                print(iconclassChildrenCombinedDictionary)
                                print("\n")
                                
                                iconclassExplanation = str(iconclassID) + " " + iconclassText 
                                if (iconclassID in iconclassChildrenCombinedDictionary):
                                    iconclassExplanation += " (" + ", ".join(iconclassChildrenCombinedDictionary[iconclassID]) + ")"
                                iconclassChildrenText = []
                                if (len(iconclassChildrenCombinedDictionary) > 1):
                                    print("iconclass combined dictionary")
                                    print(iconclassChildrenCombinedDictionary)
                                    print("\n")

                                    iconclassExplanation += ". Obtained from the artwork's iconclass IDs: "
                                    for iconclassChild in iconclassChildrenCombinedDictionary:
                                        iconclassChildText = self.daoAPI_iconclass.getIconclassText(iconclassChild)
                                        iconclassChildText += " (" + ", ".join(iconclassChildrenCombinedDictionary[iconclassChild]) + ")"
                                        iconclassChildrenText.append(str(iconclassChild) + " " + iconclassChildText)
                                    iconclassExplanation += "; ".join(iconclassChildrenText)
                                    iconclassExplanation += ""

                                result3[iconclassExplanation] = 0.0

                            print("result3: " + str(result3))
                            
                            
                            #explainedCommunityProperties[col] = "\n".join(result2)
                            
                            explainedCommunityProperties[col] = dict()
                            explainedCommunityProperties[col]["label"] = 'Community representative properties of the implicit attribute ' + "(" + str(col2) + ")" + ":"
                            explainedCommunityProperties[col]["explanation"] = result3

                        # For materials ontology
                        elif (col == "community_" + "Materials" and 1 == 2):
                            print("improved explanation for materials")
                            print("\n")

                            print(array)
                            print("\n")

                            print("end new materials")
                            print("\n")

                            # Example array
                            # [{}, {'31D1': [['31D15', '31D12']]}]

                            # Combine all into one dictionary
                            iconclassDictionary = {}
                            for dictionary in array:
                                for dictionaryKey in dictionary:
                                    if (dictionaryKey not in iconclassDictionary):
                                        iconclassDictionary[dictionaryKey] = []
                                    iconclassDictionary[dictionaryKey].extend(dictionary[dictionaryKey])

                            # Sort dictionary
                            res = '#separator#'.join(sorted(iconclassDictionary, key = lambda key: len(iconclassDictionary[key])))
                            result = res.split('#separator#')
                            result.reverse()

                            # Get x more frequent keys
                            result2 = []
                            result2 = {k:iconclassDictionary[k] for k in result[0:5:1] if k in iconclassDictionary}

                            result3 = {}
                            for iconclassID in result2:
                                iconclassText = ""
                                # Get array of dicts {key: iconclassID, value: artwork it originates from}
                                np_array = np.asarray(result2[iconclassID], dtype=object)
                                iconclassChildren = list(np.hstack(np_array))

                                print("iconclass children")
                                print(iconclassChildren)
                                print("\n")

                                # Group iconclassChildren into a combined dictionary (values with the same key are added to an array)
                                iconclassChildrenCombinedDictionary = {}
                                for dictionary in iconclassChildren:
                                    for key, value in dictionary.items():
                                        if (key not in iconclassChildrenCombinedDictionary):
                                            iconclassChildrenCombinedDictionary[key] = []
                                        iconclassChildrenCombinedDictionary[key].extend(value)
                                        iconclassChildrenCombinedDictionary[key] = list(set(iconclassChildrenCombinedDictionary[key]))

                                print("iconclass children combined")
                                print(iconclassChildrenCombinedDictionary)
                                print("\n")
                                
                                iconclassExplanation = str(iconclassID) + " " + iconclassText 
                                if (iconclassID in iconclassChildrenCombinedDictionary):
                                    iconclassExplanation += " (" + ", ".join(iconclassChildrenCombinedDictionary[iconclassID]) + ")"
                                iconclassChildrenText = []
                                if (len(iconclassChildrenCombinedDictionary) > 1):
                                    print("iconclass combined dictionary")
                                    print(iconclassChildrenCombinedDictionary)
                                    print("\n")

                                    iconclassExplanation += ". Obtained from the artwork's materials: "
                                    for iconclassChild in iconclassChildrenCombinedDictionary:
                                        iconclassChildText = ""
                                        iconclassChildText += " (" + ", ".join(iconclassChildrenCombinedDictionary[iconclassChild]) + ")"
                                        iconclassChildrenText.append(str(iconclassChild) + " " + iconclassChildText)
                                    iconclassExplanation += "; ".join(iconclassChildrenText)
                                    iconclassExplanation += ""

                                result3[iconclassExplanation] = 0.0

                            print("result3: " + str(result3))
                            
                            
                            #explainedCommunityProperties[col] = "\n".join(result2)
                            
                            explainedCommunityProperties[col] = dict()
                            explainedCommunityProperties[col]["label"] = 'Community representative properties of the implicit attribute ' + "(" + str(col2) + ")" + ":"
                            explainedCommunityProperties[col]["explanation"] = result3

                        # For id
                        elif (col == "community_" + "id" and 1 == 2):
                            print("improved explanation for id")
                            print("\n")

                            print(array)
                            print("\n")

                            print("end new id")
                            print("\n")

                            # Example array
                            # [{}, {'31D1': [['31D15', '31D12']]}]

                            # Combine all into one dictionary
                            iconclassDictionary = {}
                            for dictionary in array:
                                for dictionaryKey in dictionary:
                                    if (dictionaryKey not in iconclassDictionary):
                                        iconclassDictionary[dictionaryKey] = []
                                    iconclassDictionary[dictionaryKey].extend(dictionary[dictionaryKey])

                            """
                            print("iconclass dictionary id")
                            print(iconclassDictionary)
                            print("\n")
                            """

                            # Sort dictionary
                            res = '#separator#'.join(sorted(iconclassDictionary, key = lambda key: len(iconclassDictionary[key])))
                            result = res.split('#separator#')
                            result.reverse()

                            # Get x more frequent keys
                            result2 = []
                            result2 = {k:iconclassDictionary[k] for k in result[0:5:1] if k in iconclassDictionary}

                            result3 = {}
                            for iconclassID in result2:
                                iconclassText = ""
                                # Get array of dicts {key: iconclassID, value: artwork it originates from}
                                np_array = np.asarray(result2[iconclassID], dtype=object)
                                iconclassChildren = list(np.hstack(np_array))

                                """
                                print("iconclass children")
                                print(iconclassChildren)
                                print("\n")
                                """

                                iconclassExplanation = str(iconclassID) + " " + iconclassText 

                                if (isinstance(iconclassChildren[0],dict) == True):

                                    # Group iconclassChildren into a combined dictionary (values with the same key are added to an array)
                                    iconclassChildrenCombinedDictionary = {}
                                    for dictionary in iconclassChildren:
                                        for key, value in dictionary.items():
                                            if (key not in iconclassChildrenCombinedDictionary):
                                                iconclassChildrenCombinedDictionary[key] = []
                                            iconclassChildrenCombinedDictionary[key].extend(value)
                                            iconclassChildrenCombinedDictionary[key] = list(set(iconclassChildrenCombinedDictionary[key]))

                                    if (iconclassID in iconclassChildrenCombinedDictionary):
                                        iconclassExplanation += " (" + ", ".join(iconclassChildrenCombinedDictionary[iconclassID]) + ")"
                                        iconclassChildrenText = []
                                        if (len(iconclassChildrenCombinedDictionary) > 1):
                                            """
                                            print("iconclass combined dictionary")
                                            print(iconclassChildrenCombinedDictionary)
                                            print("\n")
                                            """

                                            iconclassExplanation += ". Obtained from the artwork's materials: "
                                            for iconclassChild in iconclassChildrenCombinedDictionary:
                                                iconclassChildText = ""
                                                iconclassChildText += " (" + ", ".join(iconclassChildrenCombinedDictionary[iconclassChild]) + ")"
                                                iconclassChildrenText.append(str(iconclassChild) + " " + iconclassChildText)
                                            iconclassExplanation += "; ".join(iconclassChildrenText)
                                            iconclassExplanation += ""

                                else:
                                    
                                    """
                                    """
                                    iconclassChildren = list(set(iconclassChildren))
                                    iconclassChildrenCombinedDictionary = {iconclassChildren[0]: iconclassChildren}
                                    
                                    #iconclassChildren = {}

                                """
                                print("iconclass children combined")
                                print(iconclassChildrenCombinedDictionary)
                                print("\n")
                                """
                                
                                
                                

                                #result3[iconclassExplanation] = 0.0
                                result3[iconclassExplanation] = iconclassChildrenCombinedDictionary[iconclassID]

                            print("result3: " + str(result3))
                            
                            
                            #explainedCommunityProperties[col] = "\n".join(result2)
                            
                            explainedCommunityProperties[col] = dict()
                            explainedCommunityProperties[col]["label"] = 'Community representative properties of the implicit attribute ' + "(" + str(col2) + ")" + ":"
                            explainedCommunityProperties[col]["explanation"] = result3

                        # For list types (artworks and iconclass)
                        elif (len(array) > 0 and isinstance(array[0],list)):
                            
                            
                            """
                            print("\n")
                            print("iconclass list type")
                            print(community[col])
                            print(array)
                            print("\n\n\n")
                            
                            
                            
                            """
                            
                            np_array = np.asarray(array, dtype=object)
                            
                            """
                            print("shape")
                            print(np_array.shape)
                            print(np.hstack(np_array))
                            
                            """
                            #array2 = list(np_array.flat)
                            array2 = list(np.hstack(np_array))
                            
                            #print("array2: " + str(array2))
                            
                            result = self.getMostFrequentElementsList(array2,5)
                            result = [ x['Number'] for x in result ]
                            
                            result2 = {}
                            
                            """
                            print("result: " + str(result))
                            
                            
                            print("before entering iconclass extra functionality")
                            print(col)
                            print("\n")
                            
                            
                            
                            
                            print("before entering iconclass extra functionality")
                            print(col)
                            print("\n")

                            """
                            
                            # Iconclass attribute
                            if (col == "community_" + "iconclassArrayIDs"):
                                for iconclassID in result:
                                    iconclassText = self.daoAPI_iconclass.getIconclassText(iconclassID)
                                    result2[str(iconclassID) + " " + iconclassText] = 0.0
                            # Other array attributes
                            else:
                                for element in result:
                                    result2[str(element)] = 0.0
                            
                            #result2.append(str(array) + " " + "0.0")
                                
                            print("result2: " + str(result2))
                            
                            
                            #explainedCommunityProperties[col] = "\n".join(result2)
                            
                            explainedCommunityProperties[col] = dict()
                            explainedCommunityProperties[col]["label"] = 'Community representative properties of the implicit attribute ' + "(" + str(col2) + ")" + ":"
                            explainedCommunityProperties[col]["explanation"] = result2
                            
                            
                            
                        
                        # For string types
                        else:

                            print("is explainable get community")

                            #explainableAttribute = self.is_explainable(community, answer_binary, percentage)

                            """

                            explainableAttribute = (len(community[col]) * percentage) <= community[col].value_counts().max()
                            if (col2 in self.dissimilar_attributes):
                                explainableAttribute = not explainableAttribute

                            """

                            # Returns dominant one
                            # explainedCommunityProperties[col] = community[col].value_counts().index[0]

                            # Remove empty string
                            df = community.copy()
                            if (is_numeric_dtype(df[col])):
                                df[col] = df[col].astype(str)
                            #df2 = df.loc[ df[col].str.len() != 0 ]
                            df[col] = df[col].replace(['', 'unknown'], 'unknown')
                            df2 = df.copy()
                            percentageColumn = df2[col].value_counts(normalize=True) * 100
                            percentageColumnDict = percentageColumn.to_dict()

                            # Returns the values for each of them
                            """
                            percentageColumn = community[col].value_counts(normalize=True) * 100
                            percentageColumnDict = percentageColumn.to_dict()
                            """

                            """
                            print("community col")
                            print(community[col])
                            print("percentageColumn")
                            print(percentageColumn)
                            print("percentageColumnDict")
                            print(percentageColumnDict)
                            print("\n")
                            """
                            
                            explainedCommunityProperties[col] = dict()
                            explainedCommunityProperties[col]["label"] = 'Percentage distribution of the implicit attribute ' + "(" + str(col2) + ")" + ":"
                            #if (not explainableAttribute):
                                #explainedCommunityProperties[col]["label"] += "(This community doesn't meet the dissimilar requirements) :"
                            #explainedCommunityProperties[col]["label"] += "distanceCommunity: " + str(self.distanceCommunity)
                            explainedCommunityProperties[col]["explanation"] = percentageColumnDict

                            
                            """
                            
                            if (col2 == "Colour"):
                                print("colour error")
                                print("id_community: " + str(id_community))
                                print(col)
                                print(col2)
                                print(percentageColumn)
                                print(percentageColumn.to_string())
                                print("end colour error")
                                print("\n\n")
                            """
                            
                            
            # Second explanation  
            #print(explainedCommunityProperties)    
            """
            community_data['explanation'] = []
            community_data['explanation'].append(explainedCommunityProperties)
            """
            
            community_data['explanation'] = explainedCommunityProperties
            
            
            #community_data['explanation'].append(self.secondExplanation(community))
            
        except Exception as e:
            
            print(str(e))
            print(self.communities)
            print("\n")
            # data with communities
            print(self.complete_data)
            print("\n\n")
            print("algorithm result")
            print(self.resultAlgorithm)
            print(self.idsCommunities)
            print("Exception retrieving community " + str(id_community))
            print("\n")

            logger = getLogger(__name__)
            logger.error(traceback.format_exc())

            #raise Exception("Exception retrieving community " + str(id_community))

            
            explainedCommunityProperties[col] = dict()
            explainedCommunityProperties[col]["label"] = 'Community representative properties of the implicit attribute ' + "(" + str(col2) + ")" + ":"
            explainedCommunityProperties[col]["explanation"] = {}

            community_data['explanation'] = explainedCommunityProperties
            
    
            
        return community_data
    
    
    
        