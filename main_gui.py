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

# 创建展示解析结果的文本框
text = tkinter.Text(root)
# 用于图片描述的label
nfa_figure_describe = Label(root, text="NFA图：")
dfa_figure_describe = Label(root, text="DFA图：")
# 用于存放图片的label
nfa_figure = Label(root)
dfa_figure = Label(root)


def run():
    # 重新初始化
    nfa_figure.image = None
    dfa_figure.image = None

    if entry_field.get() == "":
        messagebox.askokcancel("确认",
                               f"你还没有输入表达式")
    else:
        # 生成NFA与DFA
        nfa = NFA(entry_field.get(), postfix=True)
        dfa = DFA(nfa)
        # 绘图
        nfa.draw(dump_path="./res/nfa.jpg")
        dfa.draw(dump_path="./res/dfa.jpg")
        # 清空文本框并刷新
        text.delete(0.0, END)
        text.insert("insert", "NFA转DFA时建立的节点表：\n" + dfa.print_node_map())

        nfa_image = Image.open("./res/nfa.jpg")
        nfa_photo = ImageTk.PhotoImage(nfa_image)
        nfa_figure.configure(image=nfa_photo)
        nfa_figure.image = nfa_photo

        dfa_image = Image.open("./res/dfa.jpg")
        dfa_photo = ImageTk.PhotoImage(dfa_image)
        dfa_figure.configure(image=dfa_photo)
        dfa_figure.image = dfa_photo


if __name__ == '__main__':
    label_file_path.grid(row=0, column=0)
    entry_field.grid(row=1, column=0)

    # 开始解析的按钮
    button_run = Button(root, command=run, text="开始解析")
    button_run.grid(row=2, column=0)

    # 将滚动条填充
    # scroll.pack(side=tkinter.RIGHT, fill=tkinter.Y)  # side是滚动条放置的位置，上下左右。fill是将滚动条沿着y轴填充

    text.grid(row=3, column=0)

    # 将滚动条与文本框关联
    # scroll.config(command=text.yview)  # 将文本框关联到滚动条上，滚动条滑动，文本框跟随滑动
    # text.config(yscrollcommand=scroll.set)  # 将滚动条关联到文本框

    nfa_figure_describe.grid(row=0, column=1)
    nfa_figure.grid(row=1, column=1)
    dfa_figure_describe.grid(row=2, column=1)
    dfa_figure.grid(row=3, column=1)

    root.mainloop()
