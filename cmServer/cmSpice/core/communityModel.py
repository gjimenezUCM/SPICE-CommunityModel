
# --------------------------------------------------------------------------------------------------------------------------
#    Python libraries
# --------------------------------------------------------------------------------------------------------------------------

import os
import pandas as pd
import numpy as np
import importlib
import json

from inspect import getsourcefile
from os.path import abspath
import sys

# --------------------------------------------------------------------------------------------------------------------------
#    Custom Class
# --------------------------------------------------------------------------------------------------------------------------


# Community model tools
from cmSpice.core.communityJsonGenerator import CommunityJsonGenerator

# Community detection
from cmSpice.algorithms.clustering.explainedCommunitiesDetection import ExplainedCommunitiesDetection

# similarity measures
from cmSpice.algorithms.similarity.complexSimilarityDAO import ComplexSimilarityDAO
from cmSpice.algorithms.similarity.interactionSimilarityDAO import InteractionSimilarityDAO

# dao
from cmSpice.dao.dao_csv import DAO_csv
from cmSpice.dao.dao_json import DAO_json
from cmSpice.dao.dao_db_users import DAO_db_users
from cmSpice.dao.dao_db_distanceMatrixes import DAO_db_distanceMatrixes
from cmSpice.dao.dao_db_communities import DAO_db_community
from cmSpice.dao.dao_db_similarities import DAO_db_similarity

# ------------------
# logger
# usar todo este codigo en cada fichero donde se quiera hacer log
import logging
import logging.config
from cmSpice.logger.mongoLogger import MongoHandler

logging.basicConfig(level=logging.INFO)
logging.config.fileConfig('cmSpice/logger/logging.ini',
                          disable_existing_loggers=False)
log = logging.getLogger(__name__)
log.addHandler(MongoHandler(collection=os.environ['DB_LOG_COLLECTION'],
                            host=os.environ['DB_HOST'],
                            db_name=os.environ['DB_NAME'],
                            username=os.environ['DB_USER'],
                            password=os.environ['DB_PASSWORD'],
                            port=os.environ['DB_PORT']))
# ------------------


# --------------------------------------------------------------------------------------------------------------------------
#    Class
# --------------------------------------------------------------------------------------------------------------------------


