#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/9/19 23:57
# @Author  : Dawnnnnnn
# @Contact: 1050596704@qq.com
from apis import *


async def clean_not_follow_fan_run(uid,cookie, csrf, suname):
    response = await get_all_fans(uid,cookie, suname)
    for k in range(0, len(response['data']['list'])):
        if response['data']['list'][k]['attribute'] != 6:
            await delete_fans(response['data']['list'][k]['mid'], cookie, csrf, suname)
