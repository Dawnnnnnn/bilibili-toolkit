#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/9/16 22:20
# @Author  : Dawnnnnnn
# @Contact: 1050596704@qq.com
from apis import *


async def destory_account_run(uid, access_key, cookie, csrf, suname):
    # 删除关注
    await delete_all_follows(cookie, csrf, suname)
    # 删除粉丝
    await delete_all_fans(cookie, csrf, suname)
    # 删除收藏夹
    await delete_all_favorite_pack(uid, cookie, csrf, suname)
    # 删除直播勋章
    await delete_all_medals(cookie, csrf, suname)
    # 删除所有动态
    await delete_all_dynamic_ids(uid, cookie, access_key, suname)
