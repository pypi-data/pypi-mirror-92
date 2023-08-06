#!/usr/bin/env python
# -*-coding:utf-8-*-


from simple_nltk import RegexpTokenizer
from simple_nltk.tokenize.api import TokenizerI
from ..list import combine_odd_even


class ChineseSentenceTokenizer(RegexpTokenizer):
    def __init__(self):
        RegexpTokenizer.__init__(self, r"(。|？|！)", gaps=True)

    def tokenize(self, text):
        res = super(ChineseSentenceTokenizer, self).tokenize(text)
        return combine_odd_even(res)

class SimpleTokenizer(TokenizerI):
    def tokenize(self, text):
        return text.split()

class NewlineTokenizer(TokenizerI):
    def tokenize(self, text):
        return text.splitlines()
