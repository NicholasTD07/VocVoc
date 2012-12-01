#!/usr/bin/env python3
"""
This is the main file of the VocVoc.
"""


# logging
import logging

# logging.handlers
from logging.handlers import TimedRotatingFileHandler

# argparse
from argparse import ArgumentParser

# interface
from interface import *

# SpellChecker
from spellchecker import WordModel 
# This is the KEY to solve the AttributeError when importing.

def getLogger(DEBUG=False) :
    # Create and set the logger.
    logger = logging.getLogger('VocVoc')
    logger.setLevel(logging.DEBUG if DEBUG else logging.INFO)
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
    descriptionMsg = """
            Put the input to a file and the list in the dialog.
            If the input is a word whose sound file can be found, 
            then the file will be played.
            """
    verboseMsg = """
            Turn on the DEBUG level for logging to see what is going on with Phonon.
            """
    argParser = ArgumentParser(description=descriptionMsg)
    argParser.add_argument(
                            '-v',
                            '--verbose',
                            help=verboseMsg,
                            action='store_true'
                            )
    args = argParser.parse_args()
    getLogger(args.verbose)
    logger = logging.getLogger('VocVoc')
    logger.info('Starting VocVoc.')
    App()


if __name__ == '__main__' :
    VocVoc()
