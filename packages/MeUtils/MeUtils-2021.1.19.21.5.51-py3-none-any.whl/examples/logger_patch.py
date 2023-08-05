#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : logger_patch
# @Time         : 2021/1/19 8:53 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


from meutils.common import logger, logger_patch

logger.info("x")

logger = logger_patch(__file__)
logger.info("xx")
