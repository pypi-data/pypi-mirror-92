#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2021 Odin <odinmanlee@gmail.com>
#
# Distributed under terms of the MIT license.

"""
log
"""

import logging  # 引入logging模块


class ColoredLevel(logging.Filter):
    """
    Log filter to enable `%(levelname)s` colord
    """

    def filter(self, record):
        """set level color"""
        if record.levelno == logging.DEBUG:
            record.levelname = "\x1b[30;42m" + record.levelname + "\x1b[0m"
        elif record.levelno == logging.INFO:
            record.levelname = "\x1b[30;44m" + record.levelname + "\x1b[0m"
        elif record.levelno == logging.WARNING:
            record.levelname = "\x1b[30;43m" + record.levelname + "\x1b[0m"
        elif record.levelno == logging.ERROR:
            record.levelname = "\x1b[30;41m" + record.levelname + "\x1b[0m"
        elif record.levelno == logging.CRITICAL:
            record.levelname = "\x1b[30;45m" + record.levelname + "\x1b[0m"
        else:
            record.levelname = "\x1b[30;47m" + record.levelname + "\x1b[0m"
        return True


Logger = logging.getLogger()
Logger.setLevel(logging.INFO)  # Log等级总开关
# ch = StreamHandlerColor()
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)  # 输出到console的log等级的开关
formatter = logging.Formatter(
    "%(asctime)s[%(levelname)s] %(message)s [%(filename)s:%(lineno)d]"
)
ch.setFormatter(formatter)
Logger.addFilter(ColoredLevel())
Logger.addHandler(ch)

if __name__ == "__main__":
    Logger.debug("debug message")
    Logger.info("info message")
    Logger.warning("warning message")
    Logger.error("error message")
    Logger.critical("critical message")
