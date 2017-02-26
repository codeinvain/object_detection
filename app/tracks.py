import logging
import os
import json
import sys


class Main:
    def __init__(self):
        self.initConfig()
        self.init_logger()
        self.logger.debug('Starting app')

    def initConfig(self):
        with open('config/application.json') as json_data_file:
            self.cfg = json.load(json_data_file)

    def env(self):
        return os.getenv('PY_ENV','development')

    def config(self):
        return self.cfg[self.env()]

    def get_logger(self):
        return logging

    def init_logger(self):
        logging.basicConfig(filename='log/{env}.log'.format(env=self.env()),level=logging.DEBUG,format='%(asctime)s [%(levelname)s] %(message)s')
        root = logging.getLogger()

        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('[%(levelname)s] %(message)s')
        ch.setFormatter(formatter)
        root.addHandler(ch)

        self.logger = logging

    def startApp(self):
        self.logger.debug('TODO call cv2')
