#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : load_conf_demo
# @Time         : 2021/1/27 8:38 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


from meutils.pipe import *


class Config(BaseConfig):
    name: str
    age: int = 666

Config.parse_zk('/mipush/myconf')
Config.parse_yaml('./myconf.yaml')

