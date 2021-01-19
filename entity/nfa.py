# -*- coding: utf-8 -*-
# @Time: 2020/10/28 18:41
# @Author: Rollbear
# @Filename: nfa.py
import os

import networkx as nx
import matplotlib.pyplot as plt
from graphviz import Digraph


class SubNFA:
    def __init__(self, start, end):
        self.start_ptr = start  # 指向NFA中的开始节点
        self.end_ptr = end  # 指向NFA中的结束节点


class NFA:
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
        self.assign_node_color(color_start_node,
                               color_end_node,
                               color_other)

    @staticmethod
    def RE_to_midfix(re_string):
        # todo::将RE转化为中缀表达式，再转化为后缀表达式
        operators = ["|", "*", "+", "(", ")"]
        res = re_string

        char_index = 0
        while char_index < len(re_string):
            if re_string[char_index] not in operators:
                if char_index < len(re_string) - 1 and \
                        re_string[char_index + 1] not in operators:
                    res = res[:char_index + 1] + "&" + res[char_index + 1:]
                    char_index += 1

            char_index += 1
        return res

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
                          color_start_node,
                          color_end_node,
                          color_other):
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

    def draw(self, dump_path=None, use_graphviz=True):
        """draw the figure of NFA"""
        if not use_graphviz:
            plt.clf()
            graph = nx.DiGraph()  # init a networkx directed-graph
            for edge in self.__edge_list:
                graph.add_edge(edge[0], edge[1], label=edge[2])

            pos = nx.spring_layout(graph)
            capacity = nx.get_edge_attributes(graph, "label")

            nx.draw_networkx_nodes(graph, pos, node_color=self.color_map)  # 画出点
            nx.draw_networkx_edges(graph, pos)  # 画出边
            nx.draw_networkx_labels(graph, pos)  # 画出点上的label
            nx.draw_networkx_edge_labels(graph, pos, capacity)  # 画出边上的label（例如权）

            if dump_path is None:
                plt.show()
            else:
                plt.savefig(dump_path)
        elif use_graphviz:
            dump_filename = dump_path[str(dump_path).rfind("/") + 1:]
            dump_dir = dump_path[:str(dump_path).rfind("/") + 1]
            graph = Digraph(name="NFA")
            # 向图结构中添加边
            for edge in self.__edge_list:
                graph.edge(str(edge[0]), str(edge[1]), label=str(edge[2]))
            print(graph.source)
            graph.render(filename="tmp", directory=dump_dir,
                         view=False, cleanup=False)
            # 通过系统调用dor指令来生成NFA的jpg/png格式图片
            # cmd = f"dot -Tjpg {dump_dir}tmp -o {dump_dir + dump_filename}"
            cmd = f"dot -Tpng {dump_dir}tmp -o {dump_dir + dump_filename}"
            print(os.system(cmd))

    # def draw_with_graphviz(self, dump_dir, dump_filename):
    #     graph = Digraph(name="NFA")
    #     # 向图结构中添加边
    #     for edge in self.__edge_list:
    #         graph.edge(str(edge[0]), str(edge[1]), label=str(edge[2]))
    #     print(graph.source)
    #     graph.render(filename="tmp", directory=dump_dir,
    #                  view=False, cleanup=False)
    #     # 通过系统调用dor指令来生成NFA的jpg格式图片
    #     cmd = f"dot -Tjpg {dump_dir}tmp -o {dump_dir + dump_filename}"
    #     print(os.system(cmd))

    def get_closure(self, node_lt, letter):
        """求一个点或者若干点对一个字母（或空）的闭包"""
        node_lt_buffer = list(node_lt)
        # 仅当求空闭包时，结果才包含自身
        if letter is None:
            res = node_lt_buffer.copy()
        else:
            res = []

        updated = True
        while updated:
            updated = False
            for edge in self.__edge_list:
                if edge[0] in node_lt_buffer and edge[1] not in node_lt_buffer and edge[2] is None:
                    node_lt_buffer.append(edge[1])
                    updated = True
                    break
                if edge[0] in node_lt_buffer and edge[2] == letter:
                    res.append(edge[1])

        # 结果应再求一次空的闭包
        if letter is not None:
            extend_res = self.get_closure(res, None)
            return tuple(set(extend_res))
        else:
            return tuple(set(res))

    def get_closure_avail_letter(self, node_lt):
        """获得当前闭包（node id的集合）可达的所有字母"""
        res = []
        node_lt_buffer = list(node_lt)

        updated = True
        while updated:
            updated = False
            for edge in self.__edge_list:
                if edge[0] in node_lt_buffer and edge[1] not in node_lt_buffer and edge[2] is None:
                    node_lt_buffer.append(edge[1])
                    updated = True
                    break
                if edge[0] in node_lt_buffer and edge[2] is not None:
                    res.append(edge[2])
        return tuple(set(res))
