#!/usr/bin/env python3
"""
This file contains things shouldn't go into interface.py.
"""

__all__ = ['flush']

def flush(filePath, text) :
    with open(filePath, 'a') as textFile :
        text = "".join( [text, '\n'] )
        textFile.write(text)


