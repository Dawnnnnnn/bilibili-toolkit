#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/9/20 01:00
# @Author  : Dawnnnnnn
# @Contact: 1050596704@qq.com
from apis import *


async def set_private_run(action,uid,cookie, csrf, suname):
    await set_private(action,uid,cookie,csrf,suname)