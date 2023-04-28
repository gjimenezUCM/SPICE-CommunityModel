# python modules
import os
from bson.json_util import dumps, loads
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ForkingMixIn
from bson.objectid import ObjectId
import json
import time

import logging
from cmSpice.logger.logger import getLogger

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
from cmSpice.utils.dataLoader import DataLoader

from cmSpice.apiServer import getHandler
from cmSpice.apiServer import postHandler
from cmSpice.apiServer import deleteHandler

server_loader_port = int(os.environ['CM_DOCKER_PORT'])
server_loader_ip = "0.0.0.0"


db_collection = os.environ['DB_LOG_COLLECTION']
db_host = os.environ['DB_HOST']
db_user = os.environ['DB_USER']
db_password = os.environ['DB_PASSWORD']
db_name = os.environ['DB_NAME']
db_port = os.environ['DB_PORT']


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        getHandler.get(self)

    def do_POST(self):
        postHandler.post(self)

    def do_DELETE(self):
        deleteHandler.delete(self)


class ForkingHTTPServer(ForkingMixIn, HTTPServer):
    def finish_request(self, request, client_address):
        request.settimeout(30)
        HTTPServer.finish_request(self, request, client_address)


def run(server_class=HTTPServer, handler_class=Handler):


    # logger
    logger = getLogger(__name__)
    logger.info('Starting server-loader...\n')

    # f = open("cmSpice/logger/file.log", "r")
    # print(f.read())

    server_address = (server_loader_ip, server_loader_port)
    httpd = ForkingHTTPServer(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()

    logger.info('Stopping server-loader...\n')
