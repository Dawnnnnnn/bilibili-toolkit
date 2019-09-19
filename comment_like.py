#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/9/20 02:44
# @Author  : Dawnnnnnn
# @Contact: 1050596704@qq.com
from apis import *


async def comment_like_run(oid, otype, rpid, cookie, csrf, suname):
    await comment_like(oid, otype, rpid, cookie, csrf, suname)
