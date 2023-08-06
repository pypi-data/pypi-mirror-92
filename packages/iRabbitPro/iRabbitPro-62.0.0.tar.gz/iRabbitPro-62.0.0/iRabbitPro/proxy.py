#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import httpx
import random


def get_proxy():
    url = f'http://api.hailiangip.com:8422/api/getIp?type=1&num=1&pid=-1&unbindTime=60&cid=-1&orderId=O20100301555849667354&time=1606747841&sign=eb7b8d7663a2932ca10330f6736d4ab9&noDuplicate=1&dataType=1&lineSeparator=0&singleIp=0'
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
