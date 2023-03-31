# python modules
from bson.json_util import dumps, loads
from bson.objectid import ObjectId

# logger
import logging
from cmSpice.logger.logger import getLogger
logger = getLogger(__name__)

# local modules
from cmSpice.dao.dao_db import DAO_db


def get(self):
    # _get handler_

    logger.info("GET request,\nPath: %s\nHeaders:\n%s\n",
                 str(self.path), str(self.headers))
    # Gets the request
    request = self.path.split("/")
    # logger.info("Request GET: %s", str(request[1]))
    first_arg = request[1]

    if first_arg == "dump":
        __getDump(self)
    else:
        __set_response(self, 500)
        self.wfile.write("-Error-\nGET request for {}".format(self.path).encode('utf-8'))


def __set_response(self, code, dataType='text/html'):
    self.send_response(code)
    self.send_header('Content-type', dataType)
    self.end_headers()


def __getDump(self):
    dump = DAO_db().dumpDB()
    __set_response(self, 200, 'application/json')
    self.wfile.write(dumps(dump).encode(encoding='utf_8'))
