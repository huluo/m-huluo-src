#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import etc

def logInited( logfile ):
    import logging
    import logging.handlers
    # 生成一个日志对象
    logger = logging.getLogger()
    # 生成一个Handler。
    # FileHandler, SocketHandler, SMTPHandler等
    hangdler = logging.handlers.TimedRotatingFileHandler(filename=logfile, when = "D")
    # 格式器用于规范日志的输出格式。
    # 如果没有这行代码，缺省格式就是："%(message)s" 信息是什么日志中就是什么
    # 这里有三项：时间，信息级别，日志信息
    formatter = logging.Formatter('%(asctime)s.%(msecs)-3d <%(module)s.%(funcName)s:%(lineno)d> [%(levelname)s] %(message)s', '%H:%M:%S')
    # 将格式器设置到处理器上
    hangdler.setFormatter(formatter)
    # 将处理器加到日志对象上
    logger.addHandler(hangdler)
    # 设置日志信息输出的级别。
    # NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL
    # 缺省为30(WARNING)。可以执行：logging.getLevelName(logger.getEffectiveLevel())来查看缺省的日志级别。
    # 写入日志时，小于指定级别的信息将被忽略。
    logger.setLevel(logging.DEBUG)
    print('log starting at : '+logfile);
    return logger


filename = os.path.basename( os.path.realpath(sys.argv[0]) ).split('.')[0]+'.log'
logfile = etc.path_log+'/'+os.path.basename(filename)
logger=logInited(logfile)
d=logger.debug
i=logger.info
w=logger.warn
e=logger.error
c=logger.critical
exp=logger.exception

# 使用示例:
#import log
#log.d('test')
#log.i('test')
#log.w('test')
#log.e('test')
#log.exp(e)

