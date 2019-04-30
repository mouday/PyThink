# -*- coding: utf-8 -*-

# @Date    : 2019-04-30
# @Author  : Peng Shiyu

import logging

from pythink import ThinkModel, ThinkDatabase

# 自定义是否显示日志
logger = logging.getLogger("pythink")
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

db_url = "mysql://root:123456@127.0.01:3306/demo"
db = ThinkDatabase(db_url)


class StudentThinkModel(ThinkModel):
    table_name = "student"
    database = db

    create_time = "%Y-%m-%d %H:%M:%S"  # 开启自动插入时间

    @classmethod
    def set_insert_name(cls, data):
        """自定义扩展以 set_insert_ 开头 插入数据之前 把名字转为大写"""
        return data["name"].upper()


data = {
    "name": "Tom",
    "age": 23,
}

ret = StudentThinkModel.insert(data)
print(ret)  # 1
# 插入结果：
# name: TOM
# age: 23
# create_time: 2019-04-30 17:38:03
