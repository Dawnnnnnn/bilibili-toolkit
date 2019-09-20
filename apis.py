#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/9/17 22:45
# @Author  : Dawnnnnnn
# @Contact: 1050596704@qq.com
import json
import random
from utils import *
from PIL import Image
from io import BytesIO
from network import Request

request = Request()


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
                follows.append(response['data']['list'][k]['uid'])
            page = page + 1
            continue
        else:
            break
    return follows


# 获取没有互粉的关注人
async def get_all_follows_not_6(uid, cookie, suname):
    follows = []
    page = 1
    while 1:
        url = f"https://api.bilibili.com/x/relation/followings?vmid={uid}&pn={page}&ps=20&order=desc&jsonp=jsonp"
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
async def get_all_fans(uid, cookie, suname):
    """
    印象中这个删除粉丝，每小时有数量限制，先设置成清除100个
    :param cookie:
    :param csrf:
    :param suname:
    :return:
    """

    url = f"https://api.bilibili.com/x/relation/followers?vmid={uid}&pn=1&ps=100&order=desc"
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
        response = json.loads(response)
        exist = (response['data']['has_more'])
        if exist == 0:
            break
        _len = len(response['data']['cards'])
        for i in range(0, _len):
            dyid = response['data']['cards'][i]['desc']['dynamic_id']
            dy_uid_list.append(dyid)
        dy_id = response['data']['cards'][_len - 1]['desc']['dynamic_id']
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
        await delete_fans(response['data']['list'][k]['mid'], cookie, csrf, suname)


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
        cid = response['data'][0]['cid']
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
        datalen = len(response['data']['vlist'])
        for i in range(0, datalen):
            aid = response['data']['vlist'][i]['aid']
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


# 主站信息获取 接口 1
async def userinfo_1(uid, cookie, suname):
    """
    ['data']['silence'] == 1 封禁
                        == 0 未封禁
    :param uid:
    :param cookie:
    :param suname:
    :return:
    """
    url = f"https://api.bilibili.com/x/space/acc/info?mid={uid}&jsonp=jsonp"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
        "Cookie": cookie
    }
    response = await request.req_add_job('get', url, headers=headers, suname=suname)
    response = json.loads(response)
    printer.printer(f"获取{uid}用户信息(封禁)API回显:{response}", "DEBUG", "yellow")
    return response


# 主站信息获取 接口 1
async def userinfo_2(cookie, suname):
    """
    :param cookie:
    :param suname:
    :return:
    """
    url = "https://account.bilibili.com/home/userInfo"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
        "Cookie": cookie
    }
    response = await request.req_add_job('get', url, headers=headers, suname=suname)
    response = json.loads(response)
    printer.printer(f"获取用户信息(主站信息)API回显:{response}", "DEBUG", "yellow")
    return response


async def userinfo_3(cookie, suname):
    """
    :param cookie:
    :param suname:
    :return:
    """
    url = "https://api.bilibili.com/x/web-interface/nav"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
        "Cookie": cookie
    }
    response = await request.req_add_job('get', url, headers=headers, suname=suname)
    response = json.loads(response)
    printer.printer(f"获取用户信息(主站信息2)API回显:{response}", "DEBUG", "yellow")
    return response


# 直播站信息获取 接口 1
async def userinfo_4(cookie, suname):
    """
    :param cookie:
    :param suname:
    :return:
    """
    url = "https://api.live.bilibili.com/xlive/web-ucenter/user/get_user_info"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
        "Cookie": cookie
    }
    response = await request.req_add_job('get', url, headers=headers, suname=suname)
    response = json.loads(response)
    printer.printer(f"获取用户信息(直播站信息)API回显:{response}", "DEBUG", "yellow")
    return response


# 获取一言以伪造签名
async def get_sentence():
    types = ["a", "b", "c", "d", "e", "f", "g"]
    c = random.choice(types)
    url = f"https://v1.hitokoto.cn?c={c}&encode=json&charset=utf-8"
    response = await request.other_get(url)
    response = json.loads(response)
    hitokoto = response['hitokoto']
    while len(hitokoto) >= 70:
        response = await request.other_get(url)
        response = json.loads(response)
        hitokoto = response['hitokoto']
    return hitokoto


# 获取头像图片
async def get_image(suname):
    url = "https://acg.toubiec.cn/random.php?return=json"
    response = await request.other_get(url)
    response = json.loads(response)
    img_url = response['acgurl']
    printer.printer("成功获取到图片url", "DEBUG", "yellow")
    response = await request.req_add_job('get', img_url, suname=suname)
    f = BytesIO()
    f.write(response)
    img = Image.open(f)
    img.thumbnail((180, 180))
    f11 = BytesIO()
    img.save(f11, format="jpeg")
    return f11