class CommunityModel():

    def __init__(self, perspective, updateUsers=[]):
        """
        Construct of Community Model objects.

        Parameters
        ----------
            perspective: perspective object. Composed by:
                id, name
                algorithm: name and parameters
                similarity_functions: name, attribute, weight
            flag: flag object. Composed by:
                perspectiveId
                userid: user to update
        """
        self.perspective = perspective
        self.updateUsers = updateUsers
        self.percentageExplainability = 0.5

    def start(self):

        log.info("update started")

        # Perspective was not found
        if (len(self.perspective) <= 0):
            return

        """
        if (self.flag['userid'] == ""):
            print("not doing the one that is added by default")
            return
        """

        self.similarityMeasure = self.initializeComplexSimilarityMeasure()
        self.distanceMatrix = self.computeDistanceMatrix()
        self.clustering()

    def getData(self):
        return self.similarityMeasure.data

    def initializeComplexSimilarityMeasure(self):
        """
        Initializes the complex similarity measure associated to the given perspective

        Parameters
        ----------

        Returns
        -------
            similarityMeasure: ComplexSimilarityDAO
        """
        print("initialize complex similarity")
        print(self.perspective)
        print(self.perspective['similarity_functions'])
        daoCommunityModel = DAO_db_users()
        # If there are interaction_features use interactionSimilarityDAO
        if (len(self.perspective['interaction_similarity_functions']) > 0):
            similarityMeasure = InteractionSimilarityDAO(
                daoCommunityModel, self.perspective)
        # Otherwise use complexSimilarityDAO
        else:
            print("there are not interactions HECHT")
            similarityDict = self.perspective['similarity_functions']
            similarityMeasure = ComplexSimilarityDAO(
                daoCommunityModel, similarityDict)

        print("similarity measure: " + str(type(similarityMeasure)))

        return similarityMeasure

    def computeDistanceMatrix(self):
        """
        Method to calculate the distance matrix between all elements included in data.

        Parameters
        ----------

        Returns
        -------
            distanceMatrix: np.ndarray
        """

        # Load previous distance matrix
        daoDistanceMatrixes = DAO_db_distanceMatrixes()
        distanceMatrixJSON = daoDistanceMatrixes.getDistanceMatrix(
            self.perspective['id'])
        if (len(distanceMatrixJSON) == 0):
            distanceMatrix = np.empty([0, 0])
        else:
            distanceMatrix = np.asarray(distanceMatrixJSON['distanceMatrix'])

        # Update distance matrix for all users (recalculate distance matrix)
        # if ("flagAllUsers" in self.updateUsers and distanceMatrix.shape[0] == 0):
        if ("flagAllUsers" in self.updateUsers):
            distanceMatrix = self.similarityMeasure.matrix_distance()
        # Update distance matrix for a user
        else:
            distanceMatrix = self.similarityMeasure.updateDistanceMatrix(
                self.updateUsers, distanceMatrix)

        print(distanceMatrix)

        # Drop irrelevant parameters to explain communities
        #self.similarityMeasure.data.drop(['origin','source_id', '_id'], axis=1, inplace=True)

        # They are useful now
        #self.similarityMeasure.data.drop(['origin','source_id'], axis=1, inplace=True)
        #self.similarityMeasure.data = self.similarityMeasure.data.rename(columns={"userid":"user"})

        # return self.similarityMeasure.distanceMatrix
        return distanceMatrix

    def clusteringOLD(self):
        """
        Performs clustering using the distance matrix and the algorithm specified by the perspective object.

        Parameters
        ----------

        """
        percentageDefault = 0.78
        percentageDefault = 0.5

        algorithmName = self.perspective['algorithm']['name'] + \
            "CommunityDetection"
        algorithmFile = "cmSpice.algorithms.clustering." + algorithmName
        algorithmModule = importlib.import_module(algorithmFile)
        algorithmClass = getattr(
            algorithmModule, algorithmName[0].upper() + algorithmName[1:])

        community_detection_df = self.similarityMeasure.data.set_index('user')

        distanceMatrix = self.self.similarityMeasure.distanceMatrix
        community_detection = ExplainedCommunitiesDetection(
            algorithmClass, community_detection_df, distanceMatrix, self.perspective)

        n_communities, users_communities, self.medoids_communities = community_detection.search_all_communities(
            percentage=percentageDefault)

        hecht_beliefR_pivot_df2 = community_detection_df.copy()
        hecht_beliefR_pivot_df2['community'] = users_communities.values()
        hecht_beliefR_pivot_df2.reset_index(inplace=True)
        hecht_beliefR_pivot_df2

        # Export to json
        self.exportCommunityClusteringJSON(
            hecht_beliefR_pivot_df2, community_detection, n_communities, percentageDefault, distanceMatrix)

    def clusteringExportFileRoute(self, percentageExplainability, algorithmName):
        abspath = os.path.dirname(__file__)
        #relpath = "clustering/" + self.perspective['name'] + " " + "(" + self.perspective['algorithm']['name'] + ")"
        #relpath = "clustering/" + '(GAMGame_stories_RN_UNITO) ' + self.perspective['name'] + " "
        # relpath = "clustering/" + '(GAM RN) ' + self.perspective['name'] + " "
        relpath = "clustering/"
        #relpath += "clusters generated/" + self.perspective["algorithm"]["name"] + "/"
        # relpath += "clusters Mine/" + self.perspective["algorithm"]["name"] + "/"

        print("clustering export file route")

        relpath += self.perspective['name'].replace(
            "Similar-", "S-").replace("Same-", "E-") + " "
        if algorithmName != "agglomerative":
            relpath += str(algorithmName) + " "
        relpath += "(" + str(percentageExplainability) + ")"

        relpath += ".json"
        route = os.path.normpath(os.path.join(abspath, relpath))

        return route

    def clusteringOLD(self, exportFile="clustering.json"):
        """
        Performs clustering using the distance matrix and the algorithm specified by the perspective object.

        Parameters
        ----------
            percentageExplainability: minimum percentage of the most frequent value among 1+ main similarity features.

        """
        percentageExplainability = self.percentageExplainability

        # Initialize data
        algorithm = self.initializeAlgorithm()
        data = self.similarityMeasure.data
        data = data.set_index('userid')

        #interactionObjectData = self.similarityMeasure.getInteractionObjectData()
        interactionObjectData = pd.DataFrame()

        # Get results
        community_detection = ExplainedCommunitiesDetection(
            algorithm, data, self.distanceMatrix, self.perspective)
        communityDict = community_detection.search_all_communities(
            percentage=percentageExplainability)
        communityDict['perspective'] = self.perspective

        # Export to json
        data.reset_index(inplace=True)
        exportFile = self.clusteringExportFileRoute(percentageExplainability)
        jsonGenerator = CommunityJsonGenerator(
            interactionObjectData, data, self.distanceMatrix, communityDict, community_detection, self.perspective)
        jsonCommunity = jsonGenerator.generateJSON(exportFile)

        # Save data to database
        insertedId = self.saveDatabase(jsonCommunity)

        return insertedId

    def clustering(self, exportFile="clustering.json"):
        """
        Performs clustering using the distance matrix and the algorithm specified by the perspective object.

        Parameters
        ----------
            percentageExplainability: minimum percentage of the most frequent value among 1+ main similarity features.

        """
        jsonCommunity = self.performClustering(exportFile)
        return self.saveDatabase(jsonCommunity)

    def performClustering(self, exportFile="clustering.json"):
        percentageExplainability = self.percentageExplainability

        # Initialize data
        algorithm = self.initializeAlgorithm()
        data = self.similarityMeasure.data

        print("perform clustering data")
        print("data columns:")
        print(list(data.columns))
        print("\n")
        print("data")
        print(data)
        print("\n")

        # For debugging (delete later)
        data['userNameAuxiliar'] = data['userid']
        data['real_index'] = data.index

        # Set index to userName to use in visualization
        data = data.set_index('userid')

        if (self.containsInteractions()):
            interactionObjectData = self.similarityMeasure.getInteractionObjectData()
        else:
            interactionObjectData = pd.DataFrame()

        # Get results
        community_detection = ExplainedCommunitiesDetection(
            algorithm, data, self.distanceMatrix, self.perspective)
        communityDict = community_detection.search_all_communities(
            percentage=percentageExplainability)
        communityDict['perspective'] = self.perspective

        # Export to json
        data.reset_index(inplace=True)
        exportFile = self.clusteringExportFileRoute(
            percentageExplainability, self.perspective['algorithm']['name'])
        jsonGenerator = CommunityJsonGenerator(
            interactionObjectData, data, self.distanceMatrix, communityDict, community_detection, self.perspective)
        jsonCommunity = jsonGenerator.generateJSON(exportFile)

        return jsonCommunity

    def initializeAlgorithm(self):
        algorithmName = self.perspective['algorithm']['name'] + \
            "CommunityDetection"
        algorithmFile = "cmSpice.algorithms.clustering." + algorithmName
        algorithmModule = importlib.import_module(algorithmFile)
        algorithmClass = getattr(
            algorithmModule, algorithmName[0].upper() + algorithmName[1:])

        return algorithmClass


