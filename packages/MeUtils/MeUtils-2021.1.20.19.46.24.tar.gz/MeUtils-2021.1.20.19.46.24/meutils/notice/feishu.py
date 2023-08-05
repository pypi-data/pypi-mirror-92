#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : feishu
# @Time         : 2021/1/20 6:04 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


from meutils.pipe import *
from meutils.zk_utils import get_zk_config


def send_feishu(body, hook_url=get_zk_config('/mipush/bot')['ann']):
    """

    :param body: {"title": "x", "text": "xx"}
    :param hook_url:
    :return:
    """
    return requests.post(hook_url, json=body).json()
