# -*- coding: utf-8 -*-

# @Date    : 2019-04-14
# @Author  : Peng Shiyu

from pythink import ThinkModel
from pythink import connect

import logging

# 自定义是否显示日志
logger = logging.getLogger("pythink")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


db = connect("mysql://root:123456@127.0.01:3306/demo")


class StudentThinkModel(ThinkModel):
    table_name = "student"
    database = db

    create_time = "%Y-%m-%d %H:%M:%S"  # 开启自动插入时间

    @classmethod
    def set_insert_name(cls, data):
        """把名字转为大写"""
        return data["name"].upper()


# 增加单条记录
data = {
    "name": "Tom",
}
result = StudentThinkModel.insert(data)
print(result)
"""
SQL: INSERT INTO student(create_time, name) VALUES (%s, %s) 
SQL Params: ["2019-04-26 15:37:08", "TOM"]
StudentThinkModel insert result: 1
1
"""
# 增加多条记录
data = [
    {
        "name": "Tom",
    },
    {
        "name": "Jack"
    }
]

result = StudentThinkModel.insert(data)
print(result)
"""
SQL: INSERT INTO student(create_time, name) VALUES (%s, %s), (%s, %s) 
SQL Params: ["2019-04-26 15:37:08", "TOM", "2019-04-26 15:37:08", "JACK"]
StudentThinkModel insert result: 2
2
"""


# 删除
result = StudentThinkModel.delete(13)
print(result)
# DELETE FROM student WHERE id=13
# 1


# 修改
data = {
    "name": "Tom",
    "age": 24
}
result = StudentThinkModel.update(1, data)
print(result)
# UPDATE student SET age=%s, name=%s WHERE id=1
# [24, 'Tom']
# 0

# 查询
result = StudentThinkModel.select(
    fields=["name", "age"],
    where="id=1",
    limit=1
)
print(result)
# SELECT name, age FROM student WHERE id=1 LIMIT 1
# <generator object <genexpr> at 0x10f77f140>
