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

def post(self):
    # _post handler_

    # Gets the size of data
    content_length = int(self.headers['Content-Length'])
    # Gets the data itself
    post_data = self.rfile.read(content_length)
    post_data = post_data.decode('utf-8')
    logger.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                 str(self.path), str(self.headers), post_data)
    # Gets the request
    request = self.path.split("/")
    # logger.info("Request POST: %s", str(request[1]))
    first_arg = request[1]
    ok = False

    # case(request)
    if first_arg == "perspective":
        # Do nothing #
        ok = True

    elif first_arg == "update_CM":
        ok = "updateCM"

    elif first_arg == "updateUsers":
        ok = "updateUsers"

    elif first_arg == "load":
        data = loads(post_data)
        DAO_db().loadDB(data)
        ok = True

    # return request response
    if ok:
        __set_response(self, 204)
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

        # after returning response, update CM or Users
        if ok == "updateCM":
            __updateCM(self)
        elif ok == "updateUsers":
            __updateUsers(self, post_data)
    else:
        __set_response(self, 500)
        self.wfile.write("-Error-\nPOST request for {}".format(self.path).encode('utf-8'))


def __set_response(self, code, dataType='text/html'):
    self.send_response(code)
    self.send_header('Content-type', dataType)
    self.end_headers()


def __updateUsers(self, post_data):
    users = loads(post_data)
    daoUsers = DAO_db_users()
    ok = daoUsers.insertUser_API(users)

    # Activate flags associated to user/perspective pair (perspective makes use of one of the user's
    # attributes (pname))
    daoPerspectives = DAO_db_perspectives()
    daoFlags = DAO_db_flags()

    perspectives = daoPerspectives.getPerspectives()

    for user in users:
        for perspective in perspectives:
            for similarityFunction in perspective['similarity_functions'] + perspective[
                'interaction_similarity_functions']:
                """
                print("checking similarity function")
                print("att_name: " + str(similarityFunction['sim_function']['on_attribute']['att_name']))
                print("pname: " + str(user['pname']))
                """
                attributeLabel = user["category"] + "." + user["pname"]
                if similarityFunction['sim_function']['on_attribute']['att_name'] == attributeLabel:
                    flag = {'perspectiveId': perspective['id'], 'userid': user['userid'], 'needToProcess': True, 'error': "N/D"}
                    # flag = {'perspectiveId': perspective['id'], 'userid': 'flagAllUsers', 'flag': True}
                    daoFlags.updateFlag(flag)


def __updateCM(self):

    # Check if there is an update flag
    daoPerspectives = DAO_db_perspectives()
    daoFlags = DAO_db_flags()

    flags = daoFlags.getFlags()
    deleteFlags = []

    # Sort all flags by perspectiveId
    perspectiveFlagsDict = {}
    for flag in flags:
        if flag['needToProcess'] == True:
            if flag["perspectiveId"] not in perspectiveFlagsDict:
                perspectiveFlagsDict[flag["perspectiveId"]] = []
            perspectiveFlagsDict[flag["perspectiveId"]].append(flag['userid'])
            # needToProcess to false
            flag["needToProcess"] = False
            daoFlags.replaceFlag(flag)
            deleteFlags.append(flag)

    try:
        # Update each perspective communities
        for perspectiveId in perspectiveFlagsDict:
            perspective = daoPerspectives.getPerspective(perspectiveId)

            communityModel = CommunityModel(perspective, perspectiveFlagsDict[perspectiveId], 0.5)
            communityModel.start()

            # Compute the similarity between the new communities generated with self.perspective
            communitiesSimilarityModel = CommunitiesSimilarityModel(perspectiveId, communityModel)

        # Delete updated flags (cannot delete the whole collection because new flags may have been added while CM was
        # updating)
        for flag in deleteFlags:
            # Remove flag
            daoFlags.deleteFlag(flag)

    except Exception as e:
        flag["error"] = str(e)
        daoFlags.replaceFlag(flag)
        logger.error(traceback.format_exc())