# --------------------------------------------------------------------------------------------------------------------------
#    Community jsons (visualization)
# --------------------------------------------------------------------------------------------------------------------------

    def saveDatabase(self, jsonCommunity):
        """
        daoCommunityModelVisualization = DAO_visualization()
        daoCommunityModelVisualization.drop()
        daoCommunityModelVisualization.insertJSON(jsonCommunity)
        """

        # Store distance matrix data
        # https://pynative.com/python-serialize-numpy-ndarray-into-json/
        daoDistanceMatrixes = DAO_db_distanceMatrixes()
        # daoDistanceMatrixes.drop()
        daoDistanceMatrixes.updateDistanceMatrix(
            {'perspectiveId': self.perspective['id'], 'distanceMatrix': self.similarityMeasure.distanceMatrix.tolist()})

        # Store community data
        daoCommunityModelCommunity = DAO_db_community()
        # drop previous data
        daoCommunityModelCommunity.drop(
            {'perspectiveId': self.perspective['id']})
        daoCommunityModelCommunity.dropFullList(
            {'perspectiveId': self.perspective['id']})
        # daoCommunityModelCommunity.dropFullList()

        # humanize some keys and values
        humanizedJsonCommunity = self.humanizator(jsonCommunity)
        # add new data
        daoCommunityModelCommunity.insertFileList("", humanizedJsonCommunity)

        log.info("json data saved")

# --------------------------------------------------------------------------------------------------------------------------
#   Auxiliar function
# --------------------------------------------------------------------------------------------------------------------------

    def containsInteractions(self):
        return len(self.perspective['interaction_similarity_functions']) > 0

# ---
#   Humanizator (rename keys, values)
# ---

    def renameValues(self, my_dict, humanizator):
        for e in humanizator:
            for path in e.keys():
                self.drill_down(my_dict, path.split(), e[path])
        return my_dict

    def drill_down(self, obj, path, value):
        if len(path) == 1:
            if isinstance(obj, dict):
                for key in obj.keys():
                    if key == path[0] and not isinstance(obj[key], dict) and obj[key] in value:
                        obj[path[0]] = value[obj[path[0]]]
            elif isinstance(obj, list):
                for elem in obj:
                    #elem = drill_down(elem, path, value)
                    for key in elem.keys():
                        if key == path[0] and elem[key] in value:
                            elem[path[0]] = value[elem[path[0]]]
            elif obj[path[0]] in value:
                obj[path[0]] = value[obj[path[0]]]

        else:
            if isinstance(obj, dict):
                obj[path[0]] = self.drill_down(obj[path[0]], path[1:], value)
            elif isinstance(obj, list):
                for elem in obj:
                    elem = self.drill_down(elem[path[0]], path[1:], value)
            return obj

    def renameKeys(self, my_dict, humanizator):
        if isinstance(my_dict, dict):
            for key in list(my_dict.keys()):
                if key in humanizator:
                    my_dict[humanizator[key]] = self.renameKeys(
                        my_dict.pop(key), humanizator)
                else:
                    my_dict[key] = self.renameKeys(
                        my_dict.pop(key), humanizator)
        elif isinstance(my_dict, list):
            for e in my_dict:
                self.renameKeys(e, humanizator)
        return my_dict

    def humanizator(self, jsonCommunity):
        # open all files inside /humanizator dir
        dict2Use = "dict"

        dir = "cmSpice/core/humanizator/"
        dictsList = []
        # for filename in os.listdir(dir):
        #    f =  open(dir + "/" + filename)

        f = open(dir + dict2Use + ".json")
        humanizator = json.load(f)

        newJsonCommunity = self.renameValues(
            jsonCommunity, humanizator["values"])
        newJsonCommunity = self.renameKeys(
            newJsonCommunity, humanizator["keys"])

        return newJsonCommunity
