#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/9/17 22:45
# @Author  : Dawnnnnnn
# @Contact: 1050596704@qq.com
from requests_utils import Request
import random
from os_utils import *
import json

request = Request()
printer = Printer()


# 取消关注 (直播站接口)
async def delete_follow(follow_uid, cookie, csrf, suname):
    url = "https://api.live.bilibili.com/liveact/attention"
    data = {
        "type": 0,
        "uid": follow_uid,
        "token": "",
        "csrf_token": csrf,
        "csrf": csrf
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
        "Cookie": cookie
    }
    response = await request.req_add_job('post', url, data=data, headers=headers, suname=suname)
    response = json.loads(response)
    printer.printer(f"取消关注{follow_uid}回显:{response}", "INFO", "blue")


# 根据勋章id删除勋章
async def delete_medal(medal_id, cookie, csrf, suname):
    url = "https://api.live.bilibili.com/i/ajaxDeleteMyFansMedal"
    data = {
        "medal_id": medal_id,
        "csrf_token": csrf,
        "csrf": csrf
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
        "Cookie": cookie
    }
    response = await request.req_add_job('post', url, data=data, headers=headers, suname=suname)
    response = json.loads(response)
    printer.printer(f"删除勋章{medal_id}回显:{response}", "INFO", "blue")


# 根据粉丝uid删除粉丝
async def delete_fans(fan_uid, cookie, csrf, suname):
    url = "https://api.bilibili.com/x/relation/modify"
    data = {
        "fid": fan_uid,
        "act": 7,
        "re_src": 11,
        "jsonp": "jsonp",
        "csrf": csrf
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
        "Cookie": cookie
    }
    response = await request.req_add_job('post', url, data=data, headers=headers, suname=suname)
    response = json.loads(response)
    printer.printer(f"删除粉丝{fan_uid}回显:{response}", "INFO", "blue")


# 根据收藏夹id删除收藏夹
async def delete_favorite_pack(media_ids, cookie, csrf, suname):
    url = "https://api.bilibili.com/medialist/gateway/base/del"
    data = {
        "media_ids": media_ids,
        "jsonp": "jsonp",
        "csrf": csrf
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
        "Cookie": cookie
    }
    response = await request.req_add_job('post', url, data=data, headers=headers, suname=suname)
    response = json.loads(response)
    printer.printer(f"删除收藏夹{media_ids}回显:{response}", "INFO", "blue")


# 根据动态id删除动态
async def del_dynamic_by_id(uid, dy_id, cookie, access_key, suname):
    url = 'https://api.vc.bilibili.com/dynamic_repost/v1/dynamic_repost/rm_rp_dyn'
    temp_data = f"_device=android&_hwid=SX1NL0wuHCsaKRt4BHhIfRguTXxOfj5WN1BkBTdLfhstTn9NfUouFiUV&access_key={access_key}&appkey=1d8b6e7d45233436&build=5310300&dynamic_id={dy_id}&mobi_app=android&platform=android&src=meizu&trace_id=20180909020900047&ts={CurrentTime() * 1000}&uid={uid}&version=5.31.3.5310300"
    data = f"{temp_data}&sign={calc_sign(temp_data)}"
    headers = {
        "User-Agent": "Mozilla/5.0 BiliDroid/5.31.3 (bbcallen@gmail.com)",
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        "Cookie": cookie
    }
    response = await request.req_add_job('post', url, data=data, headers=headers, suname=suname)
    response = json.loads(response)
    printer.printer(f"删除动态{dy_id}回显:{response}", "INFO", "blue")


# 获取所有关注的另一种写法
# async def get_all_follows(uid, cookie, suname):
#     url = f"https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?visitor_uid={uid}&host_uid={uid}"
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
#         "Cookie": cookie
#     }
#     response = await request.req_add_job('get', url, headers=headers, suname=suname)
#     response = json.loads(response)
#     return response

