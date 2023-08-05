import logging
from pymongo import MongoClient
from pymongo.errors import ConfigurationError
from datetime import datetime
from socket import gethostname
from time import tzname
from platform import platform
from getpass import getuser
from os import getpid, getcwd, getuid


class MongoHandler(logging.Handler):
    """
    Handler for logging to MongoDB
    """

    def __init__(self, level=logging.NOTSET, collection='log', mongodb_uri='mongodb://127.0.0.1:27017/test'):
        logging.Handler.__init__(self, level)
        client = MongoClient(mongodb_uri)
        try:
            db = client.get_default_database()
        except ConfigurationError as cfg_err:
            if cfg_err.args[0] == 'No default database name defined or provided.':
                db = client.test
            else:
                raise cfg_err
        self.collection = db[collection]

    def emit(self, objLogMsg):
        self.collection.save(
            {
                'message': objLogMsg.msg,
                'loggerInfo': {
                    'loggerName': objLogMsg.name,
                    'logLevel': objLogMsg.levelname,
                    'loggedAt': datetime.utcnow(),
                },
                'host': {
                    'hostName': gethostname(),
                    'localTimeZone': tzname,
                    'platform': platform(),
                },
                'location': {
                    'module': objLogMsg.module,
                    'path': objLogMsg.pathname,
                    'file': objLogMsg.filename,
                    'funcName': objLogMsg.funcName,
                    'lineNo': objLogMsg.lineno,
                },
                'processInfo': {
                    'username': getuser(),
                    #'uid': getuid(),
                    'processId': getpid(),
                    'workingDirectory': getcwd()
                },
            }
        )