# 上传头像，我猜有bug
async def upload_image(cookie, suname):
    f11 = await get_image(suname)
    # data = {"dopost": "save", "DisplayRank": "10000"}
    # files = {'face': ('blob', f11.getvalue(), "image/jpeg")}
    url = "http://account.bilibili.com/pendant/updateFace"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        "Cookie": cookie
    }
    data = request.form_data
    data.add_field('face', f11.getvalue(), content_type='image/jpeg')
    data.add_field('dopost', 'save')
    data.add_field('DisplayRank', '10000')
    response = await request.req_add_job('post', url, data=data, headers=headers, suname=suname)
    response = json.loads(response)
    return response


# 根据av号和收藏夹id添加到收藏夹
async def add_something_to_favorite_pack(aid, media_id, cookie, csrf, suname):
    url = "https://api.bilibili.com/medialist/gateway/coll/resource/deal"
    data = {
        "rid": aid,
        "type": 2,
        "add_media_ids": media_id,
        "del_media_ids": "",
        "jsonp": "jsonp",
        "csrf": csrf
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
        "Referer": f"https://www.bilibili.com/video/av{aid}",
        "Cookie": cookie
    }
    response = await request.req_add_job('post', url, headers=headers, data=data, suname=suname)
    response = json.loads(response)
    printer.printer(f"收藏视频{aid}回显:{response}", "INFO", "blue")


# 随机获取一些up主uid
async def get_follow_uid_list(suname):
    page = random.randint(1, 25)
    url = f"https://api.live.bilibili.com/room/v1/room/get_user_recommend?page={page}"
    response = await request.req_add_job('get', url, suname=suname)
    response = json.loads(response)
    return response


# 获取50个番剧id
async def get_bangumi_list(suname):
    url = "https://api.bilibili.com/pgc/season/index/result?season_version=-1&area=-1&is_finish=-1&copyright=-1&season_status=-1&season_month=-1&year=-1&style_id=-1&order=3&st=1&sort=0&page=1&season_type=1&pagesize=50&type=1"
    response = await request.req_add_job('get', url, suname=suname)
    response = json.loads(response)
    return response


# 追番
async def add_bangumi_to_follow(season_id, cookie, csrf, suname):
    url = "https://api.bilibili.com/pgc/web/follow/add"
    data = {
        "season_id": season_id,
        "csrf": csrf
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
        "Cookie": cookie,
        "Referer": f"https://www.bilibili.com/bangumi/play/ss{season_id}/"
    }
    response = await request.req_add_job('post', url, headers=headers, data=data, suname=suname)
    response = json.loads(response)
    printer.printer(f"添加追番{season_id}回显:{response}", "INFO", "blue")


# 取消追番
async def del_bangumi_in_follow(season_id, cookie, csrf, suname):
    url = "https://api.bilibili.com/pgc/web/follow/del"
    data = {
        "season_id": season_id,
        "csrf": csrf
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
        "Cookie": cookie,
        "Referer": f"https://www.bilibili.com/bangumi/play/ss{season_id}/"
    }
    response = await request.req_add_job('post', url, headers=headers, data=data, suname=suname)
    response = json.loads(response)
    printer.printer(f"取消追番{season_id}回显:{response}", "INFO", "blue")


# 订阅标签
async def add_tag(tag_id, cookie, csrf, suname):
    url = "https://api.bilibili.com/x/tag/subscribe/add"
    data = {
        "tag_id": tag_id,
        "csrf": csrf
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
        "Cookie": cookie
    }
    response = await request.req_add_job('post', url, headers=headers, data=data, suname=suname)
    response = json.loads(response)
    printer.printer(f"订阅标签{tag_id}回显:{response}", "INFO", "blue")


# 设置各种不可见
async def set_private(action, uid, cookie, csrf, suname):
    """
    fav_video
    bangumi
    tags
    coins_video
    user_info
    played_game
    :return:
    """
    url = "http://space.bilibili.com/ajax/settings/setPrivacy"
    data = {
        action: 0,
        "csrf": csrf
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
        "Cookie": cookie,
        'Origin': "https://space.bilibili.com",
        'Referer': f"https://space.bilibili.com/{uid}/",
    }
    response = await request.req_add_job('post', url, headers=headers, data=data, suname=suname)
    response = json.loads(response)
    printer.printer(f"设置隐私{action}回显:{response}", "INFO", "blue")


# 佩戴勋章
async def wear_medal(medal, cookie, suname):
    url = f"https://api.live.bilibili.com/i/ajaxWearFansMedal?medal_id={medal}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
        "Cookie": cookie
    }
    response = await request.req_add_job('get', url, headers=headers, suname=suname)
    response = json.loads(response)
    printer.printer(f"佩戴勋章{medal}回显:{response}", "INFO", "blue")


