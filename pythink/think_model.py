# -*- coding: utf-8 -*-

# @Date    : 2019-04-11
# @Author  : Peng Shiyu

from __future__ import unicode_literals, print_function

from .logger import logger
from .think_table import ThinkTable
from .util import Util


class ThinkModel(object):
    """
    ThinkModel 基类
    """
    #############################
    # 必须设置的参数
    #############################

    table_name = None
    database = None

    #############################
    # 可选的参数
    #############################

    # 自动添加创建时间 False or "%Y-%m-%d %H:%M:%S"
    create_time = False

    # 自动添加更新时间 False or "%Y-%m-%d %H:%M:%S"
    update_time = False

    # list 去重MD5 的联合字段列表
    md5_list = []

    @classmethod
    def get_table(cls):
        return ThinkTable(cls.database, cls.table_name)

    @classmethod
    def insert(cls, data, ignore=False, replace=False):
        """
        :param data: dict/list
        :param ignore: bool
        :param replace: bool
        :return:
        """
        table = cls.get_table()

        if isinstance(data, list):
            lst = []
            for d in data:
                d = cls._process_method(d, "set_insert_")
                lst.append(d)

            data = lst

        elif isinstance(data, dict):
            data = cls._process_method(data, "set_insert_")

        result = table.insert(data, ignore, replace).execute()

        logger.debug("{} insert result: {}".format(
            cls.__name__, result)
        )

        return result

    @classmethod
    def select(cls, fields, where="1=1", limit=1, as_list=False, as_dict=False):
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

        logger.debug("{} update result: {}".format(
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

        logger.debug("{} delete result: {}".format(
            cls.__name__, result)
        )

        return result

    @classmethod
    def _process_method(cls, data, process_method_key):
        """
        数据预处理所做的动作
        :param data: dict
        :param process_method_key: str
        :return: dict
        """

        for method_name in Util.get_public_names(cls):
            if method_name.startswith(process_method_key):
                method = Util.get_method(cls, method_name)

                if method is None:
                    continue

                field_name = method_name.split(process_method_key)[-1]

                result = method(data)
                if result is not None:
                    data[field_name] = result

        return data

    @classmethod
    def set_insert_create_time(cls, data):
        if cls.create_time:
            return Util.get_date_time_str(cls.create_time)
        else:
            return None

    @classmethod
    def set_update_update_time(cls, data):
        if cls.update_time:
            return Util.get_date_time_str(cls.update_time)
        else:
            return None

    @classmethod
    def set_insert_md5(cls, data):
        if cls.md5_list:
            return Util.get_md5(data, cls.md5_list)
        else:
            return None
