#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/9/21 00:16
# @Author  : Dawnnnnnn
# @Contact: 1050596704@qq.com
import asyncio
from apis import *


async def check_account_state_run(uid, cookie, suname):
    response_1 = await userinfo_1(uid, cookie, suname)
    printer.printer(response_1,"DEBUG","yellow")
    response_2 = await userinfo_2(cookie, suname)
    printer.printer(response_2,"DEBUG","yellow")
    # response_3 = await userinfo_3(cookie, suname)
    # printer.printer(response_3,"DEBUG","yellow")
    response_4 = await userinfo_4(cookie, suname)
    printer.printer(response_4,"DEBUG","yellow")
    printer.printer(
        f"({response_1['data']['name']} {uid}) 封禁状态:{response_1['data']['silence']} 用户类型:{response_2['data']['userStatus']} 主站等级:{response_2['data']['level_info']['current_level']}({response_2['data']['level_info']['current_exp']}/{response_2['data']['level_info']['next_exp']}) 硬币:{response_2['data']['coins']} 直播站等级:{response_4['data']['user_level']}({response_4['data']['user_intimacy']}/{response_4['data']['user_next_intimacy']}) 银瓜子:{response_4['data']['silver']}",
        "INFO", "blue")


async def clean_dynamic_run(uid, access_key, cookie, suname):
    await delete_all_dynamic_ids(uid, cookie, access_key, suname)


async def clean_not_follow_fan_run(uid, cookie, csrf, suname):
    response = await get_all_fans(uid, cookie, suname)
    for k in range(0, len(response['data']['list'])):
        if response['data']['list'][k]['attribute'] != 6:
            await delete_fans(response['data']['list'][k]['mid'], cookie, csrf, suname)


async def clean_not_follow_up_run(uid, cookie, csrf, suname):
    follows = await get_all_follows_not_6(uid, cookie, suname)
    for follow_uid in follows:
        await unfollow(follow_uid, cookie, csrf, suname)


async def coin_to_medal_run(buy_uid, cookie, suname):
    await coin_to_medal(buy_uid, cookie, suname)


async def combo_run(aid, uid, access_key, cookie, csrf, suname):
    await watch_av(aid, uid, csrf, cookie, suname)
    await share(aid, access_key, suname)
    await combo(aid, csrf, cookie, suname)


async def comment_hate_run(oid, otype, rpid, cookie, csrf, suname):
    await comment_hate(oid, otype, rpid, cookie, csrf, suname)


async def comment_like_run(oid, otype, rpid, cookie, csrf, suname):
    await comment_like(oid, otype, rpid, cookie, csrf, suname)


async def destory_account_run(uid, access_key, cookie, csrf, suname):
    # 删除关注
    await delete_all_follows(cookie, csrf, suname)
    # 删除粉丝
    await delete_all_fans(uid, cookie, csrf, suname)
    # 删除收藏夹
    await delete_all_favorite_pack(uid, cookie, csrf, suname)
    # 删除直播勋章
    await delete_all_medals(cookie, csrf, suname)
    # 删除所有动态
    await delete_all_dynamic_ids(uid, cookie, access_key, suname)
    # 退出友爱社
    await quit_unionfans(cookie, suname)
    # 删除订阅番剧
    response = await get_owner_bangumi_list(uid, cookie, suname)
    for k in range(0, len(response['data']['list'])):
        await del_bangumi_in_follow(response['data']['list'][k]['season_id'], cookie, csrf, suname)
    # 随机消耗硬币
    # for _ in range(200):
    #     av_num = await get_attention_video_or_random(cookie, suname)
    #     await combo(av_num, csrf, cookie, suname)


async def draw_lottery_run(aid, number, cookie, suname):
    await draw_lottery(aid, number, cookie, suname)


async def follow_run(follow_uid, cookie, csrf, suname):
    await follow(follow_uid, cookie, csrf, suname)


async def level_task_run(uid, access_key, cookie, csrf, suname):
    await watch_av_random(uid, csrf, cookie, suname)
    await share_random(cookie, access_key, suname)


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


async def query_live_reward_run(access_key, suname):
    await query_live_reward(access_key, suname)


async def query_system_notice_run(cookie, suname):
    await query_system_notice(cookie, suname)


async def send_danmu_run(msg, roomid, cookie, csrf, suname):
    await send_danmu(msg, roomid, cookie, csrf, suname)


async def set_private_run(action, uid, cookie, csrf, suname):
    await set_private(action, uid, cookie, csrf, suname)


async def sliver_to_coin_run(cookie, csrf, suname):
    await sliver_to_coin(cookie, csrf, suname)


async def wear_medal_run(medal, cookie, suname):
    await wear_medal(medal, cookie, suname)


async def act_id_lottery_run(act_id, get_chance, sleep, cookie, suname):
    for i in range(0, get_chance):
        await act_id_get_chance(act_id, cookie, suname)
        await asyncio.sleep(sleep)
    response = await act_id_check_chance(act_id, cookie, suname)
    if response['data']['times'] >= 90:
        pass
    else:
        for _ in range(0, response['data']['times']):
            await act_id_lottery(act_id, cookie, suname)
            await asyncio.sleep(sleep)


async def comment_send_run(oid, otype, message, cookie, csrf, suname):
    await comment_send(oid, otype, message, cookie, csrf, suname)


async def comment_reply_run(oid, otype, message, root, parent, cookie, csrf, suname):
    await comment_reply(oid, otype, root, parent, message, cookie, csrf, suname)
