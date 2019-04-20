# -*- coding: utf-8 -*-

# @Date    : 2019-04-04
# @Author  : Peng Shiyu

from __future__ import unicode_literals, print_function

from .think_table import ThinkTable


class ThinkDatabase(object):
    def __init__(self, database):
        """
        初始化ThinkModel
        :param database:
            peeweee.Database 对象
        """
        self._database = database

    def table(self, table_name):
        return ThinkTable(self._database, table_name)
