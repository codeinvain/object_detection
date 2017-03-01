import logging
import os
import json
import sys
from object_detector import ObjectDetector
from jsonmerge import merge


config = {}
logger = None

def bootstrap(options):

    if not os.path.exists('log'):
        os.makedirs('log')

    initConfig(options)
    init_logger()
    logger.debug('Starting app %s' %config['version'])

def initConfig(options):
    with open('config/application.json') as json_data_file:
        cfg = json.load(json_data_file)
        global config
        config = merge(merge(cfg['default'],cfg[env()]),options)


def env():
    return os.getenv('PY_ENV','development')


def init_logger():
    logging.basicConfig(filename='log/{env}.log'.format(env=env()),level=logging.DEBUG,format='%(asctime)s [%(levelname)s] %(message)s')
    logging.captureWarnings(True)
    root = logging.getLogger()

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(levelname)s] %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)

    global logger
    logger = logging

def startApp():
    o = ObjectDetector()
