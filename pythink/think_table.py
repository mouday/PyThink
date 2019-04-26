# -*- coding: utf-8 -*-

# @Date    : 2019-04-04
# @Author  : Peng Shiyu

from __future__ import unicode_literals, print_function

import json

from .logger import logger
from .exceptions import ThinkException
import time
from collections import namedtuple


class ThinkTable(object):
    """
    一个便于使用的Model 助手，使用方式和sql语句一样
    """
    # 1、update 必须有 where
    # 2、delete 必须有 where

    replace_symbol = "%s"

    def __init__(self, database, table_name):
        self._database = database
        self._table_name = table_name
        self._fields = None
        self._params = None
        self._sql = None
        self._is_count = False

    def _clear(self):
        """
        初始化所有值，避免多条语句中的参数冲突
        """
        self._fields = None
        self._params = None
        self._sql = None
        self._is_count = False

    def _insert(self, keys_str, values_str, ignore=False, replace=False):
        """
        插入数据
        :param keys_str: str 关键字字符串
        :param values_str: str 数值字符串
        :param ignore: bool
        :param replace: bool
        :return: self
        """
        # 启用ignore
        if ignore:
            insert_method = "INSERT IGNORE"

        elif replace:
            insert_method = "REPLACE"

        else:
            insert_method = "INSERT"

        insert_sql = "{insert_method} INTO {table_name}({keys}) VALUES {values} ".format(
            insert_method=insert_method,
            table_name=self._table_name,
            keys=keys_str,
            values=values_str
        )
        self._sql = [insert_sql]
        return self

    def insert_one(self, data, ignore=False, replace=False):
        """
        插入一条数据
        :param data: dict
        :param ignore: bool
        :param replace: bool
        :return: self
        """
        keys = ", ".join(data.keys())
        value_symbols = ", ".join([self.replace_symbol] * len(data.keys()))
        values = "({})".format(value_symbols)
        self._params = data.values()
        return self._insert(keys, values, ignore, replace)

    def insert_many(self, data, ignore=False, replace=False):
        """
        插入多条数据
        :param data: list
        :param ignore: bool
        :param replace: bool
        :return: self
        """
        dct = data[0]
        base_keys = dct.keys()

        # 对列表中的key 进行校验
        for d in data:
            if set(base_keys) != set(d.keys()):
                raise ThinkException("list data keys different")

        keys = ", ".join(base_keys)
        value_symbols = ", ".join([self.replace_symbol] * len(base_keys))
        values = ", ".join("({})".format(value_symbols) for _ in range(len(data)))

        self._params = []
        for dct in data:
            self._params.extend(dct.values())

        return self._insert(keys, values, ignore, replace)

    def insert(self, data, ignore=False, replace=False):
        """
        向数据库插入一条 或 多条数据
        :param data: dict/list
        :param ignore: bool
        :param replace: bool
        :return: self
        """
        # 构造字典数据
        if isinstance(data, dict):
            return self.insert_one(data, ignore, replace)

        # 构造列表数据
        elif isinstance(data, list):
            return self.insert_many(data, ignore, replace)

        else:
            raise ThinkException("data must list(dict) or dict")

    def update(self, data):
        """
        更新数据库数据
        :return: self
        """
        set_str = ", ".join("{}={}".format(key, self.replace_symbol) for key in data.keys())

        update_sql = "UPDATE {table_name} SET {set_str}".format(
            table_name=self._table_name, set_str=set_str
        )
        self._sql = [update_sql]
        self._params = data.values()
        return self

    def delete(self):
        """
        删除数据库中的数据
        :return: self
        """
        delete_sql = "DELETE FROM {table_name}".format(
            table_name=self._table_name
        )
        self._sql = [delete_sql]
        return self

    def _select(self, field_str):

        if field_str == "*":
            raise ThinkException("ThinkDatabase fields can not select *")

        select_sql = "SELECT {fields} FROM {table_name}".format(
            fields=field_str, table_name=self._table_name
        )
        self._sql = [select_sql]
        return self

    def select_count(self, field_list=None, count_as="count"):
        # 处理语句 select count(*) as count,
        self._is_count = True
        self._fields = [count_as]
        count_fields = ["COUNT(*) AS {}".format(count_as)]

        if field_list:
            self._fields.extend(field_list)
            count_fields.extend(field_list)

        field_str = ", ".join(count_fields)
        return self._select(field_str)

    def select(self, field_list):
        """
        从数据库中选择数据
        :param field_list: list 字段名称列表
        :return:self
        """
        self._fields = field_list
        field_str = ", ".join(field_list)
        return self._select(field_str)

    def _append_sql(self, *args):
        for arg in args:
            self._sql.append("{}".format(arg))
        return self

    def where(self, condition):
        return self._append_sql("WHERE", condition)

    def between(self, condition):
        return self._append_sql("BETWEEN", condition)

    def and_(self, condition):
        return self._append_sql("AND", condition)

    def or_(self, condition):
        return self._append_sql("OR", condition)

    def in_(self, condition):
        return self._append_sql("IN", condition)

    def on(self, condition):
        return self._append_sql("ON", condition)

    def join(self, table_name):
        return self._append_sql("JOIN", table_name)

    def limit(self, limit):
        return self._append_sql("LIMIT", limit)

    def offset(self, offset):
        return self._append_sql("OFFSET", offset)

    def paginate(self, page, size):
        if page > 0:
            page -= 1

        return self.limit(size).offset(page * size)

    def order_by(self, order_by):
        return self._append_sql("ORDER BY", order_by)

    def desc(self):
        return self._append_sql("DESC")

    def group_by(self, group):
        return self._append_sql("GROUP BY", group)

    def having(self, condition):
        return self._append_sql("HAVING", condition)

    def comment(self, comment):
        return self._append_sql("#", comment)

    def sql_builder(self):
        """
        sql条件
        1、不可以select *
        2、不可以不写where条件, 如果需要删除、更新所有, 则 1=1
        3、不可以不写limit
        :return: str
        """
        sql = " ".join(self._sql)

        logger.debug("SQL: {}".format(sql))

        # 安全校验
        if "UPDATE" in sql and "WHERE" not in sql:
            raise ThinkException("ThinkDatabase if update must have where")

        if "DELETE" in sql and "WHERE" not in sql:
            raise ThinkException("ThinkDatabase if delete must have where")

        return sql

    def execute(self):
        """
        insert update delete 需要调用此方法才会被执行
        :return: int 影响行数
        """
        sql = self.sql_builder()
        cursor = self._execute_sql(sql, self._params)
        return cursor.rowcount

    def _execute_sql(self, sql, params=None):
        """
        执行SQL 可以重写此方法 返回cursor 对象 即可
        :param sql: str
        :return: cursor对象
        """
        try:
            params_str = json.dumps(params, ensure_ascii=False)
        except Exception as e:
            logger.debug(e)
            params_str = params

        logger.debug("SQL Params: {}".format(params_str))

        # peewee 执行SQL
        cursor = self._database.execute_sql(sql, params)
        self._clear()

        return cursor

    def query(self, as_list=False, as_dict=False):
        """
        select 需要调用此方法才会有查询结果
        :param as_list: 结果转为列表 默认 False为迭代器
        :param as_dict: 元素转为字典 默认 False为Row对象
        :return: generator(Row)/ generator(dict)
        """
        sql = self.sql_builder()

        if not sql:
            raise ThinkException("SQL can not None")

        Row = namedtuple("Row", self._fields)

        start = time.time()

        cursor = self._execute_sql(sql)

        result = cursor.fetchall()

        end = time.time()
        logger.debug("query time: {:.3f}s".format(end - start))

        if as_dict:
            rows = (Row(*ret)._asdict() for ret in result)
        else:
            rows = (Row(*ret) for ret in result)

        return list(rows) if as_list else rows

    def query_first(self, as_dict=False):
        """
        返回 一条数据
        :param as_dict: 转为字典输出 默认 False
        :return: Row
        """
        if not self._is_count:
            self.limit(1)

        try:
            row = self.query(as_list=True, as_dict=as_dict)[0]
        except IndexError:
            row = None
        return row

    def __getattr__(self, item):
        return self._append_sql(item.upper())._append_sql
