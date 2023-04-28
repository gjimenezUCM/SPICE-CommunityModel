
from cmSpice.dao.dao_db_users import DAO_db_users
from cmSpice.dao.dao_db_communities import DAO_db_community

from cmSpice.utils.dataLoader import DataLoader

import pandas as pd

import json
import copy

from cmSpice.core.communityModel import CommunityModel

from itertools import combinations_with_replacement

# ------------------
# logger
import logging
import traceback
from cmSpice.logger.logger import getLogger

logger = getLogger(__name__)
# ------------------

class ExplicitCommunityJSONGenerator:

    def __init__(self):
        self.dao = DAO_db_users()

        route = DataLoader.fileRoute('seedFile.json')

        if route:
            file = open(route)
            self.seedFile = json.load(file)
            file.close()
        else:
            self.seedFile = {}

    def generate(self):
        try:

            self.data = self.dao.getPandasDataframe()

            for citizenAttribute in self.seedFile["user_attributes"]:
                self.citizenAttribute_name = citizenAttribute["att_name"]
                if (self.citizenAttribute_name in self.data.columns):
                    self.citizenAttribute_values = pd.unique(self.data[self.citizenAttribute_name]).tolist()
                    
                    # Set the community labels
                    # self.data['group'] = communityDict['users'].values()
                    self.data['group'] = self.data.apply(lambda row: self.citizenAttribute_values.index(row[self.citizenAttribute_name]), axis = 1)
                    # Set other visualization attributes
                    self.data["id"] = self.data["userid"]
                    self.data["label"] = self.data["userid"]
                    self.data['explicit_community'] = self.data[[self.citizenAttribute_name]].to_dict(orient='records')
                    self.data["implicit_community"] = [{} for _ in range(len(self.data))]
                    self.data["community_interactions"] = [{} for _ in range(len(self.data))]
                    self.data["no_community_interactions"] = [{} for _ in range(len(self.data))]

                    # Generate JSON
                    self.communityJson = {}

                    self.communityJSON(self.citizenAttribute_name)
                    self.userJSON()
                    self.similarityJSON(self.citizenAttribute_name)
                    self.interactionObjectJSON()

                    # Save it in the database
                    self.saveDatabase(self.communityJson)

        except Exception as e:

            logger.error(traceback.format_exc())

    def communityJSON(self, citizenAttribute):
        # Community Data 
        self.communityJson['name'] = citizenAttribute
        self.communityJson['perspectiveId'] = citizenAttribute
        self.communityJson['communities'] = []
        
        self.implicitExplanationJSON(citizenAttribute)

    def implicitExplanationJSON(self, citizenAttribute):
        for i in range(len(self.citizenAttribute_values)):
            communityDictionary = {}
            communityDictionary['id'] = self.communityJson['name'] + "-" + str(len(self.communityJson['communities']))
            communityDictionary['perspectiveId'] = self.communityJson['name'] 
            communityDictionary['community-type'] = 'explicit'
            communityDictionary['name'] = 'Community ' + str(len(self.communityJson['communities'])) + " - " + str(self.citizenAttribute_values[i])

            # Explanations
            communityDictionary['explanations'] = []

            # Users
            communityDictionary['users'] = self.data.loc[self.data[citizenAttribute] == self.citizenAttribute_values[i]]['userid'].tolist()

            self.communityJson['communities'].append(communityDictionary)

    def userJSON(self):
        self.communityJson['users'] = self.data[['id','label','group','explicit_community', 'implicit_community', 'community_interactions', 'no_community_interactions']].to_dict('records')
        
    def similarityJSON(self, citizenAttribute):
        self.communityJson['similarity'] = []


        users = self.data.index
        pairs = combinations_with_replacement(range(len(users)), r=2)

        for p in pairs:
            if (p[0] != p[1]):
                userA = self.data.loc[p[0]]['userid'] 
                userB = self.data.loc[p[1]]['userid']

                attributeA = self.data.loc[p[0]][citizenAttribute] 
                attributeB = self.data.loc[p[1]][citizenAttribute]

                similarity = 1
                if (attributeA != attributeB):
                    similarity = 0

                dicti = {}
                dicti['u1'] = str(userA)
                dicti['u2'] = str(userB)
                dicti['value'] = round(similarity,2)
                self.communityJson['similarity'].append(dicti)           

    def interactionObjectJSON(self):
        self.communityJson['artworks'] = []


# --------------------------------------------------------------------------------------------------------------------------
#    Community jsons (visualization)
# --------------------------------------------------------------------------------------------------------------------------

    def saveDatabase(self, jsonCommunity):
        # Store community data
        daoCommunityModelCommunity = DAO_db_community()
        # drop previous data
        daoCommunityModelCommunity.drop(
            {'perspectiveId': jsonCommunity['perspectiveId']})
        daoCommunityModelCommunity.dropFullList(
            {'perspectiveId': jsonCommunity['perspectiveId']})
        # daoCommunityModelCommunity.dropFullList()

        # # humanize some keys and values
        # self.jsonCommunity = copy.deepcopy(jsonCommunity)
        # communityModel = CommunityModel({})
        # humanizedJsonCommunity = communityModel.humanizator(jsonCommunity)

        humanizedJsonCommunity = jsonCommunity
        # add new data
        daoCommunityModelCommunity.insertFileList("", humanizedJsonCommunity)

        logger.info("explicit community json data saved")
