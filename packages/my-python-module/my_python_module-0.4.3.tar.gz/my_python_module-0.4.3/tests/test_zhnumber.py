#!/usr/bin/env python
# -*- coding: utf-8 -*-

from my_python_module.nlp.text_helper import guess_chapter_id
from simple_nltk.util import bigrams, trigrams, skipgrams
from my_python_module.zhnumber import int_zhnumber, zhnumber


def test_zhnumber():
    assert zhnumber(0) == '零'
    assert zhnumber(1) == '一'
    assert zhnumber(11) == '一十一'
    assert zhnumber(15156) == '一万五千一百五十六'
    assert zhnumber(101) == '一百零一'
    assert zhnumber(1001) == '一千零一'
    assert zhnumber(10000001) == '一千万零一'


def test_int_zhnumber():
    assert int_zhnumber('一') == 1
    assert int_zhnumber('十一') == 11
    assert int_zhnumber('二十二') == 22
    assert int_zhnumber('一百零三') == 103
    assert int_zhnumber('三百四十五') == 345

    assert int_zhnumber('1万6千') == 16000


def test_zhnumber_all():
    assert int_zhnumber(zhnumber(15156)) == 15156


def test_guess_chapter_id():
    assert guess_chapter_id('第3103章') == 3103

    assert guess_chapter_id('第三十章') == 30
    assert guess_chapter_id('第三十一章') == 31

    assert guess_chapter_id('第一百零二章') == 102

    assert guess_chapter_id('第二百三十八章') == 238


def test_bigrams():
    assert list(bigrams([1, 2, 3, 4, 5])) == [(1, 2), (2, 3), (3, 4), (4, 5)]


def test_trigrams():
    assert list(trigrams([1, 2, 3, 4, 5])) == [(1, 2, 3), (2, 3, 4), (3, 4, 5)]


def test_skipgrams():
    sent = "Insurgents killed in ongoing fighting".split()
    assert list(skipgrams(sent, 2, 2)) == [('Insurgents', 'killed'),
                                           ('Insurgents', 'in'),
                                           ('Insurgents', 'ongoing'),
                                           ('killed', 'in'),
                                           ('killed', 'ongoing'),
                                           ('killed', 'fighting'),
                                           ('in', 'ongoing'),
                                           ('in', 'fighting'),
                                           ('ongoing', 'fighting')]
    assert list(skipgrams(sent, 3, 2)) == [('Insurgents', 'killed', 'in'),
                                           ('Insurgents', 'killed', 'ongoing'),
                                           ('Insurgents', 'killed', 'fighting'),
                                           ('Insurgents', 'in', 'ongoing'),
                                           ('Insurgents', 'in', 'fighting'), (
                                               'Insurgents', 'ongoing',
                                               'fighting'),
                                           ('killed', 'in', 'ongoing'),
                                           ('killed', 'in', 'fighting'),
                                           ('killed', 'ongoing', 'fighting'),
                                           ('in', 'ongoing', 'fighting')]
