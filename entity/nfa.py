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
    def __init__(self, re, postfix=False,
                 color_start_node="#a195fb",
                 color_end_node="#ff8696",
                 color_other="#e5f7ff"):
        # init the vars
        self.raw_re = re
        self.root_NFA = None
        self.color_map = None
        self.__edge_list = []
        self.__node_map = {}

        # build NFA
        if postfix:
            self.build_nfa_from_postfix()
        else:
            self.build_nfa()
        self.assign_node_color()

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

        self.root_NFA = operand_buffer[0]

    def assign_node_color(self,
                          color_start_node="#a195fb",
                          color_end_node="#ff8696",
                          color_other="#e5f7ff"):
        """
        assign the color of nodes (while drawing figure)
        :return: None
        """
        self.color_map = [color_other for i in range(len(self.__node_map))]
        self.color_map[self.root_NFA.start_ptr] = color_start_node
        self.color_map[self.root_NFA.end_ptr] = color_end_node

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
        self.build_edge(pre_nfa.end_ptr, post_nfa.start_ptr, None)
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
        for edge in self.__edge_list:
            graph.add_edge(edge[0], edge[1], label=edge[2])

        pos = nx.spring_layout(graph)
        capacity = nx.get_edge_attributes(graph, "label")

        nx.draw_networkx_nodes(graph, pos, node_color=self.color_map)  # 画出点
        nx.draw_networkx_edges(graph, pos)  # 画出边
        nx.draw_networkx_labels(graph, pos)  # 画出点上的label
        nx.draw_networkx_edge_labels(graph, pos, capacity)  # 画出边上的label（例如权）

        plt.show()
