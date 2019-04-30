# -*- coding: utf-8 -*-

# @Date    : 2019-04-11
# @Author  : Peng Shiyu

from __future__ import unicode_literals, print_function

from pythink.logger import logger
from pythink.think_table import ThinkTable
from pythink.util import Util


class ThinkModel(object):
    """
    ThinkModel 基类
    """
    #############################
    # 必须设置的参数
    #############################

    # 表名
    table_name = None

    # 数据库对象 peewee.Database
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
    def select(cls, fields, where=None, limit=1):
        """
        查询数据
        :param fields: list 要选择的字段列表
        :param where: str 条件（包括sql 中 where关键字到 limit关键字之间的内容）
        :param limit: int 数量
        :return:
            generator/list
                -object/dict
        """
        table = cls.get_table()
        if where:
            rows = table.select(fields).where(where).limit(limit).query()
        else:
            rows = table.select(fields).limit(limit).query()

        return rows

    @classmethod
    def insert(cls, data, truncate=None, ignore=False, replace=False):
        """
        插入数据
        :param truncate: int 分段插入，每次插入数量
        :param data: dict/list 要插入的数据
        :param ignore: bool 启用 'INSERT IGNORE INTO'
        :param replace: bool 启用 'REPLACE INTO'
        :return: int 插入成功条数
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

        result = table.insert(data, truncate, ignore, replace).execute()

        logger.debug("{} insert result: {}".format(
            cls.__name__, result)
        )

        return result

    @classmethod
    def update(cls, data, where):
        """
        更新数据
        :param data: dict 数据字典
        :param where: str 更新条件
        :return: int 更新成功的条数
        """
        table = cls.get_table()

        data = cls._process_method(data, "set_update_")

        result = table.update(data).where(where).execute()

        logger.debug("{} update result: {}".format(
            cls.__name__, result)
        )
        return result

    @classmethod
    def delete(cls, where):
        """
        删除数据
        :param where: str 删除条件
        :return: int 删除条数
        """
        table = cls.get_table()

        result = table.delete().where(where).execute()

        logger.debug("{} delete result: {}".format(
            cls.__name__, result)
        )

        return result

    @classmethod
    def count(cls, where=None):
        table = cls.get_table()

        if where:
            result = table.select_count().where(where).query_first()
        else:
            result = table.select_count().query_first()

        return result.count

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
        """
        自定义实现的插入时间预处理函数
            使用mysql 自动维护
            `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP

        :param data: dict
        :return: create_time str
        """
        if cls.create_time:
            return Util.get_date_time_str(cls.create_time)
        else:
            return None

    @classmethod
    def set_update_update_time(cls, data):
        """
        自定义实现的更新时间处理函数
            使用mysql 自动维护
            `update_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP

        :param data: dict
        :return: update_time str
        """
        if cls.update_time:
            return Util.get_date_time_str(cls.update_time)
        else:
            return None

    @classmethod
    def set_insert_md5(cls, data):
        """
        自定义实现的插入MD5 计算函数
        :param data: dict
        :return: md5 str
        """
        if cls.md5_list:
            return Util.get_md5(data, cls.md5_list)
        else:
            return None
