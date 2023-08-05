#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : mi.
# @File         : __init__.py
# @Time         : 2021/1/7 7:34 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


from meutils.pipe import *
from meutils.zk_utils import get_zk_config


def feishu_send(body={"title": "x", "text": "xx"}, hook_url=get_zk_config('/mipush/bot')['ann']):
    return requests.post(hook_url, json=body).json()
