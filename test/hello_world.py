# -*- coding: utf-8 -*-
# @Time: 2020/10/21 8:23
# @Author: Rollbear
# @Filename: hello_world.py

from entity.nfa import NFA
from entity.dfa import DFA

# re = "(((a)*,b)|,c)|"
# nfa = NFA(re, postfix=True)
# nfa.draw()
#
# dfa = DFA(nfa)
# for key, value in dfa.node_map.items():
#     print(str(key) + "\t" + str(value))
#
# dfa.draw()

tester = NFA("(A,B)|", postfix=True)
print(tester.RE_to_midfix("AC|AB*"))