# 更新签名，出生年月，性别信息
async def update_info(uname, cookie, csrf, suname):
    url = "https://api.bilibili.com/x/member/web/update"
    data = {
        "uname": uname,
        "usersign": await get_sentence(),
        "sex": random.choice(['男', '女', '保密']),
        "birthday": random.choice(['1970-01-01', '2000-09-10', '2002-03-12']),
        "csrf": csrf
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
        "Cookie": cookie
    }
    response = await request.req_add_job('post', url, headers=headers, data=data, suname=suname)
    response = json.loads(response)
    printer.printer(f"更新用户基本信息回显:{response}", "INFO", "blue")


# 直播间发送弹幕
async def send_danmu(msg, roomid, cookie, csrf, suname):
    url = "https://api.live.bilibili.com/msg/send"
    data = {
        "color": 16777215,
        "fontsize": 25,
        "mode": 1,
        "msg": msg,
        "rnd": 0,
        "roomid": roomid,
        "bubble": 0,
        "csrf_token": csrf,
        "csrf": csrf
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
        "Cookie": cookie
    }
    response = await request.req_add_job('post', url, headers=headers, data=data, suname=suname)
    response = json.loads(response)
    printer.printer(f"发送弹幕{msg}回显:{response}", "INFO", "blue")


# 硬币换勋章
async def coin_to_medal(buy_uid, cookie, suname):
    url = f"https://api.vc.bilibili.com/link_group/v1/member/buy_medal?coin_type=metal&master_uid={buy_uid}&platform=android"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
        "Cookie": cookie
    }
    response = await request.req_add_job('get', url, headers=headers, suname=suname)
    response = json.loads(response)
    printer.printer(f"硬币购买勋章回显:{response}", "INFO", "blue")
    return response


# 银瓜子换硬币
async def sliver_to_coin(cookie, csrf, suname):
    url = "https://api.live.bilibili.com/pay/v1/Exchange/silver2coin"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
        "Cookie": cookie
    }
    data = {
        "platform": "pc",
        "csrf_token": csrf
    }
    response = await request.req_add_job('post', url, data=data, headers=headers, suname=suname)
    response = json.loads(response)
    printer.printer(f"银瓜子兑换硬币回显:{response}", "INFO", "blue")
    return response


# 查询直播站实物礼物列表
async def query_live_reward(access_key, suname):
    url = f"https://api.live.bilibili.com/lottery/v1/Award/award_list?access_key={access_key}"
    headers = {
        "User-Agent": "Mozilla/5.0 BiliDroid/5.31.3 (bbcallen@gmail.com)"
    }
    response = await request.req_add_job('get', url, headers=headers, suname=suname)
    response = json.loads(response)
    printer.printer(f"{suname}查询直播站实物礼物回显:{response['data']['list']}", "INFO", "blue")
    return response


# 参与实物抽奖
async def draw_lottery(aid, number, cookie, suname):
    url = f"https://api.live.bilibili.com/lottery/v1/box/draw?aid={aid}&number={number}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
        "Cookie": cookie
    }
    response = await request.req_add_job('get', url, headers=headers, suname=suname)
    response = json.loads(response)
    printer.printer(f"{suname}实物抽奖编号{aid}第{number}轮次回显:{response}", "INFO", "blue")
    return response


# 查询最新一条系统通知
async def query_system_notice(cookie, suname):
    url = "https://message.bilibili.com/api/notify/query.sysnotify.list.do?data_type=1"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
        "Cookie": cookie
    }
    response = await request.req_add_job('get', url, headers=headers, suname=suname)
    response = json.loads(response)
    printer.printer(f"{suname}最新一条系统通知回显:{response['data'][0]['content']}", "INFO", "blue")
    return response


# 给评论点赞
async def comment_like(oid, otype, rpid, cookie, csrf, suname):
    url = "https://api.bilibili.com/x/v2/reply/action"
    data = {
        'oid': oid,
        'type': otype,
        'rpid': rpid,
        'action': 1,
        'jsonp': "jsonp",
        'csrf': csrf,
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
        "Cookie": cookie
    }
    response = await request.req_add_job('post', url, data=data, headers=headers, suname=suname)
    response = json.loads(response)
    printer.printer(f"评论点赞回显:{response}", "INFO", "blue")
    return response


# 给评论点踩
async def comment_hate(oid, otype, rpid, cookie, csrf, suname):
    url = "https://api.bilibili.com/x/v2/reply/hate"
    data = {
        'oid': oid,
        'type': otype,
        'rpid': rpid,
        'action': 1,
        'jsonp': "jsonp",
        'csrf': csrf,
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
        "Cookie": cookie
    }
    response = await request.req_add_job('post', url, data=data, headers=headers, suname=suname)
    response = json.loads(response)
    printer.printer(f"评论点踩回显:{response}", "INFO", "blue")
    return response
