# -*- coding: utf-8 -*-
# @Time: 2020/10/28 18:38
# @Author: Rollbear
# @Filename: unittest.py

import unittest
from unittest import TestCase

from entity.nfa import NFA


class TestFLEX(TestCase):
    def test_nfa(self):
        re = "a|ab"
        nfa = NFA(re)


if __name__ == '__main__':
    unittest.main()
