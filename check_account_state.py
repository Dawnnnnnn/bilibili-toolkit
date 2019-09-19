#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/9/16 22:24
# @Author  : Dawnnnnnn
# @Contact: 1050596704@qq.com
from apis import *


async def check_account_state_run(uid, cookie, suname):
    response_1 = await userinfo_1(uid, cookie, suname)
    # printer.printer(response_1,"DEBUG","yellow")
    response_2 = await userinfo_2(cookie, suname)
    # printer.printer(response_2,"DEBUG","yellow")
    # response_3 = await userinfo_3(cookie, suname)
    # printer.printer(response_3,"DEBUG","yellow")
    response_4 = await userinfo_4(cookie, suname)
    # printer.printer(response_4,"DEBUG","yellow")
    printer.printer(f"{response_1['data']['name']}({uid}) 封禁状态:{response_1['data']['silence']} 用户类型:{response_2['data']['userStatus']} 主站等级:{response_2['data']['level_info']['current_level']}({response_2['data']['level_info']['current_exp']}/{response_2['data']['level_info']['next_exp']}) 硬币:{response_2['data']['coins']} 直播站等级:{response_4['data']['user_level']}({response_4['data']['user_intimacy']}/{response_4['data']['user_next_intimacy']}) 银瓜子:{response_4['data']['silver']}","INFO","blue")