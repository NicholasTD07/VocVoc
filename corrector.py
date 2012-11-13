#!/usr/bin/env python3
"""
This is the spell checker of the VocVoc.

The original code is written by Peter Norvig.
He has an article about the code itself and the principles behind and details of it explained at http://norvig.com/spell-correct.html .
"""

# collections
from collections import defaultdict

# re
from re import findall


class SpellCorrector :

    """ This is the class for the spelling corrector."""

    alphabet = 'abcdefghijklmnopqrstuvwxyz'

    def __init__(self, wordFile) :
        self.wordList = wordFile.read()
        self.wordModel = defaultdict(lambda : 1)

    def trainModel(self) :
        wordModel = self.wordModel
        for word in wordList :
            wordModel[word] += 1

    def editD1(self, word) : # D1 for Distance = 1
        splits = [ ( word[:i] + word[i:] ) for i in range( len(word+1) ) ]
        deletes = [ a + b[1:] for a, b in splits if b ]
        transposes = [ a + b[1] + b[0] + b[2:] for a, b in splits if (len(b)>1) ]
        replaces = [ a + c + b[1:] for a, b in splits for c in alphabet if b ]
        inserts = [ a + c + b for a, b in splits for c in alphabet ]

        return set(deletes, transposes, replaces, inserts)

    def knownEditD2(self, word) :
        return set( e2 for e1 in self.editD1(word) for e2 in self.editD1(e1) if e2 in self.wordModel )

    def known(self, wordList) :
        return set( word in wordList if word in self.wordModel )

    def correct(self, word) :
        candidates = known( [word] ) or known( self.editD1(word) ) or knownEditD2(word) or [word]
        return max(candidates, key=self.wordModel.get



