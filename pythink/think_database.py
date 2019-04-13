# -*- coding: utf-8 -*-

# @Date    : 2019-04-04
# @Author  : Peng Shiyu

from __future__ import unicode_literals, print_function

from .logger import logger
from .exceptions import ThinkException
import time
from collections import namedtuple


class ThinkDatabase(object):
    """
    一个便于使用的Model 助手，使用方式和sql语句一样
    """
    # 字符串的引号，可以继承后重写为 '"'
    quotation_mark = "'"

    # 默认开启 safe_operation:
    # 1、select 必须有 limit
    # 2、update 必须有 where
    # 3、delete 必须有 where
    safe_operation = True

    def __init__(self, database):
        """
        初始化ThinkModel
        :param database:
            peeweee.Database 对象 或者
            pymysql.cursor 对象

            可以是任何实现了3个操作的对象
            cursor.execute_sql / cursor.execute
            cursor.rowcount
            cursor.fetchall()
        """
        self._database = database
        self._table_name = None
        self._fields = None
        self._sql = []

    def table(self, table_name):
        self._table_name = table_name
        return self

    def insert(self, **kwargs):
        """
        向数据库插入一条数据
        :return: self
        """
        keys = ", ".join(kwargs.keys())
        values = ", ".join("{0}{1}{0}".format(
            self.quotation_mark, value
        ) for value in kwargs.values())

        insert_sql = "INSERT INTO {table_name}({keys}) VALUES({values})".format(
            table_name=self._table_name, keys=keys, values=values
        )
        self._sql = [insert_sql]
        return self

    def update(self, **kwargs):
        """
        更新数据库数据
        :return: self
        """
        set_list = []
        for key, value in kwargs.iteritems():
            set_list.append("{1}={0}{2}{0}".format(
                self.quotation_mark, key, value
            ))

        set_str = ", ".join(set_list)

        update_sql = "UPDATE {table_name} SET {set_str}".format(
            table_name=self._table_name, set_str=set_str
        )
        self._sql = [update_sql]
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

    def select(self, field_list):
        """
        从数据库中选择数据
        :param field_list: list 字段名称列表
        :return:self
        """
        self._fields = field_list
        field_str = ", ".join(field_list)

        if field_str == "*":
            raise ThinkException("ThinkDatabase fields can not select *")

        select_sql = "SELECT {fields} FROM {table_name}".format(
            fields=field_str, table_name=self._table_name
        )
        self._sql = [select_sql]
        return self

    def _append_sql(self, *args):
        for arg in args:
            self._sql.append("{}".format(arg))
        return self

    def _append_condition(self, *args):
        if len(args) == 1:
            return self._append_sql(*args)
        else:
            key, symbol, value = args
            value = "{0}{1}{0}".format(self.quotation_mark, value)
            return self._append_sql(key, symbol, value)

    def where(self, *args):
        self._append_sql("WHERE")
        return self._append_condition(*args)

    def between(self, *args):
        self._append_sql("BETWEEN")
        return self._append_condition(*args)

    def and_(self, *args):
        self._append_sql("AND")
        return self._append_condition(*args)

    def or_(self, *args):
        self._append_sql("OR")
        return self._append_condition(*args)

    def in_(self, condition):
        return self._append_sql("IN", condition)

    def on(self, *args):
        self._append_sql("ON")
        return self._append_condition(*args)

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

    def order_by(self, order):
        return self._append_sql("ORDER BY", order)

    def desc(self):
        return self._append_sql("DESC")

    def group_by(self, group):
        return self._append_sql("GROUP BY", group)

    def having(self, *args):
        self._append_sql("HAVING")
        return self._append_condition(*args)

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

        logger.debug("\n[ThinkDatabase SQL] {}".format(sql))

        if self.safe_operation:
            if "SELECT" in sql and "LIMIT" not in sql:
                raise ThinkException("ThinkDatabase if select must have limit")

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
        cursor = self._execute_sql(sql)
        return cursor.rowcount

    def _execute_sql(self, sql):
        """
        执行SQL 可以重写此方法 返回cursor 对象 即可
        :param sql: str
        :return: cursor对象
        """
        # peewee 执行SQL
        execute_sql = getattr(self._database, "execute_sql")

        if not execute_sql:
            #  pymysql 执行SQL
            execute_sql = getattr(self._database, "execute")

        cursor = execute_sql(sql)
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
            raise ThinkException("ThinkDatabase Exception: SQL can not None")

        Row = namedtuple("Row", self._fields)

        start = time.time()

        cursor = self._execute_sql(sql)

        result = cursor.fetchall()

        end = time.time()
        logger.debug("\n[ThinkDatabase SQL] query time: {:.3f}s".format(end - start))

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
        self.limit(1)

        try:
            row = self.query(as_list=True, as_dict=as_dict)[0]
        except IndexError:
            row = None
        return row

    def __getattr__(self, item):
        return self._append_sql(item.toupper())._append_sql
