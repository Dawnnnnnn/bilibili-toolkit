#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/9/16 22:17
# @Author  : Dawnnnnnn
# @Contact: 1050596704@qq.com
import re
import os
import toml
import aiohttp
from functions import *
from login import BiliLogin

config = toml.load('config.toml')


class Main:
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
        if config['set_private']['enable']:
            for action in ['fav_video', 'bangumi', 'tags', 'coins_video', 'user_info', 'played_game']:
                await set_private_run(action, uid, cookie, csrf, username)
        if config['coin_to_medal']['enable']:
            buy_uid = config['coin_to_medal']['buy_uid']
            await coin_to_medal_run(buy_uid, cookie, username)
        if config['sliver_to_coin']['enable']:
            await sliver_to_coin_run(cookie, csrf, username)
        if config['query_live_reward']['enable']:
            await query_live_reward_run(access_token, username)
        if config['draw_lottery']['enable']:
            aid = config['draw_lottery']['aid']
            number = config['draw_lottery']['number']
            await draw_lottery(aid, number, cookie, username)
        if config['query_system_notice']['enable']:
            await query_system_notice_run(cookie, username)
        if config['comment_like']['enable']:
            otype = config['comment_like']['type']
            oid = config['comment_like']['oid']
            rpid = config['comment_like']['rpid']
            await comment_like_run(oid, otype, rpid, cookie, csrf, username)
        if config['comment_hate']['enable']:
            otype = config['comment_hate']['type']
            oid = config['comment_hate']['oid']
            rpid = config['comment_hate']['rpid']
            await comment_hate_run(oid, otype, rpid, cookie, csrf, username)


Main().run()
