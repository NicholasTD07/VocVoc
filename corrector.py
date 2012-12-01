#!/usr/bin/env python3
"""
This is the spell checker of the VocVoc.

The original code is written by Peter Norvig.
He has an article about the code itself and the principles behind and details of it explained at http://norvig.com/spell-correct.html.

With class Counter from the collections module, it is much simpler to combine two models together.
"""

# collections
from collections import Counter

# re
from re import findall

# logging
from logging import getLogger

# time
from time import time

# os
from os.path import join as pJoin

# config
from config import __dir__, Config


class WordModel(Counter) :

    """This is the adapted Counter class which returns 1 as the value of keys which are not present."""

    def __missing__(self, key) :
        return 1


class SpellChecker:

    """ This is the class for the spelling corrector.\nPass the file object to start it."""

    alphabet = 'abcdefghijklmnopqrstuvwxyz'

    def __init__(self, wordFile=None) :
        self.logger = getLogger('VocVoc.SpellChecker')
        self.info = self.logger.info
        self.warn = self.logger.warn
        self.info('Initializing SpellChecker.')
        self.wordModel = WordModel()
        self.loadConfig()
        self.wordModel.update(self.trainModel(wordFile))
        self.info('SpellChecker Initialized.')

    def loadConfig(self) :
        info = self.info
        info('Start to get config from config.ini')
        config = Config()
        pickleDir = config.pickleDir
        pickleDirName = config.pickleDirName
        corpusDir = config.corpusDir
        corpusDirName = config.corpusDirName
        if pickleDir :
            info('PickleDir Found in config.ini.')
            self.pickleDir = pickleDir
        else :
            info('PickleDir NOT Found in config.ini.')
            self.pickleDir = pJoin(__dir__, pickleDirName)
        if corpusDir :
            info('CorpusDir Found in config.ini.')
            self.corpusDir = corpusDir
        else :
            info('CorpusDir NOT Found in config.ini.')
            self.corpusDir = pJoin(__dir__, corpusDirName)
        info("""Config listed below:
                pickleDir : {},
                corpusDir : {}
                """.format(self.pickleDir, self.corpusDir)
                )


    def trainModel(self, wordFile=None) :
        self.info('Training a WordModel.')
        begin = time()
        try : # If wordFile is not None.
            wordList = findall( r'[a-z]+', wordFile.read().lower() )
            wordModel = WordModel()
            for word in wordList :
                wordModel[word] += 1
        except Exception as error:
            self.warn( 'There is no file input. Aborting.')
            return
        self.info( 'WordModel trained in {}s.'.format(time()-begin) )
        return wordModel

    def saveModel(self, fileName) :
        pass

    def loadModel(self, fileName) :
        pass

    def editD1(self, word) : # D1 for Distance = 1
        self.info('Generating one-distance spell errors.')
        begin = time()
        splits = [ ( word[:i], word[i:] ) for i in range( len(word)+1 ) ]
        deletes = [ a + b[1:] for (a, b) in splits if b ]
        transposes = [ a + b[1] + b[0] + b[2:] for (a, b) in splits if (len(b)>1) ]
        replaces = [ a + c + b[1:] for (a, b) in splits for c in self.alphabet if b ]
        inserts = [ a + c + b for (a, b) in splits for c in self.alphabet ]

        errors = set(deletes + transposes + replaces + inserts)
        self.info( '{} errors generated in {}s.'.format(len(errors), time()-begin) )
        return errors

    def editD2(self, word) :
        self.info('Generating two-distance spell errors.')
        begin = time()
        errors = set( e2 for e1 in self.editD1(word) for e2 in self.editD1(e1) )
        self.info( '{} errors generated in {}s.'.format(len(errors), time()-begin) )

    def known(self, wordList) :
        self.info('Generating known words from the input wordList with the wordModel.')
        begin = time()
        try :
            knownWords = set( word for word in wordList if word in self.wordModel )
        except Exception as error :
            self.info( 'No wordModel.' )
            return
        self.info( '{} known words from the input in {}s.'.format(len(knownWords), time()-begin) )
        return knownWords

    def correct(self, word) :
        self.info('Checking the word.')
        begin = time()
        candidates = self.known( [word] ) or \
                self.known( self.editD1(word) ) or \
                self.known( self.editD2(word) ) or [word]
        self.info( '{} correct candidates generated in {}s.'.format(len(candidates), time()-begin) )
        return sorted(candidates, key=self.wordModel.get, reverse=True) # return a sorted list with decending order.


if __name__ == '__main__' :
    # logger
    from VocVoc import getLogger as myLogger

    myLogger()

    with open('big.txt') as corpus :
        #sc = SpellChecker(None)
        sc = SpellChecker(corpus)

    print(sc.correct('therr'))
    print(sc.wordModel.most_common(10))
