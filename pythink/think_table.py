# -*- coding: utf-8 -*-

# @Date    : 2019-04-04
# @Author  : Peng Shiyu

from __future__ import unicode_literals, print_function

import time

from pythink.exceptions import ThinkException
from pythink.logger import logger
from pythink.records import Records


class ThinkTable(object):
    """
    一个便于使用的Model 助手，使用方式和sql语句一样
    """
    # 1、update 必须有 where
    # 2、delete 必须有 where

    def __init__(self, database, table_name):
        self._database = database
        self._table_name = table_name
        self._params = None
        self._sql = None
        self._truncate = None
        self._is_count = False
        self._is_insert = False

    def _clear(self):
        """
        初始化所有值，避免多条语句中的参数冲突
        """
        self._params = None
        self._sql = None
        self._truncate = None
        self._is_count = False
        self._is_insert = False

    def _insert(self, keys, ignore=False, replace=False):
        """
        插入数据
        :param keys: list 关键字列表
        :param ignore: bool
        :param replace: bool
        :return: self
        """
        # 不允许两个值同时设定
        if all([ignore, replace]):
            raise ThinkException("not allow set ignore and replace equal True at the same time")

        keys_str = ", ".join(keys)
        value_symbols = ", ".join(":{}".format(key) for key in keys)
        values_str = "({})".format(value_symbols)

        # 启用ignore
        if ignore:
            insert_method = "INSERT IGNORE"  # 返回值 0

        elif replace:
            insert_method = "REPLACE"        # 返回值 2

        else:
            insert_method = "INSERT"

        insert_sql = "{insert_method} INTO {table_name}({keys}) VALUES {values} ".format(
            insert_method=insert_method,
            table_name=self._table_name,
            keys=keys_str,
            values=values_str
        )

        self._sql = [insert_sql]
        self._is_insert = True

        return self

    def insert_one(self, data, ignore=False, replace=False):
        """
        插入一条数据
        :param data: dict
        :param ignore: bool
        :param replace: bool
        :return: self
        """
        self._params = data
        return self._insert(data.keys(), ignore, replace)

    def insert_many(self, data, truncate=None, ignore=False, replace=False):
        """
        插入多条数据
        :param truncate: int
        :param data: list
        :param ignore: bool
        :param replace: bool
        :return: self
        """
        self._params = data
        self._truncate = truncate

        try:
            dct = data[0]
        except IndexError:
            raise ThinkException("data not list!")

        base_keys = dct.keys()
        # 对列表中的key 进行校验
        for d in data:
            if set(base_keys) != set(d.keys()):
                raise ThinkException("list data keys different")

        return self._insert(base_keys, ignore, replace)

    def insert(self, data, truncate=None, ignore=False, replace=False):
        """
        向数据库插入一条 或 多条数据
        :param truncate: int
        :param data: dict/list
        :param ignore: bool
        :param replace: bool
        :return: self
        """

        # 构造字典数据
        if isinstance(data, dict):
            if truncate:
                raise ThinkException("data is dict, not allow truncate")

            return self.insert_one(data, ignore, replace)

        # 构造列表数据
        elif isinstance(data, list):
            return self.insert_many(data, truncate, ignore, replace)

        else:
            raise ThinkException("data must list(dict) or dict")

    def update(self, data):
        """
        更新数据库数据
        :return: self
        """
        set_str = ", ".join("{0}=:{0}".format(key) for key in data.keys())

        update_sql = "UPDATE {table_name} SET {set_str}".format(
            table_name=self._table_name, set_str=set_str
        )
        self._sql = [update_sql]
        self._params = data
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
        count_fields = ["COUNT(*) AS {}".format(count_as)]

        if field_list:
            count_fields.extend(field_list)

        field_str = ", ".join(count_fields)
        return self._select(field_str)

    def select(self, field_list):
        """
        从数据库中选择数据
        :param field_list: list 字段名称列表
        :return:self
        """
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

        if not sql:
            raise ThinkException("SQL can not None")

        # 安全校验
        if "UPDATE" in sql and "WHERE" not in sql:
            raise ThinkException("ThinkDatabase if update must have where")

        if "DELETE" in sql and "WHERE" not in sql:
            raise ThinkException("ThinkDatabase if delete must have where")

        return sql

    def _truncate_insert(self, sql):
        """
        分段插入
        :param sql: str
        :return:
        """
        start = 0
        end = self._truncate
        data = self._params[start: end]

        rowcount = 0

        while data:
            cursor = self._database.execute_sql(sql, data)
            rowcount += cursor.rowcount

            start += self._truncate
            end += self._truncate
            data = self._params[start: end]

        return rowcount

    def execute(self):
        """
        insert update delete 需要调用此方法才会被执行
        :return: int 影响行数
        """
        sql = self.sql_builder()

        if self._params:
            if all([self._is_insert, self._truncate]):
                rowcount = self._truncate_insert(sql)

            else:
                cursor = self._database.execute_sql(sql, self._params)
                rowcount = cursor.rowcount
        else:
            cursor = self._database.execute_sql(sql)
            rowcount = cursor.rowcount

        self._clear()
        return rowcount

    def query(self):
        """
        select 需要调用此方法才会有查询结果
        :return: generator(Row)/ generator(dict)
        """
        sql = self.sql_builder()

        start = time.time()

        cursor = self._database.execute_sql(sql)
        self._clear()

        result = cursor.fetchall()

        end = time.time()
        logger.debug("query time: {:.3f}s".format(end - start))

        return Records(cursor.keys(), result, cursor.rowcount)

    def query_first(self, as_dict=False):
        """
        返回 一条数据
        :param as_dict: 转为字典输出 默认 False
        :return: Row
        """
        if not self._is_count:
            self.limit(1)

        return self.query().first(as_dict)

    def __getattr__(self, item):
        return self._append_sql(item.upper())._append_sql
