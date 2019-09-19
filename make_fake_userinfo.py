#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/9/16 22:25
# @Author  : Dawnnnnnn
# @Contact: 1050596704@qq.com
from apis import *


async def make_fake_info_run(uid, cookie, csrf, suname):
    # 更新用户信息
    response = await userinfo_3(cookie, suname)
    await update_info(response['data']['uname'], cookie, csrf, suname)
    # 添加追番
    response = await get_bangumi_list(suname)
    for k in range(0, len(response['data']['list'])):
        random_num = random.randint(1, 20)
        if random_num > 10:
            await add_bangumi_to_follow(response['data']['list'][k]['season_id'], cookie, csrf, suname)
    # 添加视频到收藏夹
    for _ in range(random.randint(4, 8)):
        av_id = await get_attention_video_or_random(cookie, suname)
        response = await get_all_favorite_pack(uid, cookie, suname)
        media_id = response['data']['archive'][0]['media_id']
        await add_something_to_favorite_pack(av_id, media_id, cookie, csrf, suname)
    # 订阅标签
    for _ in range(random.randint(3, 6)):
        await add_tag(random.randint(100, 1100), cookie, csrf, suname)
    # 随机关注
    response = await get_follow_uid_list(suname)
    for i in range(0, len(response['data'])):
        random_num = random.randint(1, 20)
        if random_num > 10:
            await follow(response['data'][i]['uid'], cookie, csrf, suname)
