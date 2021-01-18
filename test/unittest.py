# -*- coding: utf-8 -*-
# @Time: 2020/10/28 18:38
# @Author: Rollbear
# @Filename: unittest.py

import unittest

from entity.nfa import NFA


class TestFLEX(unittest.TestCase):
    def test_nfa(self):
        re = "a|ab"
        nfa = NFA(re)

    def test_build_from_postfix(self):
        re = "(a,(a,b)&)|"
        nfa = NFA(re, postfix=True)


if __name__ == '__main__':
    unittest.main()
