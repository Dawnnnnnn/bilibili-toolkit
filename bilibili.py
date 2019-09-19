#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/9/16 22:17
# @Author  : Dawnnnnnn
# @Contact: 1050596704@qq.com
from login import BiliLogin
import toml
import re
import aiohttp
import os
from check_account_state import *
from make_fake_userinfo import *
from level_task import *
from clean_dynamic import *
from follow import *
from combo import *
from clean_not_follow_up import *
from clean_not_follow_fan import *
from wear_medal import *
from send_danmu import *

config = toml.load('config.toml')


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
            task_req = [request.req_loop()]
            task_list = task_req + task_work
            loop.run_until_complete(asyncio.wait(task_list))
            loop.close()

    async def main_loop(self, thread, username, password):
        await asyncio.sleep(random.randint(1, 3) * thread)
        printer.printer(f"第{thread}个账号开始工作", "Info", "blue")
        uname, cookie, access_token = BiliLogin().login(username, password)
        s1 = re.findall(r'bili_jct=(\S+)', cookie, re.M)
        csrf = s1[0].split(";")[0]
        s2 = re.findall(r'DedeUserID=(\S+)', cookie, re.M)
        uid = s2[0].split(";")[0]
        if username not in request.ssion.keys():
            request.ssion[username] = aiohttp.ClientSession()
        if config['get_user_info']['enable']:
            await check_account_state_run(uid, cookie, username)
        if config['destory_account']['enable']:
            printer.printer("危险操作，自己写await", "DEBUG", "yellow")
        if config['make_fake_userinfo']['enable']:
            await make_fake_info_run(uid, cookie, csrf, username)
        if config['level_task']['enable']:
            await level_task_run(uid, access_token, cookie, csrf, username)
        if config['combo']['enable']:
            aid_list = config['combo']['av_list']
            for aid in aid_list:
                await combo_run(aid, uid, access_token, cookie, csrf, username)
        if config['clean_dynamic']['enable']:
            await clean_dynamic_run(uid, access_token, cookie, username)
        if config['follow']['enable']:
            uid_list = config['follow']['uid_list']
            for uid in uid_list:
                await follow_run(uid, cookie, csrf, username)
        if config['clean_not_follow_up']['enable']:
            await clean_not_follow_up_run(uid, cookie, csrf, username)
        if config['clean_not_follow_fan']['enable']:
            await clean_not_follow_fan_run(uid, cookie, csrf, username)
        if config['wear_medal']['enable']:
            medal_id = config['wear_medal']['medal_id']
            await wear_medal_run(medal_id, cookie, username)
        if config['send_danmu']['enable']:
            msg = config['send_danmu']['msg']
            roomid = config['send_danmu']['roomid']
            await send_danmu_run(msg, roomid, cookie, csrf, username)


Main().run()
