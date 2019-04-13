# pythink

灵感来自于ThinkPHP

根据现有业务 实现了简单的增删改查

依赖于peewee

# 安装
```
pip install pythink
```

# 快速开始

## ThinkDatabase 的基本使用
```python
# -*- coding: utf-8 -*-

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


```

## ThinkModel 的基本使用
```python
# -*- coding: utf-8 -*-

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

```