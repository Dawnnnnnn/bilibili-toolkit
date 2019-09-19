#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/9/20 00:18
# @Author  : Dawnnnnnn
# @Contact: 1050596704@qq.com
from apis import *


async def send_danmu_run(msg, roomid, cookie, csrf, suname):
    await send_danmu(msg, roomid, cookie, csrf, suname)
