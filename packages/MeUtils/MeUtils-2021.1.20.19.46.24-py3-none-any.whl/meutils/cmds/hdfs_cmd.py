#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : hdfs_cmd
# @Time         : 2021/1/20 10:15 上午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


from meutils.pipe import *

HADOOP_HOME = os.environ.get('HADOOP_HOME', '~/infra-client/bin')
HDFS_CLUSTER_NAME = os.environ.get('HDFS_CLUSTER_NAME', 'zjyprc-hadoop')

HDFS_CMD = f"{HADOOP_HOME}/hdfs --cluster {HDFS_CLUSTER_NAME} dfs"  # f"{HADOOP_HOME}/hadoop --cluster {HDFS_CLUSTER_NAME} fs"


def hdfs_check_file_isexist(path):
    cmd = f"{HDFS_CMD} -test -e {path}"
    output = os.system(cmd)
    rst = False if output != 0 else True

    logger.info(cmd)
    logger.info(f"CMD Output: {output}")
    logger.info(f'Path Exist: {rst}')

    return rst


def add_hdfs_success_file(input_data_path, date):
    hdfs_success_path = input_data_path + "/date=" + date
    cmd = HDFS_CMD + " -touchz {}/_SUCCESS".format(hdfs_success_path)
    logger.info(cmd)
    os.system(cmd)
    return True


def check_hdfs_dir_exists(data_path):
    cmd = HDFS_CMD + " -test -d {}".format(data_path)
    output = os.system(cmd)

    if output != 0:
        logger.info('%s not exist!' % data_path)
        return 0
    else:
        logger.info('%s exist!' % data_path)
        return 1


def check_hdfs_file_exists(file_path):
    cmd = HDFS_CMD + " -test -e {}".format(file_path)
    output = os.system(cmd)

    if output != 0:
        logger.info('%s not exist!' % file_path)
        return 0
    else:
        logger.info('%s exist!' % file_path)
        return 1


def check_ckpt_training_flag_exists(model_ckpt_path):
    training_flag_path = model_ckpt_path + "/" + Constant.Training
    cmd = HDFS_CMD + " -test -e {}".format(training_flag_path)
    output = os.system(cmd)

    if output != 0:
        logger.info('%s not exist!' % training_flag_path)
        return 0
    else:
        logger.info('%s exist!' % training_flag_path)
        return 1
