#!/usr/bin/env python3
"""
This is the config part of VocVoc.
"""


# configparser
from configparser import ConfigParser

# os.path
from os.path import dirname, join as pJoin

# logger
from logging import getLogger

__config__ = 'config.ini'
__dir__ = dirname(__file__)
#__path__ = join(__dir__, __config__)
__config__ = pJoin(__dir__, __config__)


class Config :
    """
    This is the class which stores the configs.
    """

    def __init__(self) :
        self.logger = getLogger('VocVoc.Config')
        self.info = self.logger.info
        self.warn = self.logger.warn
        self.info('Initializing Config.')
        self.config = ConfigParser()
        self.config.read(__config__)
        self.getConfig()
        self.info('Config Initialized.')

    def getConfig(self) :
        self.info('Getting configs into Config.')
        config = self.config
        self.corpusDir = config['Path']['corpusDir']
        self.pickleDir = config['Path']['pickleDir']
        self.info('Config got.')

    def setConfig(self, section, option, value) :
        msg = 'Trying to set the option : {} with the given value : {}.'.format(option, value)
        self.info(msg)
        try :
            self.config[section][option] = value
            with open(__config__, 'w') as configFile :
                self.config.write(configFile)
        except TypeError as error :
            self.warn(error)
            self.warn('Option NOT set.')
            return
        self.info('Option set sucessfully.')


if __name__ == '__main__':

    config = Config()
    #config.setConfig('Path', 'corpusDir', '')
