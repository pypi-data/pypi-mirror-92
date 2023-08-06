# -*- coding: utf-8 -*-

import logging
import time

from just.resultset import ResultSet

logger = logging.getLogger('just-client-logger')

# 最大重试次数
max_retry = 10


def keep_connection(func):
    """
    包装 JustClient 类，用于异常时重新连接
    :param func: 函数
    :return: 被包装的函数
    """

    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception as e:
            # 重新连接
            self.close()
            logger.warning('连接中断，尝试重连: ' + str(e))
            self.connect()
            for i in range(max_retry):
                try:
                    logger.info('重试连接第%s次', i + 1)
                    return func(self, *args, **kwargs)
                except Exception:
                    logger.warning('重试第%s次失败', i + 1)
                    time.sleep(i + 1)
                    continue
            return ResultSet('{"resultCode":500,"resultMsg":"服务异常，重连10次失败","data":null}', '', None, '')

    return wrapper
