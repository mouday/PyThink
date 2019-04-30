# -*- coding: utf-8 -*-

# @Date    : 2019-04-14
# @Author  : Peng Shiyu

from pythink import ThinkDatabase

# 连接数据库
db_url = "mysql://root:123456@127.0.0.1:3306/demo"
think_db = ThinkDatabase(db_url)
student = think_db.table("student")

# 执行原生sql
cursor = think_db.execute_sql("show tables")
rows = cursor.fetchall()
print(rows)
# [('student',), ('student2',), ('table_age',)]


#############################
# 一、插入操作
#############################

# 1、插入一条数据
def test_insert_one():
    data = {
        "name": "Tom",
        "age": 24,
    }

    result = student.insert(data).execute()
    print(result)  # 1


# test_insert_one()


# 2、插入多条
def test_insert_many():
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

    result = student.insert(data).execute()
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
    ret = student.insert(data, truncate=3).execute()
    print(ret)  # 6


#############################
# 二、查询操作
#############################

# 1、查询数量
def test_select_count():
    row = student.select_count(["name"]).group_by("name").query_first()
    print(row.name, row.count)  # ('Tom', 9L)


# test_select_count()


# 2、查询记录
def test_select_row():
    rows = student.select(["name", "age"]).limit(4).query()
    for row in rows:
        print(row.name, row.age)


# ('Tom', 24L)
# ('Tom', 25L)
# ('Tom', 26L)
# ('Tom', 27L)

# test_select_row()


#############################
# 三、更新操作
#############################

# 1、条件更新
def test_update():
    data = {
        "name": "tom",
        "age": 30
    }
    ret = student.update(data).where("id=25").execute()
    print(ret)  # 1


# test_update()

# 2、全部更新，如果不指定where会抛出异常，避免删库跑路
def test_update_all():
    data = {
        "name": "tom",
        "age": 30
    }
    student.update(data).execute()


# pythink.exceptions.ThinkException: ThinkDatabase if update must have where

# test_update_all()


#############################
# 四、删除操作
#############################

# 1、条件删除
def test_delete():
    # 删除
    result = student.delete().where("id=33").execute()
    print(result)
    # 1


# test_delete()

# 2、条件删除  如果不指定where会抛出异常，避免删库跑路
def test_delete_all():
    student.delete().execute()


# pythink.exceptions.ThinkException: ThinkDatabase if delete must have where


# test_delete_all()
