#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/9/16 22:17
# @Author  : Dawnnnnnn
# @Contact: 1050596704@qq.com
from login import BiliLogin
import toml
import aiohttp
import random
import os
from os_utils import *
from requests_utils import Request

request = Request()

# config = toml.load('config.toml')
printer = Printer()


class Main():
    def __init__(self):
        self.accounts = []
        self.cookies = []
        self.threads = 0

    def run(self):
        if os.path.exists("cookies.txt"):
            self.cookies = get_cookies_file('cookies.txt')
        elif os.path.exists("accounts.txt"):
            self.accounts = get_accounts_file('accounts.txt')
        loop = switch_sys_loop()
        if self.cookies:
            pass
        elif self.accounts:
            self.threads = len(self.accounts)
            # 协程任务 # 测试阶段，用login代替任务
            task_work = [
                self.main_loop(thread, account_info[0], account_info[1])
                for thread, account_info in
                zip(range(0, self.threads), self.accounts)
            ]
            # task_req = [Request().req_loop()]
            # task_list = task_req + task_work
            loop.run_until_complete(asyncio.wait(task_work))
            loop.close()

    async def main_loop(self, thread, username, password):
        await asyncio.sleep(random.randint(1, 3) * thread)
        printer.printer(f"第{thread}个账号开始工作", "Info", "blue")
        uname, cookie = BiliLogin().login(username, password)
        printer.printer(cookie,"INFO","blue")
        # if username not in request.ssion.keys():
        #     request.ssion[username] = aiohttp.ClientSession()

        #
        # data = await self.user_status(self.add_headers(cookie),
        #                               username)
Main().run()
