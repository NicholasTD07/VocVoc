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
    """
    Return (text, locatedLines).
    text -- the text read from file.
    locatedLines -- lines with the word in put in a list.
    """
    locatedLines = list()
    with open(filePath) as textFile :
        lines = textFile.readlines()
        # Put the file path into the first item in lines.
        lines.insert(0, filePath) 
    for line in lines :
        if word in line :
            locatedLines.append(lines.index(line))
    return (lines, locatedLines)


