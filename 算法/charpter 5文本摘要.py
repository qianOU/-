# -*- coding: utf-8 -*-
"""
Created on Sun Jan  3 15:29:56 2021

@author: 28659
"""

from nltk.corpus import gutenberg

alice = gutenberg.sents(fileids='carroll-alice.txt')
alice[2]

