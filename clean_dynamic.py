#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/9/19 23:40
# @Author  : Dawnnnnnn
# @Contact: 1050596704@qq.com
from apis import *


async def clean_dynamic_run(uid, access_key, cookie, suname):
    await delete_all_dynamic_ids(uid, cookie, access_key, suname)
