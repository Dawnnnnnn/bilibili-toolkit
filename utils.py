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


# 删除文本数据
def delete_data(filename, mark):
    while True:
        try:
            with open(filename, "r", encoding="utf-8") as f:
                lines = f.readlines()
            with open(filename, "w", encoding="utf-8") as f_w:
                for line in lines:
                    if mark in line:
                        continue
                    f_w.write(line)
            printer.printer('删除文本完成', "Running", "green")
            break
        except Exception as e:
            printer.printer(f'删除文本失败 {e}', "Error", "red")


# 写入文本数据
def insert_data(filename, data):
    while True:
        try:
            with open(filename, "a+", encoding="utf-8") as f:
                f.write(data + "\n")
            printer.printer('写入文件成功!', "Running", "green")
            break
        except Exception as e:
            printer.printer(f'写入文件失败!{e}', "Error", "red")


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
        if len(cookies) == 0:
            printer.printer(f'cookies.txt内为空，继续读取accounts.txt文件', "Running", "green")
            return False
        return cookies
    except Exception as e:
        printer.printer(f'从{filename}文件里读取账号错误{e}', "Error", "red")
        exit()


def get_message_file(filename):
    msgs = []
    try:
        with open(filename) as f:
            for line in f.readlines():
                line = line.strip('\n')
                msgs.append(line)
        printer.printer(f'从{filename}文件里共获取到{len(msgs)}句预置信息', "Running", "green")
        if len(msgs) == 0:
            printer.printer(f'msgs.txt内为空', "Running", "green")
            return False
        return msgs
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
