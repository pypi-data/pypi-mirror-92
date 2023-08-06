import os
import logging
from logging.handlers import RotatingFileHandler
import yaml
from pathlib import Path
from shutil import copyfile
from abc import ABC, abstractmethod

class ManagedClass(ABC):

    def __init__(self, execpath):
        self._installfolder = Path(execpath).parent
        self.homevar = "{}/var/{}".format(str(Path.home()), self.getClassName())

        if not os.path.exists(self.homevar):
            os.makedirs(self.homevar)

        self.readConfig()
        self.setupLogger()

    @classmethod
    @abstractmethod
    def getClassName(cls):
        pass

    def setupLogger(self):
        self.logger = logging.getLogger('{}_log'.format(self.getClassName()))
        log_folder = os.path.join(self.homevar, self.config['logpath'])

        if not os.path.exists(log_folder):
            os.mkdir(log_folder)

        log_path = os.path.join(self.homevar, self.config['logpath'], "{}.log".format(self.getClassName()))

        self.logger.setLevel(logging.INFO)
        fh = RotatingFileHandler(log_path, maxBytes=10000, backupCount=10)
        formatter = logging.Formatter('%(asctime)s-%(message)s', '%Y-%m-%d %H:%M:%S')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

    def readConfig(self):
        config_yml_path = os.path.join(self.homevar, 'config.yml')

        # If config file doesn't exist yet, create it from the template
        if not os.path.isfile(config_yml_path):
            config_template_yml_path = os.path.join(self._installfolder, 'config-template.yml')
            copyfile(config_template_yml_path, config_yml_path)

        with open(config_yml_path, 'r') as config_file:
            self.config = yaml.load(config_file, Loader=yaml.FullLoader)

    @classmethod
    def getHomevarPath(cls):
        return "{}/var/{}".format(str(Path.home()), cls.getClassName())

    @classmethod
    def getConfig(cls):
        config_yml_path = os.path.join(cls.getHomevarPath(), 'config.yml')
        with open(config_yml_path) as config_file:
            config = yaml.load(config_file, Loader=yaml.FullLoader)
            return config

    @classmethod
    def setConfig(cls, config):
        config_yml_path = os.path.join(cls.getHomevarPath(), 'config.yml')

        with open(config_yml_path, 'w') as config_file:
            yaml.dump(config, config_file)