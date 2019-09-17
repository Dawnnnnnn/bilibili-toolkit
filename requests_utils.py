#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/9/17 23:06
# @Author  : Dawnnnnnn
# @Contact: 1050596704@qq.com
import traceback
import aiohttp
import asyncio
import time
from printer import Printer
from uuid import uuid4

printer = Printer()


# 生成获取令牌
def generate_verify_token():
    return str(uuid4()).replace('-', '')


class Request:
    def __init__(self):
        self.proxy_api = "8.8.8.8"
        # 全局session
        self.ssion = {}
        # 工作队列
        self.req_work_list = []
        self.req_done_dict = {}
        self.req_alive_num = 20
        self.req_timeout_max = 60

    # 请求中心
    async def _requests(self, verify_token, method, url, proxy=False,
                        suname='',
                        **kwargs):
        flag = 10
        while True:
            try:
                if flag < 0 or proxy:
                    temp = await self.other_get(self.proxy_api)
                    proxy = f'http://{temp}'
                else:
                    proxy = None
                async with getattr(self.ssion[suname], method)(
                        url, proxy=proxy, verify_ssl=False, timeout=20,
                        **kwargs) as r:

                    # text()函数相当于requests中的r.text，r.read()相当于requests中的r.content
                    data = await r.read()
                    await r.release()
                    self.req_done_dict[verify_token] = data
                    return None

            except Exception as e:
                traceback.print_exc()
                printer.printer(f"{url}{e}", "Error", "red")
                flag -= 1
                continue

    # 其他GET请求
    async def other_get(self, url, headers=None, proxy=False):
        flag = 10
        while True:
            try:
                if flag < 0 or proxy:
                    temp = await self.other_get(self.proxy_api)
                    proxy = f'http://{temp}'
                else:
                    proxy = None

                async with aiohttp.ClientSession() as session:
                    async with session.get(url, headers=headers,
                                           timeout=10, proxy=proxy,
                                           verify_ssl=False) as r:
                        # text()函数相当于requests中的r.text，r.read()相当于requests中的r.content
                        data = await r.text()
                        await r.release()
                        return data

            except Exception as e:
                printer.printer(f"{url}{e}", "Error", "red")
                flag -= 1
                continue

    # 加入请求任务
    async def req_add_job(self, *args, **kwargs):
        try:
            verify_token = generate_verify_token()
            # 将任务放入队列，等待阻塞读取，参数是被执行的函数和函数的参数
            req_pack = {
                'func': self._requests,
                'token': verify_token,
                'args': args,
                'kwargs': kwargs
            }
            self.req_work_list.append(req_pack)
            return await self.req_result(verify_token)
        except Exception as e:
            printer.printer(f"req_add_job {e}", "Error", "red")

    # 获取请求结果
    async def req_result(self, verify_token):
        while True:
            # 理论数据 后期根据实际情况微调
            await asyncio.sleep(0.1)
            try:
                if verify_token not in self.req_done_dict.keys():
                    continue
                temp_data = self.req_done_dict[verify_token]
                del self.req_done_dict[verify_token]
                return temp_data
            except Exception as e:
                printer.printer(f"req_result {e}", "Error", "red")

    # 维护请求队列
    async def req_loop(self):
        is_alive_time = int(time.time())
        while True:
            try:
                # 理论数据 不排除其他协程调度的消耗 可能会堵塞
                await asyncio.sleep(1 / self.req_alive_num)
                # 退出当前协程
                if int(time.time()) - is_alive_time > self.req_timeout_max:
                    printer.printer("最大超时时间内没有请求处理,请求协程退出!", "Finished", "green")
                    return
                if self.req_work_list:
                    is_alive_time = int(time.time())
                    req_pack = self.req_work_list.pop(0)
                    target = req_pack['func']
                    verify_token = req_pack['token']
                    args = req_pack['args']
                    kwargs = req_pack['kwargs']
                    await target(verify_token, *args, **kwargs)

            except Exception as e:
                printer.printer(f"req_loop {e}", "Error", "red")
