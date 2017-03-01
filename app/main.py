import logging
import os
import json
import sys
from object_detector import ObjectDetector
from jsonmerge import merge


class Main:
    def __init__(self,options):
        self.initConfig(options)
        self.init_logger()
        self.logger.debug('Starting app %s' %self.config['version'])

    def initConfig(self,options):
        with open('config/application.json') as json_data_file:
            self.cfg = json.load(json_data_file)
            self.config = merge(merge(self.cfg['default'],self.cfg[self.env()]),options)

    def env(self):
        return os.getenv('PY_ENV','development')

    def get_logger(self):
        return logging

    def init_logger(self):
        logging.basicConfig(filename='log/{env}.log'.format(env=self.env()),level=logging.DEBUG,format='%(asctime)s [%(levelname)s] %(message)s')
        logging.captureWarnings(True)
        root = logging.getLogger()

        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('[%(levelname)s] %(message)s')
        ch.setFormatter(formatter)
        root.addHandler(ch)

        self.logger = logging

    def startApp(self):
        o = ObjectDetector(self,self.config)
