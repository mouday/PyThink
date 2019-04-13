# -*- coding: utf-8 -*-

# @Date    : 2019-04-11
# @Author  : Peng Shiyu

from __future__ import unicode_literals, print_function

import hashlib
from datetime import datetime

from .logger import logger
from .think_database import ThinkDatabase


class ThinkModel(object):
    """
    基类
    """
    # 必须设置的参数
    table_name = None
    database = None

    # 可选的参数
    datetime_format = "%Y-%m-%d %H:%M:%S"
    think_database = ThinkDatabase

    @classmethod
    def get_table(cls):
        think_db = cls.think_database(cls.database)
        table = think_db.table(cls.table_name)
        return table

    @classmethod
    def insert(cls, data, create_time_=False, md5_list_=None):
        """
        :param data:
        :param create_time_: bool 自动添加创建时间
        :param md5_list_: list 去重MD5 的联合字段列表
        :return:
        """
        table = cls.get_table()

        if create_time_:
            data.setdefault("create_time", cls._date_time())

        if md5_list_:
            data.setdefault("md5", cls._md5(data, md5_list_))

        result = table.insert(
            **data
        ).execute()

        logger.debug(" {} insert result: {}".format(
            cls.__name__, result)
        )
        return result

    @classmethod
    def select(cls, fields, where, limit, as_list=False, as_dict=False):
        table = cls.get_table()

        rows = table.select(
            fields
        ).where(
            where
        ).limit(
            limit
        ).query(as_list, as_dict)
        return rows

    @classmethod
    def update(cls, uid, data, update_time_=False):
        """
        :param uid:
        :param data:
        :param update_time_: bool 自动添加更新时间
        :return:
        """
        table = cls.get_table()

        if update_time_:
            data.setdefault("update_time", cls._date_time())

        result = table.update(
            **data
        ).where(
            "id", "=", uid
        ).execute()

        logger.debug(" {} update result: {}".format(
            cls.__name__, result)
        )
        return result

    @classmethod
    def delete(cls, uid):
        table = cls.get_table()

        result = table.delete(
        ).where(
            "id", "=", uid
        ).execute()

        logger.debug(" {} delete result: {}".format(
            cls.__name__, result)
        )
        return result

    @classmethod
    def _date_time(cls):
        return datetime.now().strftime(cls.datetime_format)

    @classmethod
    def _md5(cls, data, md5_list):
        md5 = hashlib.md5()

        for md5_field in md5_list:
            value = data[md5_field]

            md5.update("{}".format(value).encode("utf-8"))

        return md5.hexdigest()