# 获取所有关注人
async def get_all_follows(cookie, suname):
    follows = []
    page = 1
    while 1:
        url = f"https://api.live.bilibili.com/i/api/following?page={page}&pageSize=20"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
            "Cookie": cookie
        }
        response = await request.req_add_job('get', url, headers=headers, suname=suname)
        response = json.loads(response)
        if response['data']['list']:
            for k in range(0, len(response['data']['list'])):
                follows.append(response['data']['list'][k]['mid'])
            page = page + 1
            continue
        else:
            break
    return follows


# 获取没有互粉的关注人
async def get_all_follows_not_6(cookie, suname):
    follows = []
    page = 1
    while 1:
        url = f"https://api.live.bilibili.com/i/api/following?page={page}&pageSize=20"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
            "Cookie": cookie
        }
        response = await request.req_add_job('get', url, headers=headers, suname=suname)
        response = json.loads(response)
        if response['data']['list']:
            for k in range(0, len(response['data']['list'])):
                if response['data']['list'][k]['attribute'] != 6:
                    follows.append(response['data']['list'][k]['mid'])
            page = page + 1
            continue
        else:
            break
    return follows


# 获取所有勋章
async def get_all_medal(cookie, suname):
    url = "https://api.live.bilibili.com/i/api/medal?page=1&pageSize=30"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
        "Cookie": cookie
    }
    response = await request.req_add_job('get', url, headers=headers, suname=suname)
    response = json.loads(response)
    return response


# 获取自己的100个粉丝
async def get_all_fans(cookie, suname):
    """
    印象中这个删除粉丝，每小时有数量限制，先设置成清除100个
    :param cookie:
    :param csrf:
    :param suname:
    :return:
    """

    url = "https://api.bilibili.com/x/relation/followers?vmid=48766812&pn=1&ps=100&order=desc"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
        "Cookie": cookie
    }
    response = await request.req_add_job('get', url, headers=headers, suname=suname)
    response = json.loads(response)
    return response


# 获取所有收藏夹id
async def get_all_favorite_pack(uid, cookie, suname):
    url = f"https://api.bilibili.com/x/space/fav/nav?mid={uid}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
        "Cookie": cookie
    }
    response = await request.req_add_job('get', url, headers=headers, suname=suname)
    response = json.loads(response)
    return response


# 获取所有动态id
async def get_all_dynamic(uid, cookie, access_key, suname):
    dy_id = 0
    dy_uid_list = []
    start = 1
    while 1:
        temp_params = f"_device=android&_hwid=SX1NL0wuHCsaKRt4BHhIfRguTXxOfj5WN1BkBTdLfhstTn9NfUouFiUV&access_key={access_key}&appkey=1d8b6e7d45233436&build=5310300&host_uid={uid}&mobi_app=android&offset_dynamic_id={dy_id}&page={start}&platform=android&qn=32&src=meizu&trace_id=20180908182200005&ts={CurrentTime()}&version=5.31.3.5310300&visitor_uid={uid}"
        url = f"https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?{temp_params}&sign={calc_sign(temp_params)}"
        headers = {
            "User-Agent": "Mozilla/5.0 BiliDroid/5.31.3 (bbcallen@gmail.com)",
            "Cookie": cookie
        }

        response = await request.req_add_job("get", url, headers=headers, suname=suname)
        exist = (response.json()['data']['has_more'])
        if exist == 0:
            break
        _len = len(response.json()['data']['cards'])
        for i in range(0, _len):
            dyid = response.json()['data']['cards'][i]['desc']['dynamic_id']
            dy_uid_list.append(dyid)
        dy_id = response.json()['data']['cards'][_len - 1]['desc']['dynamic_id']
        start = start + 1
        continue
    return dy_uid_list


# 清空自己的关注人
async def delete_all_follows(cookie, csrf, suname):
    follows = await get_all_follows(cookie, suname)
    for follow_uid in follows:
        await delete_follow(follow_uid, cookie, csrf, suname)


# 清空自己的所有勋章
async def delete_all_medals(cookie, csrf, suname):
    response = await get_all_medal(cookie, suname)
    for k in range(0, len(response['data']['fansMedalList'])):
        await delete_medal(response['data']['fansMedalList']['id'], cookie, csrf, suname)


