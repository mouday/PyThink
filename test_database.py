# -*- coding: utf-8 -*-

# @Date    : 2019-04-14
# @Author  : Peng Shiyu

from pythink import ThinkDatabase
from playhouse.db_url import connect

db = connect("mysql://root:123456@127.0.01:3306/demo")
think_db = ThinkDatabase(db)
student = think_db.table("student")

# 增加
data = {
    "name": "Tom",
    "age": 23
}
result = student.insert(**data).execute()
print(result)
# 1

# 删除
result = student.delete().where("id", "=", 15).execute()
print(result)
# 1

# 修改
data = {
    "name": "Tom",
    "age": 24
}
result = student.update(**data).where("id", "=", 14).execute()
print(result)

# 查询
result = student.select(["name", "age"]).where("id", "=", 14).limit(1).query(as_list=True)
print(result)
# [Row(name=u'Tom', age=24L)]

db.close()
