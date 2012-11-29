#!/usr/bin/env python3
"""
This is the main file of the VocVoc.
"""


# logging
import logging

# logging.handlers
from logging.handlers import TimedRotatingFileHandler

# interface
from interface import *


def getLogger() :
    # Create and set the logger.
    logger = logging.getLogger('VocVoc')
    logger.setLevel(logging.INFO)
    # Create a TimedRotatingFileHandler.
    fileHandler = TimedRotatingFileHandler('VocVoc.log', when='w0')
    # Only log things which could be wrong.
    fileHandler.setLevel(logging.WARNING)
    # Create a StreamHandler to output to the console.
    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(logging.DEBUG)
    # Set the formatter and give it to handlers.
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fileHandler.setFormatter(formatter)
    consoleHandler.setFormatter(formatter)
    # Add handlers to the logger.
    for handler in [fileHandler, consoleHandler] :
        logger.addHandler(handler)
    logger.info('Created Logger.')

def VocVoc() :
    getLogger()
    logger = logging.getLogger('VocVoc')
    logger.info('Starting VocVoc.')
    App()


if __name__ == '__main__' :
    VocVoc()
