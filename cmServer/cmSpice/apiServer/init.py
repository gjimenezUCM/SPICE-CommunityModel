# python modules


from bson.json_util import dumps, loads
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ForkingMixIn
from bson.objectid import ObjectId
import json
import time
import logging

# local modules
from cmSpice.dao.dao_db import DAO_db
from cmSpice.dao.dao_db_users import DAO_db_users
from cmSpice.dao.dao_db_communities import DAO_db_community
from cmSpice.dao.dao_db_similarities import DAO_db_similarity
from cmSpice.dao.dao_db_perspectives import DAO_db_perspectives
from cmSpice.dao.dao_db_flags import DAO_db_flags
from cmSpice.dao.dao_db_distanceMatrixes import DAO_db_distanceMatrixes
from cmSpice.dao.dao_db_artworkDistanceMatrixes import DAO_db_artworkDistanceMatrixes
from cmSpice.dao.dao_db_interactionDistances import DAO_db_interactionDistances

from cmSpice.dao.dao_json import DAO_json

from cmSpice.core.communityModel import CommunityModel
from cmSpice.core.communitiesSimilarityModel import CommunitiesSimilarityModel

from cmSpice.utils.dataLoader import DataLoader


def removeData():
    daoP = DAO_db_perspectives()
    daoP.drop()
    daoC = DAO_db_community()
    daoC.drop()
    daoC.dropFullList()
    daoS = DAO_db_similarity()
    daoS.drop()


def importData():
    json5 = DAO_json("app/cmSpice/api_server/data/5.json").getData()
    json6 = DAO_json("app/cmSpice/api_server/data/6.json").getData()

    daoC = DAO_db_community()
    daoC.insertFileList("5", json5)
    daoC.insertFileList("6", json6)

    # jsonAll = DAO_json("app/cmSpice/api_server/data/Allperspectives.json").getData()
    # daoP = DAO_db_perspectives()
    # daoP.insertPerspective(jsonAll)


def clearDatabase():
    print("1")
    daoF = DAO_db_flags()
    print("1a")
    # flags = daoF.getFlags()
    # print(flags)
    daoF.drop()

    print("2")
    daoC = DAO_db_community()
    daoC.drop()
    daoC.dropFullList()

    print("3")
    daoU = DAO_db_users()
    daoU.drop()

    print("4")
    daoDistanceMatrixes = DAO_db_distanceMatrixes()
    daoDistanceMatrixes.drop()

    daoArtworkDistanceMatrixes = DAO_db_artworkDistanceMatrixes()
    daoArtworkDistanceMatrixes.drop()

    daoInteractionDistances = DAO_db_interactionDistances()
    daoInteractionDistances.drop()

    print("5")
    daoSimilarities = DAO_db_similarity()
    daoSimilarities.drop()

    daoPerspectives = DAO_db_perspectives()
    daoPerspectives.drop()


def initializeDatabase():
    daoPerspectives = DAO_db_perspectives()
    daoPerspectives.drop()

    route = DataLoader().fileRoute("perspectives/HECHT/hecht agglomerative.json")
    # route = DataLoader().fileRoute("perspectives/GAM/GAM similar user emotions in similar artworks (iconclass) annotated-stories.json")
    file = open(route)
    perspectives = json.load(file)
    print(perspectives)
    file.close()

    daoPerspectives.insertPerspective(perspectives)


def importDatabase():
    route = DataLoader().fileRoute("databases/database.json")
    file = open(route)
    database = json.load(file)

    for key in database:
        for data in database[key]:
            data.pop("_id", "")

    # daos
    daoFlags = DAO_db_flags()
    daoSimilarities = DAO_db_similarity()
    daoCommunities = DAO_db_community()
    daoUsers = DAO_db_users()
    daoPerspectives = DAO_db_perspectives()
    daoMatrixes = DAO_db_distanceMatrixes()

    # daoFlags.insertFlag(database['flags'])
    # daoSimilarities.insertSimilarity(database['similarities'])
    for data in database['communitiesVisualization']:
        daoCommunities.insertFileList("", data)
    daoUsers.insertUser(database['users'])
    daoPerspectives.insertPerspective(database['perspectives'])
    daoMatrixes.insertDistanceMatrix(database['distanceMatrixes'])