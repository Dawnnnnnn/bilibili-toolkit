#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/9/18 00:01
# @Author  : Dawnnnnnn
# @Contact: 1050596704@qq.com
from printer import Printer
import platform
import asyncio
import time
import datetime
import hashlib
printer = Printer()


def get_accounts_file(filename):
    accounts = []
    try:
        with open(filename) as f:
            for line in f.readlines():
                line = line.strip('\n')
                accounts.append(line.split('----'))
        printer.printer(f'从{filename}文件里共获取到{len(accounts)}个账号', "Running", "green")
        return accounts
    except Exception as e:
        printer.printer(f'从{filename}文件里读取账号错误{e}', "Error", "red")
        exit()


def get_cookies_file(filename):
    cookies = []
    try:
        with open(filename) as f:
            for line in f.readlines():
                line = line.strip('\n')
                cookies.append(line)
        printer.printer(f'从{filename}文件里共获取到{len(cookies)}个账号cookie', "Running", "green")
        return cookies
    except Exception as e:
        printer.printer(f'从{filename}文件里读取账号错误{e}', "Error", "red")
        exit()


# 自动判断类型生成loop
def switch_sys_loop():
    sys_type = platform.system()
    if sys_type == "Windows":
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop)
    else:
        loop = asyncio.get_event_loop()

    return loop


# 计算sign
def calc_sign(str):
    str = str + "560c52ccd288fed045859ed18bffd973"
    hash = hashlib.md5()
    hash.update(str.encode('utf-8'))
    sign = hash.hexdigest()
    return sign


# 获取当前时间戳
def CurrentTime():
    currenttime = int(time.mktime(datetime.datetime.now().timetuple()))
    return str(currenttime)