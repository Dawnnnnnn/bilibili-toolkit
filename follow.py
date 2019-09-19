#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/9/19 23:47
# @Author  : Dawnnnnnn
# @Contact: 1050596704@qq.com
from apis import *


async def follow_run(follow_uid, cookie, csrf, suname):
    await follow(follow_uid, cookie, csrf, suname)
