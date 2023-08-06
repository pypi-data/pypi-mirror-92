#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import httpx
import random


def get_proxy():
    url = f'http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=b5dc17284d1a4979b399e9ac4f1f3441&orderno=YZ201810158701TpKrSK&returnType=1&count=1'
    try:
        resp = httpx.get(url)
        while ':' not in resp.text:
            time.sleep(random.randint(1, 3))
            resp = httpx.get(url)
        else:
            print(f'获取到代理IP:' + resp.text)
            return resp.text
    except Exception as e:
        print(e)
