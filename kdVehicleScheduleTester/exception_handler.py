'''
Created on 2019年4月8日

@author: bkd
'''
from tkinter import Tk, Label
from tkinter.constants import W, LEFT
import traceback


#     注册全局异常处理类
def show_error(*args):
    err_msg = "".join(traceback.format_exception(*args))
    print(err_msg)
    win = Tk(className="系统异常")
    Label(win, text=err_msg,
          anchor=W, justify=LEFT).pack()
    win.mainloop()


def set_global_callback(parent):
    parent._root().report_callback_exception = show_error
