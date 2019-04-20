# -*- coding: utf-8 -*-

# @Date    : 2019-04-11
# @Author  : Peng Shiyu

from __future__ import unicode_literals, print_function

import hashlib
from datetime import datetime
from pythink.logger import logger
from pythink.think_table import ThinkTable


class ThinkModel(object):
    """
    基类
    """
    # 必须设置的参数
    table_name = None
    database = None

    # 可选的参数
    datetime_format = "%Y-%m-%d %H:%M:%S"

    # 自动添加创建时间
    create_time = False
    create_time_format = datetime_format

    # 自动添加更新时间
    update_time = False
    update_time_format = datetime_format

    # list 去重MD5 的联合字段列表
    md5_list = []

    @classmethod
    def get_table(cls):
        return ThinkTable(cls.database, cls.table_name)

    @classmethod
    def set_insert_create_time(cls, data):
        if cls.create_time:
            return cls._date_time(cls.create_time_format)
        else:
            return None

    @classmethod
    def set_insert_md5(cls, data):
        if cls.md5_list:
            return cls._md5(data, cls.md5_list)
        else:
            return None

    @classmethod
    def set_update_update_time(cls, data):
        if cls.update_time:
            return cls._date_time(cls.update_time_format)
        else:
            return None

    @classmethod
    def insert(cls, data, ignore=False, replace=False):
        """
        :param data:
        :param ignore: bool
        :param replace: bool
        :return:
        """
        table = cls.get_table()

        data = cls._process_method(data, "set_insert_")

        result = table.insert(data, ignore, replace).execute()

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
    def update(cls, uid, data):
        """
        :param uid:
        :param data:
        :return:
        """
        table = cls.get_table()

        data = cls._process_method(data, "set_update_")

        result = table.update(
            data
        ).where(
            "id={}".format(uid)
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
            "id={}".format(uid)
        ).execute()

        logger.debug(" {} delete result: {}".format(
            cls.__name__, result)
        )

        return result

    @classmethod
    def _date_time(cls, datetime_format=datetime_format):
        return datetime.now().strftime(datetime_format)

    @classmethod
    def _md5(cls, data, md5_list):
        md5 = hashlib.md5()

        for md5_field in md5_list:
            value = data[md5_field]

            md5.update("{}".format(value).encode("utf-8"))

        return md5.hexdigest()

    @classmethod
    def _get_methods(cls):
        return filter(cls._is_public_method, dir(cls))

    @classmethod
    def _is_public_method(cls, method_name):
        if all([
            not method_name.startswith("_"),
            not method_name.startswith("__"),
            callable(getattr(cls, method_name))
        ]):
            return True
        else:
            return False

    @classmethod
    def _process_method(cls, data, process_method_key):
        """
        数据预处理所做的动作
        :param data: dict
        :param process_method_key: str
        :return: dict
        """

        for method_name in cls._get_methods():
            if method_name.startswith(process_method_key):
                method = getattr(cls, method_name)
                field_name = method_name.split(process_method_key)[-1]

                result = method(data)
                if result is not None:
                    data[field_name] = result

        return data