# 清空自己的全部粉丝
async def delete_all_fans(cookie, csrf, suname):
    response = await get_all_fans(cookie, suname)
    for k in range(0, len(response['data']['list'])):
        await delete_fans(response['data']['list']['mid'], cookie, csrf, suname)


# 清空自己的所有收藏夹
async def delete_all_favorite_pack(uid, cookie, csrf, suname):
    response = await get_all_favorite_pack(uid, cookie, suname)
    for k in range(0, len(response['data']['archive'])):
        await delete_favorite_pack(response['data']['archive']['media_id'], cookie, csrf, suname)


# 清空所有的动态
async def delete_all_dynamic_ids(uid, cookie, access_key, suname):
    dynamic_ids = await get_all_dynamic(uid, cookie, access_key, suname)
    for dy_id in dynamic_ids:
        await del_dynamic_by_id(uid, dy_id, cookie, access_key, suname)


# 关注
async def follow(follow_uid, cookie, csrf, suname):
    url = "https://api.bilibili.com/x/relation/modify"
    data = {
        "fid": follow_uid,
        "act": 1,
        "re_src": 11,
        "jsonp": "jsonp",
        "csrf": csrf
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
        "Cookie": cookie
    }
    response = await request.req_add_job('post', url, data=data, headers=headers, suname=suname)
    response = json.loads(response)
    printer.printer(f"关注{follow_uid}回显:{response}", "INFO", "blue")


# 取消关注 (主站接口)
async def unfollow(follow_uid, cookie, csrf, suname):
    url = "https://api.bilibili.com/x/relation/modify"
    data = {
        "fid": follow_uid,
        "act": 2,
        "re_src": 11,
        "jsonp": "jsonp",
        "csrf": csrf
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
        "Cookie": cookie
    }
    response = await request.req_add_job('post', url, data=data, headers=headers, suname=suname)
    response = json.loads(response)
    printer.printer(f"取关{follow_uid}回显:{response}", "INFO", "blue")


# 删除没有互粉的粉丝
async def delete_not_exchange_fans(cookie, csrf, suname):
    response = await get_all_fans(cookie, suname)
    for k in range(0, len(response['data']['list'])):
        if response['data']['list'][k]['attribute'] != 6:
            await delete_fans(response['data']['list']['mid'], cookie, csrf, suname)


# 删除没有互粉的关注人
async def delete_not_exchange_follows(cookie, csrf, suname):
    follows = await get_all_follows_not_6(cookie, suname)
    for follow_uid in follows:
        await delete_follow(follow_uid, cookie, csrf, suname)


# 视频av转cid
async def get_av_cid(aid, cookie, suname):
    url = f"https://api.bilibili.com/x/player/pagelist?aid={aid}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
        "Cookie": cookie
    }
    response = await request.req_add_job('get', url, headers=headers, suname=suname)
    response = json.loads(response)
    if response['code'] == 0:
        cid = response['data']['cid']
    else:
        cid = 0
    return cid


# 随机得到一个av号
async def get_attention_video_or_random(cookie, suname):
    follows = await get_all_follows(cookie, suname)
    video_list = []
    for mid in follows:
        url = f"https://space.bilibili.com/ajax/member/getSubmitVideos?mid={mid}&pagesize=100&tid=0"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
            "Cookie": cookie
        }
        response = await request.req_add_job('get', url, headers=headers, suname=suname)
        response = json.loads(response)
        datalen = len(response.json()['data']['vlist'])
        for i in range(0, datalen):
            aid = response.json()['data']['vlist'][i]['aid']
            video_list.append(aid)
        if len(video_list) >= 5:
            break
    if video_list:
        return random.choice(video_list)
    else:
        while 1:
            av_num = random.randint(10000000, 67967399)
            cid = await get_av_cid(av_num, cookie, suname)
            if cid != 0:
                return av_num
            else:
                continue


