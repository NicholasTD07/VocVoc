#!/usr/bin/env python3
"""
This is the spell checker of the VocVoc.

The original code is written by Peter Norvig.
He has an article about the code itself and the principles behind and details of it explained at http://norvig.com/spell-correct.html.
"""

# collections
from collections import defaultdict

# re
from re import findall


class SpellCorrector :

    """ This is the class for the spelling corrector.\nPass the file object to start it."""

    alphabet = 'abcdefghijklmnopqrstuvwxyz'

    def __init__(self, wordFile=None) :
        self.wordModel = defaultdict(lambda : 1)
        self.addCorpus(wordFile)

    def addCorpus(self, wordFile=None) :
        if wordFile is not None :
            self.wordList = findall( r'[a-z]+', wordFile.read().lower() )
            self.trainModel()

    def trainModel(self) :
        wordList = self.wordList
        wordModel = self.wordModel
        for word in wordList :
            wordModel[word] += 1
        self.wordList = [] # clear the wordList

    def editD1(self, word) : # D1 for Distance = 1
        splits = [ ( word[:i], word[i:] ) for i in range( len(word)+1 ) ]
        deletes = [ a + b[1:] for (a, b) in splits if b ]
        transposes = [ a + b[1] + b[0] + b[2:] for (a, b) in splits if (len(b)>1) ]
        replaces = [ a + c + b[1:] for (a, b) in splits for c in self.alphabet if b ]
        inserts = [ a + c + b for (a, b) in splits for c in self.alphabet ]

        return set(deletes + transposes + replaces + inserts)

    def knownEditD2(self, word) :
        return set( e2 for e1 in self.editD1(word) for e2 in self.editD1(e1) if e2 in self.wordModel )

    def known(self, wordList) :
        return set( word for word in wordList if word in self.wordModel )

    def correct(self, word) :
        candidates = self.known( [word] ) or self.known( self.editD1(word) ) or self.knownEditD2(word) or [word]
        #return max(candidates, key=self.wordModel.get) # only return the one with highest possibility.
        return sorted(candidates, key=self.wordModel.get, reverse=True) # return a sorted list with decending order.


