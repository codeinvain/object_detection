import logging
import os
import json
import sys
from object_detector import ObjectDetector
from jsonmerge import merge
import atexit


config = {}
logger = None

def bootstrap(options):

    if not os.path.exists('log'):
        os.makedirs('log')

    if not os.path.exists('tmp'):
        os.makedirs('tmp')

    create_pid()
    initConfig(options)
    init_logger()
    logger.info('Starting app v{0} on pid: {1}'.format(config['version'], os.getpid()))
    logger.debug('With config:')
    logger.debug(config)

    atexit.register(delete_pid)


def create_pid():
    f = open('tmp/tracks.pid', 'w')
    f.write("{0}".format(os.getpid()))  
    f.close()  
    

def delete_pid():
    os.remove('tmp/tracks.pid')

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
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)

    global logger
    logger = logging

def startApp():
    o = ObjectDetector()
