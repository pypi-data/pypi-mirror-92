#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : fds_cmd
# @Time         : 2021/1/20 10:15 上午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *

HADOOP_HOME = '/home/work/inf/infra-client/bin/'
HDFS_CLUSTER_NAME = 'zjyprc-hadoop'
HDFS_CMD = HADOOP_HOME + 'hadoop --cluster ' + HDFS_CLUSTER_NAME + ' fs '
CLOUDML_CMD = '/home/work/anaconda2/bin/cloudml'




os.popen("ls")