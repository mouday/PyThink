# -*- coding: utf-8 -*-

# @Date    : 2019-04-14
# @Author  : Peng Shiyu

from pythink import ThinkModel, ThinkDatabase

db_url = "mysql://root:123456@127.0.01:3306/demo"
db = ThinkDatabase(db_url, echo=True)


class StudentThinkModel(ThinkModel):
    table_name = "student"
    database = db


#############################
# 一、插入操作
#############################
# 1、增加单条记录
def test_insert_one():
    data = {
        "name": "Tom",
    }
    result = StudentThinkModel.insert(data)
    print(result)  #


# test_insert_one()


# 2、增加多条记录
def test_insert_many():
    data = [
        {
            "name": "Tom",
        },
        {
            "name": "Jack"
        }
    ]

    result = StudentThinkModel.insert(data)
    print(result)  # 2


# test_insert_many()


# 3、插入多条 分段插入
def test_multi_insert():
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
    ret = StudentThinkModel.insert(data, truncate=3)
    print(ret)  # 6


# test_multi_insert()


# 4、忽略重复
def test_insert_ignore():
    data = {
        "name": "Tom",
    }
    result = StudentThinkModel.insert_ignore(data)
    print(result)  # 0


# test_insert_ignore()


# 5、替换重复
def test_insert_replace():
    data = {
        "name": "Tom",
        "age": 100
    }
    result = StudentThinkModel.insert_replace(data)
    print(result)  # 2


# test_insert_replace()


#############################
# 二、查询操作
#############################

# 1、查询数量
def test_select_count():
    count = StudentThinkModel.count("name='Tom'")
    # SELECT COUNT(*) AS count FROM student WHERE name='Tom'
    print(count)  # 24


# test_select_count()


# 2、查询记录
def test_select_row():
    rows = StudentThinkModel.select(["name", "age"], where="id>25", limit=5)
    # SELECT name, age FROM student WHERE id>25 LIMIT 5
    for row in rows:
        print(row.name, row.age)


# ('Tom', 25L)
# ('Tom', 26L)
# ('Tom', 27L)
# ('Tom', 28L)
# ('Tom', 29L)

# test_select_row()

# 3、快捷获取
def test_select_by_id():
    row = StudentThinkModel.select_by_id(4, ["name", "age"])
    # SELECT name, age FROM student WHERE id=4 LIMIT 1
    print(row.name, row.age)


# ('Tom', 27L)

# test_select_by_id()

# 4、查询记录
def test_select_all_row():
    rows = StudentThinkModel.select("name, age")
    # SELECT name, age FROM student
    for row in rows:
        print(row.name, row.age)


# test_select_all_row()


#############################
# 三、更新操作
#############################

# 1、条件更新
def test_update():
    data = {
        "name": "tom",
        "age": 30
    }
    ret = StudentThinkModel.update(data, "id=25")
    print(ret)  # 1


# test_update()

# 2、快捷更新
def test_update_by_id():
    data = {
        "name": "tom",
        "age": 30
    }
    ret = StudentThinkModel.update_by_id(2, data)
    print(ret)  # 1


# test_update_by_id()


#############################
# 四、删除操作
#############################

# 1、条件删除
def test_delete():
    result = StudentThinkModel.delete("id=13")
    print(result)  # 1


# test_delete()

# 2、快速删除
def test_delete_by_id():
    result = StudentThinkModel.delete_by_id(1)
    print(result)  # 1

# test_delete_by_id()
