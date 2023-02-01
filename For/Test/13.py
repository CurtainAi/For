from tkinter import *
from tkinter.ttk import *


class Win_la5863h0:
    def __init__(self):
        self.root = self.__win()
        self.tk_button_la586g2p = self.__tk_button_la586g2p()
        self.tk_input_la586gvr = self.__tk_input_la586gvr()
        self.tk_label_la586ksd = self.__tk_label_la586ksd()
        self.tk_radio_button_la586nii = self.__tk_radio_button_la586nii()
        self.tk_check_button_la586oed = self.__tk_check_button_la586oed()
        self.tk_list_box_la586p8b = self.__tk_list_box_la586p8b()
        self.tk_select_box_la586qj5 = self.__tk_select_box_la586qj5()
        self.tk_progressbar_la586rmy = self.__tk_progressbar_la586rmy()
        self.tk_table_la586spx = self.__tk_table_la586spx()
        self.tk_frame_la586ttr = Frame_la586ttr(self.root)
        self.tk_label_frame_la586w89 = Frame_la586w89(self.root)
        self.tk_tabs_la586xk2 = Frame_la586xk2(self.root)

    def __win(self):
        root = Tk()
        root.title("我是标题 ~ Tkinter布局助手")
        # 设置大小 居中展示
        width = 900
        height = 500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(geometry)
        root.resizable(width=False, height=False)
        return root

    def __tk_button_la586g2p(self):
        btn = Button(self.root, text="按钮")
        btn.place(x=200, y=20, width=50, height=24)
        return btn

    def __tk_input_la586gvr(self):
        ipt = Entry(self.root)
        ipt.place(x=20, y=20, width=150, height=24)
        return ipt

    def __tk_label_la586ksd(self):
        label = Label(self.root, text="标签")
        label.place(x=30, y=70, width=50, height=24)
        return label

    def __tk_radio_button_la586nii(self):
        rb = Radiobutton(self.root, text="单选框")
        rb.place(x=120, y=80, width=80, height=24)
        return rb

    def __tk_check_button_la586oed(self):
        cb = Checkbutton(self.root, text="多选框")
        cb.place(x=220, y=80, width=120, height=24)
        return cb

    def __tk_list_box_la586p8b(self):
        lb = Listbox(self.root)
        lb.insert(END, "列表框")
        lb.insert(END, "Python")
        lb.insert(END, "Tkinter Helper")
        lb.place(x=140, y=140, width=150, height=100)
        return lb

    def __tk_select_box_la586qj5(self):
        cb = Combobox(self.root, state="readonly")
        cb['values'] = ("下拉选择框", "Python", "Tkinter Helper")
        cb.place(x=320, y=140, width=150, height=24)
        return cb

    def __tk_progressbar_la586rmy(self):
        progressbar = Progressbar(self.root, orient=HORIZONTAL)
        progressbar.place(x=60, y=260, width=150, height=24)
        return progressbar

    def __tk_table_la586spx(self):
        # 表头字段 表头宽度
        columns = {"ID": 50, "网站名": 100, "地址": 300}
        # 初始化表格 表格是基于Treeview，tkinter本身没有表格。show="headings" 为隐藏首列。
        tk_table = Treeview(self.root, show="headings", columns=list(columns))
        for text, width in columns.items():  # 批量设置列属性
            tk_table.heading(text, text=text, anchor='center')
            tk_table.column(text, anchor='center', width=width, stretch=False)  # stretch 不自动拉伸

        data = [
            [1, "github", "https://github.com/iamxcd/tkinter-helper"],
            [2, "演示地址", "https://www.pytk.net/tkinter-helper"]
        ]

        # 导入初始数据
        for values in data:
            tk_table.insert('', END, values=values)

        tk_table.place(x=30, y=410, width=450, height=70)
        return tk_table


class Frame_la586ttr:
    def __init__(self, parent):
        self.root = self.__frame(parent)

    def __frame(self, parent):
        frame = Frame(parent)
        frame.place(x=330, y=230, width=200, height=150)
        return frame


class Frame_la586w89:
    def __init__(self, parent):
        self.root = self.__frame(parent)

    def __frame(self, parent):
        frame = LabelFrame(parent, text="标签容器")
        frame.place(x=60, y=320, width=200, height=150)
        return frame


class Frame_la586xk2:
    def __init__(self, parent):
        self.root = self.__frame(parent)

    def __frame(self, parent):
        frame = Notebook(parent)

        tk_tabs_la586xk2_0 = Frame_la586xk2_0(frame)
        frame.add(tk_tabs_la586xk2_0.root, text="选项卡1")

        tk_tabs_la586xk2_1 = Frame_la586xk2_1(frame)
        frame.add(tk_tabs_la586xk2_1.root, text="选项卡2")

        frame.place(x=310, y=0, width=200, height=150)
        return frame


class Frame_la586xk2_0:
    def __init__(self, parent):
        self.root = self.__frame(parent)

    def __frame(self, parent):
        frame = Frame(parent)
        frame.place(x=310, y=0, width=200, height=150)
        return frame


class Frame_la586xk2_1:
    def __init__(self, parent):
        self.root = self.__frame(parent)

    def __frame(self, parent):
        frame = Frame(parent)
        frame.place(x=310, y=0, width=200, height=150)
        return frame


def run():
    win = Win_la5863h0()
    # TODO 绑定点击事件或其他逻辑处理
    win.root.mainloop()


if __name__ == "__main__":
    run()

