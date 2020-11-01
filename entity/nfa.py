# -*- coding: utf-8 -*-
# @Time: 2020/10/28 18:41
# @Author: Rollbear
# @Filename: nfa.py

import networkx as nx
import matplotlib.pyplot as plt


class SubNFA:
    def __init__(self, start, end):
        self.start_ptr = start  # 指向NFA中的开始节点
        self.end_ptr = end  # 指向NFA中的结束节点


class NFA:
    # todo::最小单位应该为NFA（连接、闭包等操作的都是NFA，
    #  最简单的NFA就是一个单词）
    def __init__(self, re, postfix=False):
        # init the vars
        self.raw_re = re
        self.__edge_list = []
        self.__node_map = {}

        # build NFA
        if postfix:
            self.build_nfa_from_postfix()
        else:
            self.build_nfa()

    def build_nfa(self):
        # priority: () > *,+ > | > link
        for char in self.raw_re:
            pass

    def build_nfa_from_postfix(self):
        stack = []
        operand_buffer = []

        char_ptr = 0
        while char_ptr < len(self.raw_re):
            if self.raw_re[char_ptr] == "(":
                stack.append(operand_buffer)
                operand_buffer = []
            elif self.raw_re[char_ptr] == ")":
                # 用当前buffer里的操作数计算，然后退栈，将计算结果放入原栈顶的buffer
                char_ptr += 1
                operator = self.raw_re[char_ptr]
                result = None
                if operator == "&":
                    # 连接运算
                    result = self.make_link(*operand_buffer)
                elif operator == "|":
                    # 或运算
                    result = self.make_or(*operand_buffer)
                elif operator == "*":
                    # 闭包运算
                    result = self.make_closure(*operand_buffer)
                operand_buffer = stack.pop()
                operand_buffer.append(result)
            elif self.raw_re[char_ptr] == ",":
                # "," is the splitter of operands.
                pass
            else:
                # 生成匹配一个字符的NFA
                operand_buffer.append(self.char_match(self.raw_re[char_ptr]))
            char_ptr += 1

    def build_node(self):
        """
        build a node in nfa
        :return: node id
        """
        node_id = len(self.__node_map)
        self.__node_map.update({node_id: []})
        return node_id

    def build_edge(self, parent, desc, edge_attr):
        """
        build a edge in nfa
        :param edge_attr: 
        :param parent: parent_node
        :param desc: descendent_node
        :return: None
        """
        self.__node_map[parent].append(desc)
        self.__edge_list.append((parent, desc, edge_attr))

    def char_match(self, char):
        """
        ground NFA: match a char
        :param char: the char this NFA matching
        :return: current NFA
        """
        pre_node = self.build_node()
        post_node = self.build_node()
        self.build_edge(pre_node, post_node, char)
        return SubNFA(pre_node, post_node)

    def make_link(self, pre_nfa: SubNFA, post_nfa: SubNFA):
        """
        linking operation
        :param pre_nfa: pre-operand
        :param post_nfa: post-operand
        :return: current NFA
        """
        mid = self.build_node()
        self.build_edge(pre_nfa.end_ptr, mid, None)
        self.build_edge(mid, post_nfa.start_ptr, None)
        return SubNFA(pre_nfa.start_ptr, post_nfa.end_ptr)

    def make_closure(self, operand_nfa: SubNFA):
        """
        closure operation
        :param operand_nfa: single operand
        :return: current NFA
        """
        pre = self.build_node()
        post = self.build_node()
        self.build_edge(pre, operand_nfa.start_ptr, None)
        self.build_edge(operand_nfa.end_ptr, post, None)
        self.build_edge(post, pre, None)
        return SubNFA(pre, post)

    def make_or(self, nfa_a: SubNFA, nfa_b: SubNFA):
        """
        or operation
        :param nfa_a: pre-operand
        :param nfa_b: post-operand
        :return: current NFA
        """
        split = self.build_node()
        merge = self.build_node()
        self.build_edge(split, nfa_a.start_ptr, None)
        self.build_edge(nfa_a.end_ptr, merge, None)
        self.build_edge(split, nfa_b.start_ptr, None)
        self.build_edge(nfa_b.end_ptr, merge, None)
        return SubNFA(split, merge)

    def draw(self):
        """draw the figure of NFA"""
        graph = nx.DiGraph()  # init a networkx directed-graph
        graph.add_edges_from(self.__edge_list)

        pos = nx.spring_layout(graph)
        nx.draw_networkx_nodes(graph, pos)
        nx.draw_networkx_edges(graph, pos)
        nx.draw_networkx_labels(graph, pos)  # draw nodes with labels
        plt.show()
