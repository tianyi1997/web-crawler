import tkinter as tk  # 使用Tkinter前需要先导入
from tkinter import ttk
import urllib.request
import time
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


def get_prices():
    target_prices = {}
    for target in targets:
        prices = []
        price = []
        url = 'https://www.shfe.com.cn/statements/delaymarket_' + target + '.html'
        response = urllib.request.urlopen(url)
        content = response.read().decode('utf-8').split('\n')
        for line in content:
            if '"合约名称"' in line:
                price.append(line[33:-5])
            elif '"最新价"' in line:
                price.append(line[50:-5])
                prices.append(price)
                price = []
        target_prices[target] = prices
    return target_prices


def init_trees():
    target_prices = get_prices()
    for target in targets:
        tree = trees[target]
        tree["columns"] = ("合约名称", "最新价")
        tree.column("合约名称", width=75, anchor='center')
        tree.column("最新价", width=75, anchor='center')
        tree.heading("合约名称", text="合约名称")  # #设置显示的表头名
        tree.heading("最新价", text="最新价")
        tree.tag_configure('oddrow', background='white')
        for i, price in enumerate(target_prices[target]):
            if i%2:
                tree.insert('', i, values=(price[0], price[1]), tags=('oddrow',))
            else:
                tree.insert('', i, values=(price[0], price[1]), tags=('evenrow',))
        tree.pack()


def update_trees():
    print('update')
    target_prices = get_prices()
    for target in targets:
        tree = trees[target]
        for i, row in enumerate(tree.get_children()):
            tree.item(row, values=(target_prices[target][i][0], target_prices[target][i][1]))
        trees[target] = tree


def refresh():
    update_trees()
    time_var.set(time.strftime('%m月%d日%H时%M分%S秒', time.localtime()))
    window.after(1000 * 60 * minute_interval, refresh)


if __name__ == '__main__':
    minute_interval = 10
    targets = ['cu', 'al', 'rb', 'ss', 'hc']
    window = tk.Tk()
    style = ttk.Style()
    settings = {
        'TNotebook.Tab': {
                          "configure": {"background": "#fdd57e",
                                        "padding": [1, 1]},
                          "map": {"background": [("selected", "#C70039"),
                                                 ("active", "#fc9292")],
                                  "foreground": [("selected", "#ffffff"),
                                                 ("active", "#000000")]
                                  }
                          }
    }
    style.theme_create("MyStyle", settings=settings)
    style.theme_use("MyStyle")
    style.configure('TNotebook', tabposition='n')

    window.title('期货行情')
    screenwidth = window.winfo_screenwidth()
    screenheight = window.winfo_screenheight()
    width = 150
    height = 315
    alignstr = '%dx%d+%d+%d' % (width, height, screenwidth - width - 30, 10)
    window.geometry(alignstr)  # 这里的乘是小x
    window.resizable(0, 0)

    tab = ttk.Notebook(window)
    frame1 = tk.Frame(tab)
    tab1 = tab.add(frame1, text="CU")
    frame2 = tk.Frame(tab)
    tab2 = tab.add(frame2, text="AL")
    frame3 = tk.Frame(tab)
    tab3 = tab.add(frame3, text="RB")
    frame4 = tk.Frame(tab)
    tab4 = tab.add(frame4, text="SS")
    frame5 = tk.Frame(tab)
    tab5 = tab.add(frame5, text="HC")
    tab.pack(expand=True, fill=tk.BOTH)

    #    window.overrideredirect(1)  # 去除窗口边框
    window.wm_attributes("-alpha", 0.9)  # 透明度(0.0~1.0)
    # window.wm_attributes("-toolwindow", True)  # 置为工具窗口(没有最大最小按钮)
    window.wm_attributes("-topmost", True)  # 永远处于顶层
    trees = {'cu': ttk.Treeview(frame1, show="headings", height=12),
             'al': ttk.Treeview(frame2, show="headings", height=12),
             'rb': ttk.Treeview(frame3, show="headings", height=12),
             'ss': ttk.Treeview(frame4, show="headings", height=12),
             'hc': ttk.Treeview(frame5, show="headings", height=12)}
    init_trees()

    time_var = tk.StringVar()
    time_var.set(time.strftime('%m月%d日%H时%M分%S秒', time.localtime()))
    time_label = tk.Label(window, textvariable=time_var, font=('Arial', 10), width=200, height=1)
    time_label.pack()

    #    quit_button = tk.Button(text="退出", command=window.destroy)
    #    quit_button.pack()

    #    window.bind("<ButtonPress-1>", StartMove)  # 监听左键按下操作响应函数
    #    window.bind("<ButtonRelease-1>", StopMove)  # 监听左键松开操作响应函数
    #    window.bind("<B1-Motion>", OnMotion)  # 监听鼠标移动操作响应函数

    window.after(1000 * 60 * minute_interval, refresh)
    window.mainloop()
