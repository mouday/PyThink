# -*- coding: utf-8 -*-

# @Date    : 2019-04-14
# @Author  : Peng Shiyu

import logging

logger = logging.getLogger("pythink")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.NullHandler())
# logger.addHandler(logging.StreamHandler())
