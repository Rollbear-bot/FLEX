# -*- coding: utf-8 -*-
# @Time: 2020/10/28 19:05
# @Author: Rollbear
# @Filename: synt_parser.py

class Word:
    def __init__(self, is_vt):
        self.is_vt = is_vt

class Statement:
    pass

class Rule:
    def __init__(self):
        self.pre = None
        self.or_statements = []


class SyntParser:
    def __init__(self, rule_file_path):
        self.rule_file_path = rule_file_path
        self.rules = []
        self.vts = []
        self.tree_root = None

    def parse(self, sentence):
        pass

    def res_reader(self, rule_file_path):
        with open(rule_file_path, "r") as rf:
            lines = rf.readlines()
            for line in lines:
                pass
