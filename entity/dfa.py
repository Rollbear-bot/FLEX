# -*- coding: utf-8 -*-
# @Time: 2020/10/28 18:42
# @Author: Rollbear
# @Filename: dfa.py

import networkx as nx
import matplotlib.pyplot as plt

from entity.nfa import NFA


class DFA:
    def __init__(self, nfa_obj: NFA,
                 color_start_node="#a195fb",
                 color_end_node="#ff8696",
                 color_other="#e5f7ff"):
        # init the vars
        self.nfa_obj = nfa_obj
        self.nx_graph = None
        self.color_map = []  # 存储节点的颜色（绘图时），在assign nodes color时初始化
        self.__node_map = None
        # 指向开始节点和结束节点的指针，稍后在build中初始化
        self.start_ptr = None
        self.end_ptr = None

        # build DFA from NFA
        self.nx_graph = self.build_dfa_from_nfa(self.nfa_obj)
        # assign nodes color
        self.color_map = self.assign_nodes_color(color_start_node,
                                                 color_end_node,
                                                 color_other)

    def build_dfa_from_nfa(self, nfa: NFA):
        dfa_node_map = {}
        # 从nfa的开始节点开始，求空的闭包
        start_empty_closure = nfa.get_closure([nfa.root_NFA.start_ptr], None)
        dfa_node_map.update({start_empty_closure: []})
        self.start_ptr = start_empty_closure

        # 建表
        updated = True
        while updated:
            updated = False
            # 找出还没求闭包的node list
            for key in [key for key, value in dfa_node_map.items() if value == []]:
                avail_letters = nfa.get_closure_avail_letter(key)
                for letter in avail_letters:
                    dfa_node_map[key].append((letter, nfa.get_closure(key, letter)))
                for closure_item in dfa_node_map[key]:
                    if closure_item[1] not in dfa_node_map.keys():
                        # 直到没有新节点出现时，停止迭代
                        updated = True
                        dfa_node_map.update({closure_item[1]: []})
        self.__node_map = dfa_node_map

        # 结束节点指针
        ends = [key for key, value in dfa_node_map.items() if value == []]
        if len(ends) == 0:
            self.end_ptr = self.start_ptr
        else:
            self.end_ptr = ends[0]

        # 从表建立图结构
        graph = nx.DiGraph()
        for start, desc_lt in dfa_node_map.items():
            for item in desc_lt:
                graph.add_edge(start, item[1], label=item[0])

        return graph

    def assign_nodes_color(self,
                           color_start_node,
                           color_end_node,
                           color_other):
        color_map = []
        for node in self.nx_graph.nodes:
            if node == self.start_ptr:
                color_map.append(color_start_node)
            elif node == self.end_ptr:
                color_map.append(color_end_node)
            else:
                color_map.append(color_other)
        return color_map

    def draw(self, dump_path=None):
        # todo::networkx画不了自环
        pos = nx.spring_layout(self.nx_graph)
        capacity = nx.get_edge_attributes(self.nx_graph, "label")

        nx.draw_networkx_nodes(self.nx_graph, pos, node_color=self.color_map)  # 画出点
        nx.draw_networkx_edges(self.nx_graph, pos)  # 画出边
        nx.draw_networkx_labels(self.nx_graph, pos)  # 画出点上的label
        nx.draw_networkx_edge_labels(self.nx_graph, pos, capacity)  # 画出边上的label（例如权）

        if dump_path is None:
            plt.show()
        else:
            plt.savefig(dump_path)

    @property
    def node_map(self):
        return self.__node_map

    def print_node_map(self):
        output = ""
        for key, value in self.node_map.items():
            output += str(key)
            output += "\t" * 3
            output += str(value)
            output += "\n"
        return output
