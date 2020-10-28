# -*- coding: utf-8 -*-
# @Time: 2020/10/28 18:41
# @Author: Rollbear
# @Filename: nfa.py

class NFA:
    def __init__(self, re):
        # init the vars
        self.raw_re = re
        self.edge_list = []
        self.node_map = {}
        # build nfa
        self.build_nfa()

    def build_nfa(self):
        for char in self.raw_re:
            pass

    @property
    def start_node(self):
        return None

    @property
    def end_node(self):
        return None

    def build_node(self):
        """
        build a node in nfa
        :return: None
        """
        node_id = len(self.node_map)
        self.node_map.update({node_id: []})
        return node_id

    def build_edge(self, parent, desc):
        """
        build a edge in nfa
        :param parent: parent_node
        :param desc: descendent_node
        :return: None
        """
        self.node_map[parent].append(desc)
        self.edge_list.append((parent, desc))

    def make_link(self, pre_nfa, post_nfa):
        """
        linking operation
        :param pre_nfa: pre-operand
        :param post_nfa: post-operand
        :return: None
        """
        mid = self.build_node()
        self.edge_list.append((pre_nfa, mid))
        self.edge_list.append((mid, post_nfa))

    def make_closure(self, operand_nfa):
        """
        closure operation
        :param operand_nfa: single operand
        :return: None
        """
        pre = self.build_node()
        post = self.build_node()
        self.edge_list.append((pre, operand_nfa))
        self.edge_list.append((operand_nfa, post))

    def make_or(self, pre_nfa, post_nfa):
        """
        or operation
        :param pre_nfa: pre-operand
        :param post_nfa: post-operand
        :return: None
        """
        split = self.build_node()
        merge = self.build_node()
        self.edge_list.append((split, pre_nfa))
        self.edge_list.append((pre_nfa, merge))
        self.edge_list.append((split, post_nfa))
        self.edge_list.append((post_nfa, merge))
