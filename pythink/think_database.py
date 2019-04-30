# -*- coding: utf-8 -*-

# @Date    : 2019-04-04
# @Author  : Peng Shiyu

from __future__ import unicode_literals, print_function

import time
from sqlalchemy import create_engine, text

from pythink.logger import logger
from pythink.think_table import ThinkTable


class ThinkDatabase(object):
    def __init__(self, db_url, **kwargs):
        """
        初始化ThinkModel
        :param db_url: str
            eg:
                mysql://root:123456@127.0.0.1:3306/demo
        """
        self._db_url = db_url
        self._kwargs = kwargs
        self._engine = None
        self._is_open = False
        self._database = None

    def __enter__(self):
        return self

    def __exit__(self, exc, val, traceback):
        self.close()

    def __repr__(self):
        return '<{} connect={}>'.format(self.__class__.__name__, self._is_open)

    def connect(self):
        self._engine = create_engine(self._db_url, **self._kwargs)
        self._database = self._engine.connect()
        self._is_open = True
        logger.info("ThinkDatabase Connect")

    def close(self):
        self._database.close()
        self._is_open = False
        logger.info("ThinkDatabase Close")

    def execute_sql(self, sql, *multiparams):
        """
        执行SQL 可以重写此方法 返回cursor 对象 即可
        :param sql: str
        :return: cursor对象
        """
        if not self._is_open:
            self.connect()

        # 执行SQL
        cursor = self._database.execute(text(sql), *multiparams)

        return cursor

    def table(self, table_name):
        return ThinkTable(self, table_name)


def main():
    db_url = "mysql://root:123456@127.0.0.1:3306/demo"

    think_db = ThinkDatabase(db_url, echo=True)

    think_db.connect()
    think_db.connect()


    student_table = think_db.table("student")
    age_table = think_db.table("table_age")

    rows = student_table.select(["name"]).query()
    print(rows.all(as_dict=True))

    # ret = student_table.insert({"name": "Tom", "age": 23}).execute()
    while True:
        rows = age_table.select(["user_id", "age"]).query()
        print(rows)
        for row in rows:
            print(row)
            print(row.user_id)
            print(row.age)

        time.sleep(5)


    data = [
        {"name": "Tom", "age": 23},
        {"name": "Jack", "age": 24},
    ]

    ret = student_table.insert(data).execute()
    print(ret)


    ret = student_table.update({"name": "Tom", "age": 60}).where("name='Tom'").execute()
    print(ret)

    ret = student_table.delete().where("name='Jack'").execute()
    print(ret)

    row = student_table.select_count().query_first()
    print(row)


if __name__ == '__main__':
    main()