# 随机分享一个视频，用于完成每日任务
async def share_random(cookie, access_key, suname):
    av_num = await get_attention_video_or_random(cookie, suname)
    url = "https://app.bilibili.com/x/v2/view/share/add"
    headers = {
        "User-Agent": "Mozilla/5.0 BiliDroid/5.26.3 (bbcallen@gmail.com)",
        "Host": "app.bilibili.com",
        "Cookie": "sid=8wfvu7i7"
    }
    temp_params = f"access_key={access_key}&aid={av_num}&appkey=1d8b6e7d45233436&build=5260003&from=7&mobi_app=android&platform=android&ts={CurrentTime()}"
    sign = calc_sign(temp_params)
    data = {
        "access_key": access_key,
        "aid": av_num,
        "appkey": "1d8b6e7d45233436",
        "build": "5260003",
        "from": "7",
        "mobi_app": "android",
        "platform": "android",
        "ts": CurrentTime(),
        "sign": sign
    }
    response = await request.req_add_job('post', url, headers=headers, data=data, suname=suname)
    response = json.loads(response)
    printer.printer(f"分享视频{av_num}回显:{response}", "INFO", "blue")


# 根据av号分享视频
async def share(av_num, access_key, suname):
    url = "https://app.bilibili.com/x/v2/view/share/add"
    headers = {
        "User-Agent": "Mozilla/5.0 BiliDroid/5.26.3 (bbcallen@gmail.com)",
        "Host": "app.bilibili.com",
        "Cookie": "sid=8wfvu7i7"
    }
    temp_params = f"access_key={access_key}&aid={av_num}&appkey=1d8b6e7d45233436&build=5260003&from=7&mobi_app=android&platform=android&ts={CurrentTime()}"
    sign = calc_sign(temp_params)
    data = {
        "access_key": access_key,
        "aid": av_num,
        "appkey": "1d8b6e7d45233436",
        "build": "5260003",
        "from": "7",
        "mobi_app": "android",
        "platform": "android",
        "ts": CurrentTime(),
        "sign": sign
    }
    response = await request.req_add_job('post', url, headers=headers, data=data, suname=suname)
    response = json.loads(response)
    printer.printer(f"分享视频{av_num}回显:{response}", "INFO", "blue")


# 随机观看一个视频，用于完成每日任务
async def watch_av_random(uid, csrf, cookie, suname):
    av_num = await get_attention_video_or_random(cookie, suname)
    url = "https://api.bilibili.com/x/report/web/heartbeat"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
        "Referer": f"https://www.bilibili.com/video/av{av_num}",
        "Cookie": cookie
    }
    cid = await get_av_cid(av_num, cookie, suname)
    data = {
        "aid": av_num,
        "cid": cid,
        "mid": uid,
        "csrf": csrf,
        "played_time": "0",
        "realtime": "0",
        "start_ts": CurrentTime(),
        "type": "3",
        "dt": "2",
        "play_type": "1"
    }
    response = await request.req_add_job('post', url, headers=headers, data=data, suname=suname)
    response = json.loads(response)
    printer.printer(f"观看视频{av_num}回显:{response}", "INFO", "blue")


# 根据av号观看视频
async def watch_av(av_num, uid, csrf, cookie, suname):
    url = "https://api.bilibili.com/x/report/web/heartbeat"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
        "Referer": f"https://www.bilibili.com/video/av{av_num}",
        "Cookie": cookie
    }
    cid = await get_av_cid(av_num, cookie, suname)
    data = {
        "aid": av_num,
        "cid": cid,
        "mid": uid,
        "csrf": csrf,
        "played_time": "0",
        "realtime": "0",
        "start_ts": CurrentTime(),
        "type": "3",
        "dt": "2",
        "play_type": "1"
    }
    response = await request.req_add_job('post', url, headers=headers, data=data, suname=suname)
    response = json.loads(response)
    printer.printer(f"观看视频{av_num}回显:{response}", "INFO", "blue")


# 根据av号一键三连
async def combo(aid, csrf, cookie, suname):
    url = f"https://api.bilibili.com/x/web-interface/archive/like/triple"
    data = {
        'aid': aid,
        'csrf': csrf,
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
        "Referer": f"https://www.bilibili.com/video/av{aid}",
        "Cookie": cookie
    }
    response = await request.req_add_job('post', url, headers=headers, data=data, suname=suname)
    response = json.loads(response)
    printer.printer(f"三连视频{aid}回显:{response}", "INFO", "blue")
