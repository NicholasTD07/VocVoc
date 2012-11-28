#!/usr/bin/env python3
"""
This is the config part of VocVoc.
"""


import configparser


__config__ = 'config.ini'


class Config :
    """
    This is the class which stores the configs.
    """

    def __init__(self) :
        self.config = configparser.ConfigParser()
        self.config.read()

    def getConfig(self) :

if __name__ == '__main__':

    config = Config()
