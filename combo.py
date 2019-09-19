#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/9/19 23:28
# @Author  : Dawnnnnnn
# @Contact: 1050596704@qq.com
from apis import *


async def combo_run(aid, uid, access_key, cookie, csrf, suname):
    await watch_av(aid, uid, csrf, cookie, suname)
    await share(aid, access_key, suname)
    await combo(aid, csrf, cookie, suname)
