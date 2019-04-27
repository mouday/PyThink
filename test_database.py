# -*- coding: utf-8 -*-

# @Date    : 2019-04-14
# @Author  : Peng Shiyu

from pythink import ThinkTable
from playhouse.db_url import connect

import unittest


class ThinkTableTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        db_url = "mysql://root:123456@127.0.0.1:3306/demo"
        table_name = "student"
        cls.db = connect(db_url)
        cls.student = ThinkTable(cls.db, table_name)

    @classmethod
    def tearDownClass(cls):
        cls.db.close()
        print("类测试结束")

    def test_insert_many(self):
        data = [
            {
                "name": "Tom",
                "age": 24,
            },
            {
                "name": "Tom",
                "age": 25,
            }
        ]

        result = self.student.insert(data).execute()
        self.assertEqual(result, 2)

    def test_select_count(self):
        row = self.student.select_count(["name"]).group_by("name").query_first()
        print(row.count)
        print(row.name)

    def test_update(self):
        data = {
            "name": "tom",
            "age": 30
        }
        row = self.student.update(data).where("id=12").execute()
        self.assertEqual(row, 0)

    def test_insert_one(self):
        # 增加
        data = {
            "name": "Tom",
            "age": 23
        }
        result = self.student.insert(data).execute()
        self.assertEqual(result, 1)

    def test_delete(self):
        # 删除
        result = self.student.delete().where("name='Tom'").execute()
        print(result)
        # 1

    def test_select(self):
        # 查询
        result = self.student.select(
            ["name", "age"]
        ).where("name='Tom'").limit(1).query(as_list=True)

        print(result)
        # [Row(name=u'Tom', age=24L)]


if __name__ == '__main__':
    unittest.main()
