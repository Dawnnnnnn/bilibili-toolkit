#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/9/20 02:57
# @Author  : Dawnnnnnn
# @Contact: 1050596704@qq.com
from apis import *


async def comment_hate_run(oid, otype, rpid, cookie, csrf, suname):
    await comment_hate(oid, otype, rpid, cookie, csrf, suname)
