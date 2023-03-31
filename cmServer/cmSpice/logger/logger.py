
import os
import logging
import logging.config
from cmSpice.logger.mongoLogger import MongoHandler


def getLogger(fileName):
    logging.basicConfig(level=logging.INFO)
    logging.config.fileConfig('cmSpice/logger/logging.ini',
                            disable_existing_loggers=False)
    logger = logging.getLogger(fileName)
    logger.addHandler(MongoHandler(collection=os.environ['DB_LOG_COLLECTION'],
                                host=os.environ['DB_HOST'],
                                db_name=os.environ['DB_NAME'],
                                username=os.environ['DB_USER'],
                                password=os.environ['DB_PASSWORD'],
                                port=os.environ['DB_PORT']))
    return logger
