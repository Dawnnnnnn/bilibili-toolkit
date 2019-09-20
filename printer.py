#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/9/17 23:07
# @Author  : Dawnnnnnn
# @Contact: 1050596704@qq.com
import time
import inspect
from termcolor import *
from colorama import init
init()


class Printer:
    # 格式化时间
    @staticmethod
    def current_time():
        return f"[{str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))}]"

    # 格式化打印
    def printer(self, string, info, color):
        ctm = self.current_time()
        tmp = "[" + str(info) + "]"
        row = "[" + str(inspect.stack()[1][3]) + ":" + str(
            inspect.stack()[1][2]) + "]"
        msg = (
            "{:<22}{:<10}{:<28}{:<20}".format(str(ctm), str(tmp), str(row),
                                              str(string)))
        print(colored(msg, color), flush=True)
