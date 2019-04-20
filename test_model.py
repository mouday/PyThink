# -*- coding: utf-8 -*-

# @Date    : 2019-04-14
# @Author  : Peng Shiyu

from pythink import ThinkModel
from playhouse.db_url import connect

db = connect("mysql://root:123456@127.0.01:3306/demo")


class StudentThinkModel(ThinkModel):
    table_name = "student"
    database = db

    create_time = True  # 开启自动插入时间

    @classmethod
    def set_insert_name(cls, data):
        """把名字转为大写"""
        return data["name"].upper()


# 增加
data = {
    "name": "Tom",
    "age": 23
}

result = StudentThinkModel.insert(data)
print(result)
# INSERT INTO student(age, create_time, name) VALUES (%s, %s, %s)
# [23, '2019-04-20 20:18:40', 'TOM']
# 1

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

