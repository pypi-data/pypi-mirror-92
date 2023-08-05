import logging
import sys


def make_logger(a_name='Default Logger', type='console', file_path='./example.log', mongodb_uri='mongodb://127.0.0.1:27017', kafka_bootstrap_servers=['localhost:9092'], kafka_topic='logs'):
    objLogger = logging.getLogger(a_name)
    objLogger.setLevel(logging.DEBUG)

    if type != 'console':
        objLogger.handlers = []
        objLogger.propagate = False

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    lh = None

    if type == 'console':
        lh = logging.StreamHandler()
    elif type == 'file':
        lh = logging.FileHandler(file_path) #'/home/kafka/KafkaConsumer.log')
    elif type == 'mongo':
        # log4mongo  # Buggy
        # from log4mongo.handlers import MongoHandler
        # lh = MongoHandler(host=mongodb_uri)

        # mongolog  # Buggy
        # from mongolog.handlers import MongoHandler
        # import pymongo
        # # dbsrv_cfg = pymongo.uri_parser.parse_uri(mongodb_uri)
        # lh = MongoHandler.to(db='mongolog', collection='logs'
        #                      # host=dbsrv_cfg['nodelist'][0][0]+':'+str(dbsrv_cfg['nodelist'][0][1]),
        #                      # username=dbsrv_cfg['username'], password=dbsrv_cfg['password']
        #                      )

        # Custom handler
        # sys.path.insert(0, dir(__file__))
        from util.MongoHandler import MongoHandler
        lh = MongoHandler(mongodb_uri=mongodb_uri)
    elif type == 'kafka':
        # TODO Test a pre-built handler and pass kafka_bootstrap_servers and kafka_topic
        pass
    else:
        raise Exception('Invalid type - must be console or file')

    lh.setLevel(logging.DEBUG)
    lh.setFormatter(formatter)
    objLogger.addHandler(lh)

    return objLogger

