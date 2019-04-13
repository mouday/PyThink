# -*- coding: utf-8 -*-

# @Date    : 2019-04-14
# @Author  : Peng Shiyu

from pythink import ThinkModel
from playhouse.db_url import connect

db = connect("mysql://root:123456@127.0.01:3306/demo")


class StudentThinkModel(ThinkModel):
    table_name = "student"
    database = db


# 增加
data = {
    "name": "Tom",
    "age": 23
}

result = StudentThinkModel.insert(data)
print(result)
# 1

# 删除
result = StudentThinkModel.delete(13)
print(result)
# 1

# 修改
data = {
    "name": "Tom",
    "age": 24
}
result = StudentThinkModel.update(1, data)
print(result)
# 1

# 查询
result = StudentThinkModel.select(
    fields=["name", "age"],
    where="id=1",
    limit=1,
    as_list=True,
    as_dict=True
)
print(result)
# [OrderedDict([('name', u'Tom'), ('age', 24L)])]
