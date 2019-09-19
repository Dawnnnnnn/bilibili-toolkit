#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/9/19 23:14
# @Author  : Dawnnnnnn
# @Contact: 1050596704@qq.com
from apis import *


async def level_task_run(uid, access_key, cookie, csrf, suname):
    await watch_av_random(uid, csrf, cookie, suname)
    await share_random(cookie, access_key, suname)
