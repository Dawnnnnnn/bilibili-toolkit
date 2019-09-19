#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/9/19 23:54
# @Author  : Dawnnnnnn
# @Contact: 1050596704@qq.com
from apis import *


async def clean_not_follow_up_run(uid,cookie, csrf, suname):
    follows = await get_all_follows_not_6(uid,cookie, suname)
    for follow_uid in follows:
        await unfollow(follow_uid, cookie, csrf, suname)

