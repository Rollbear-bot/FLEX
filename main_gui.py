# -*- coding: utf-8 -*-
# @Time: 2020/11/1 16:51
# @Author: Rollbear
# @Filename: main_gui.py

import tkinter
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

from entity.nfa import NFA
from entity.dfa import DFA
from entity.source_generator import SourceGenerator


# 根面板
root = Tk()  # 创建窗口对象的背景色
root.geometry("1200x400")
root.title("myFLEX")

# 初始化文本
CPP_PATH = ""
file_path_str_obj = StringVar()
file_path_str_obj.set("请输入表达式：")

# 初始化组件
label_file_path = Label(root, textvariable=file_path_str_obj)
entry_field = Entry(root, show=None)

# 创建滚动条
# scroll = tkinter.Scrollbar()

# 文本框
text_node_map = tkinter.Text(root)  # 展示解析节点表
text_source = tkinter.Text(root)  # 展示生成的源代码

# 用于图片描述的label
# nfa_figure_describe = Label(root, text="NFA图：")
# dfa_figure_describe = Label(root, text="DFA图：")
# 用于存放图片的label
# nfa_figure = Label(root)
# dfa_figure = Label(root)


def run():
    # 重新初始化
    # nfa_figure.image = None
    # dfa_figure.image = None

    if entry_field.get() == "":
        messagebox.askokcancel("确认",
                               f"你还没有输入表达式")
    else:
        # 生成NFA与DFA
        nfa = NFA(entry_field.get(), postfix=True)
        dfa = DFA(nfa)
        # 绘图
        nfa.draw(dump_path="./res/nfa.png")
        dfa.draw(dump_path="./res/dfa.png")
        # 清空文本框并刷新
        text_node_map.delete(0.0, END)
        text_node_map.insert("insert", "NFA转DFA时建立的节点表：\n" + dfa.print_node_map())

        text_source.delete(0.0, END)
        text_source.insert("insert", SourceGenerator(dfa).cpp_source)

        # 通过系统的图片浏览器来展示NFA/DFA图像
        nfa_image = Image.open("./res/nfa.png")
        nfa_image.show(title="figure of NFA")

        dfa_image = Image.open("./res/dfa.png")
        dfa_image.show(title="figure of DFA")


if __name__ == '__main__':
    label_file_path.grid(row=0, column=0)
    entry_field.grid(row=1, column=0)

    # 开始解析的按钮
    button_run = Button(root, command=run, text="开始解析")
    button_run.grid(row=2, column=0)

    # 将滚动条填充
    # scroll.pack(side=tkinter.RIGHT, fill=tkinter.Y)  # side是滚动条放置的位置，上下左右。fill是将滚动条沿着y轴填充

    text_node_map.grid(row=3, column=0)
    text_source.grid(row=3, column=1)

    # 将滚动条与文本框关联
    # scroll.config(command=text.yview)  # 将文本框关联到滚动条上，滚动条滑动，文本框跟随滑动
    # text.config(yscrollcommand=scroll.set)  # 将滚动条关联到文本框

    # nfa_figure_describe.grid(row=0, column=1)
    # nfa_figure.grid(row=1, column=1)
    # dfa_figure_describe.grid(row=0, column=2)
    # dfa_figure.grid(row=1, column=2)

    root.mainloop()
