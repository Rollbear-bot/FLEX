# -*- coding: utf-8 -*-
# @Time: 2021/1/18 22:15
# @Author: Rollbear
# @Filename: source_generator.py

from entity.dfa import DFA


class SourceGenerator:
    def __init__(self, dfa_obj: DFA):
        self.dfa = dfa_obj
        self.nx_graph = dfa_obj.nx_graph
        self.

    def dump_cpp_source(self, dump_path):
        out = self.__head() + self.__func() + self.__main_front() \
               + self.__switch_part() + self.__main_back()
        with open(dump_path, "w") as wf:
            wf.write(out)

    @staticmethod
    def __base():
        out = ""
        return out

    @staticmethod
    def __head():
        out = """#include <iostream>
using namespace std;

#define MAX_TARGET_LEN 50"""
        return out

    @staticmethod
    def __func():
        out = """void print_err() {
    cout << "error!" << endl;
}

void match(char tar) {
    cout << "match " << tar << "!" << endl;
}"""
        return out

    @staticmethod
    def __main_front():
        out = """int main() {
    cout << "input a string:" << endl;
    char target[MAX_TARGET_LEN];
    cin >> target;

    int cur_char = 0;  //当前字符标记
    int flag = 1;  //状态标记，定义1为开始状态，-1为结束状态
    while (flag > 0) {
        switch (flag) {"""
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
        # todo::switch part
        out = ""

        for cur_node, dest_map in self.dfa.node_map.items():
            for dest in dest_map:
                edge = (cur_node, dest[1], dest[0])  # tail, dest, label

        return out

    @staticmethod
    def __in_switch_make_case():
        out = ""
        return out
