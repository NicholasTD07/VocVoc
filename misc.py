#!/usr/bin/env python3
"""
This file contains things shouldn't go into interface.py.
"""

__all__ = ['flush', 'locateWord']

def flush(filePath, text) :
    with open(filePath, 'a') as textFile :
        text = "".join( [text, '\n'] )
        textFile.write(text)

def locateWord(filePath, word) :
    locatedLines = list()
    with open(filePath) as textFile :
        lines = textFile.readlines()
    for line in lines :
        if word in line :
            locatedLines.append(lines.index(line))
    return locatedLines


