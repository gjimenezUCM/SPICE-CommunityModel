# python modules
import os
import pymongo
from bson.json_util import dumps, loads
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ForkingMixIn
from bson.objectid import ObjectId
import json
import time
import logging
import traceback

# local modules
from cmSpice.dao.dao_db import DAO_db
from cmSpice.dao.dao_db_users import DAO_db_users
from cmSpice.dao.dao_db_communities import DAO_db_community
from cmSpice.dao.dao_db_similarities import DAO_db_similarity
from cmSpice.dao.dao_db_perspectives import DAO_db_perspectives
from cmSpice.dao.dao_db_flags import DAO_db_flags
from cmSpice.dao.dao_db_distanceMatrixes import DAO_db_distanceMatrixes

from cmSpice.dao.dao_json import DAO_json

from cmSpice.core.communityModel import CommunityModel
from cmSpice.core.communitiesSimilarityModel import CommunitiesSimilarityModel

import logging
from cmSpice.logger.logger import getLogger

logger = getLogger(__name__)

def delete(self):
    # DELETE handler_

    logger.info("DELETE request,\nPath: %s\nHeaders:\n%s\n",
                 str(self.path), str(self.headers))
    # Gets the request
    request = self.path.split("/")
    # logger.info("Request DELETE: %s", str(request[1]))
    first_arg = request[1]
    ok = False

    # case(request)
    if first_arg == "perspective":
        ok = "deletePerspective"


    # return request response
    if ok == "deletePerspective":
        perspectiveId = request[2]
        if __deletePerspective(self, perspectiveId):
            __set_response(self, 204)
            self.wfile.write("DELETE request for {}".format(self.path).encode('utf-8'))
        else:
            __set_response(self, 404)
            self.wfile.write("DELETE request for {}".format(self.path).encode('utf-8'))

    else:
        __set_response(self, 500)
        self.wfile.write("-Error-\nDELETE request for {}".format(self.path).encode('utf-8'))


def __set_response(self, code, dataType='text/html'):
    self.send_response(code)
    self.send_header('Content-type', dataType)
    self.end_headers()


def __deletePerspective(self, perspectiveId):

    daoPerspective = DAO_db_perspectives()
    daoCommunity = DAO_db_community()
    daoSimilarities = DAO_db_similarity()
    daoFlags = DAO_db_flags()
    daoDistMatrixes = DAO_db_distanceMatrixes()

    if daoPerspective.getPerspective(perspectiveId) == {}:
        return False

    daoPerspective.deletePerspective(perspectiveId)
    daoCommunity.deleteFileByPerspectiveId(perspectiveId)
    daoDistMatrixes.deleteDistanceMatrixByPerspectiveId(perspectiveId)
    daoFlags.deleteFlagByPerspectiveId(perspectiveId)

    communities = daoCommunity.getCommunitiesPerspective(perspectiveId, "all")

    for community in communities:
        daoCommunity.deleteCommunity(community["id"])
        daoSimilarities.deleteSimilarity(community["id"], "")
        daoSimilarities.deleteSimilarity("", community["id"])

    return True