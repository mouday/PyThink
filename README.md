# pythink

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pythink.svg)
![PyPI](https://img.shields.io/pypi/v/pythink.svg)

灵感来自于ThinkPHP
部分代码实现参考了 records

根据现有业务 实现了简单的增删改查， 可以用作日常助手

依赖：
```
SQLAlchemy>=1.2.8
```
> ps：原来基于peewee实现的，不过问题较多，就直接用SQLAlchemy

# 安装
```
pip install pythink
```

# 快速开始

新建表
```sql
CREATE TABLE `student` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uid` int(11) DEFAULT NULL,
  `name` varchar(20) DEFAULT '',
  `age` int(11),
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8
```

代码示例

1、连接数据库，创建Model
```python
# -*- coding: utf-8 -*-

from pythink import ThinkModel, ThinkDatabase

db_url = "mysql://root:123456@127.0.01:3306/demo"
db = ThinkDatabase(db_url)


class StudentThinkModel(ThinkModel):
    table_name = "student"
    database = db

```

2、插入操作
```python

# 1、增加单条记录

data = {
    "name": "Tom"
}

>>> StudentThinkModel.insert(data)
>>> 1


# 2、增加多条记录
data = [
    {
        "name": "Tom",
    },
    {
        "name": "Jack"
    }
]

>>> StudentThinkModel.insert(data)
>>> 2



# 3、插入多条 分段插入
data = [
    {
        "name": "Tom",
        "age": 24,
    },
    {
        "name": "Tom",
        "age": 25,
    },
    {
        "name": "Tom",
        "age": 26,
    },
    {
        "name": "Tom",
        "age": 27,
    },
    {
        "name": "Tom",
        "age": 28,
    },
    {
        "name": "Tom",
        "age": 29,
    }
]

# 每次插入3 条数据
>>> StudentThinkModel.insert(data, truncate=3)
>>> 6
```

3、查询操作
```python

# 1、查询数量
>>> StudentThinkModel.count()
>>> 24



# 2、查询记录
rows = StudentThinkModel.select(["name", "age"], where="id>25", limit=5)
for row in rows:
    print(row.name, row.age)


# ('Tom', 25L)
# ('Tom', 26L)
# ('Tom', 27L)
# ('Tom', 28L)
# ('Tom', 29L)

```

4、更新操作
```python

# 条件更新
data = {
    "name": "tom",
    "age": 30
}

>>> StudentThinkModel.update(data, "id=25")
>>> 1

```

5、删除操作
```python

# 删除
>>> StudentThinkModel.delete("id=13")
>>> 1

```

当然，也可以不写表名，就像（省略部分代码）

```python
class BaseThinkModel(ThinkModel):
    database = db


class StudentThinkModel(BaseThinkModel):
    """
    学生类
    会被自动转为 小写命名方式：student
    """

```


更多关于使用示例：
ThinkDatabase
https://github.com/mouday/PyThink/blob/master/test_database.py

ThinkModel
https://github.com/mouday/PyThink/blob/master/test_modle_extend.py

# 更新记录
* 部分版本可能存在不兼容，属于正常现象，后续版本会趋于稳定

|时间 | 版本 | 主要更新|
|-|-|-|
|2019-04-14 | v0.0.1 | 基于peewee 实现基本的CURD |
|2019-04-20 | v0.0.2 | 增强Model的功能,配置自动完成字段 |
|2019-04-26 | v0.0.3 | 添加多行插入功能 |
|2019-04-27 | v0.0.4 | 将update、delete修改得更通用 |
|2019-04-30 | v0.0.5 | 基于SQLAlchemy重写逻辑，完成多行分次插入 |
|2019-04-30 | v0.0.6 | 修复安装报错的问题 |
|2019-05-10 | v0.0.7 | 添加自动转为类名为表名 |
