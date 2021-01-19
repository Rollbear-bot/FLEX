# -*- coding: utf-8 -*-
# @Time: 2021/1/18 22:15
# @Author: Rollbear
# @Filename: source_generator.py

from entity.dfa import DFA


class SourceGenerator:
    def __init__(self, dfa_obj: DFA):
        self.__dfa = dfa_obj
        self.__nx_graph = dfa_obj.nx_graph
        self.__map_node_id = {node: node_id for node_id, node in enumerate(self.__dfa.node_map)}

    @property
    def cpp_source(self):
        out = self.__head() + self.__func() + self.__main_front() \
               + self.__switch_part() + self.__main_back()
        return out

    def dump_cpp_source(self, dump_path):
        with open(dump_path, "w") as wf:
            wf.write(self.cpp_source)

    @staticmethod
    def __head():
        out = """#include <iostream>
using namespace std;

#define MAX_TARGET_LEN 50\n"""
        return out

    @staticmethod
    def __func():
        out = """void print_err(int cur_char) {
    cout << "error! (at index " << cur_char << ")" << endl;
}

void match(char tar) {
    cout << "match " << tar << "!" << endl;
}\n"""
        return out

    def __main_front(self):
        # 计算开始节点的id，以赋值给初始的状态标记flag
        start_node = self.__map_node_id[self.__dfa.start_ptr]
        out = """int main() {
    cout << "input a string:" << endl;
    char target[MAX_TARGET_LEN];
    cin >> target;

    int cur_char = 0;  //当前字符标记
    int flag = """ + str(start_node) + """;  //状态标记
    while (flag >= 0) {
        switch (flag) {\n"""
        return out

    @staticmethod
    def __main_back():
        out = """
        }
    }
    return 0;
}"""
        return out

    def __switch_part(self):
        out = ""
        for cur_node, dest_map in self.__dfa.node_map.items():
            # tail, dest, label
            edges = [(self.__map_node_id[cur_node],
                      self.__map_node_id[dest[1]],
                      dest[0])
                     for dest in dest_map]
            out += self.__in_switch_make_case(self.__map_node_id[cur_node], edges)
        return out

    @staticmethod
    def __in_switch_make_case(node_id, edges):
        out = ""
        out += "case " + str(node_id) + ": {\n"

        if len(edges) == 0:
            # 无出边的节点转移到结束状态
            out += "flag = -1;\nbreak;}\n"
        else:
            out += """switch (target[cur_char]) {\n"""
            for edge in edges:
                out += "case '" + str(edge[2]) + "': {\n"
                out += "match(target[cur_char]);\n"
                out += "cur_char++;\n"
                out += "flag = " + str(edge[1]) + ";\n"  # 状态标记设置为下一个状态的id
                out += "break;\n}\n"

            out += """default: {
                        print_err(cur_char);
                        flag = -1;
                        break;
                    }\n}\nbreak;\n}\n"""
        return out
