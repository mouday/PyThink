# -*- encoding: utf-8 -*-

"""
打包
python setup.py sdist bdist_wheel

上传pypi
twine upload dist/*
"""

import io
import os
from os import path

import requests
import setuptools

version = "0.0.3"

basedir = path.dirname(path.abspath(__file__))

readme_md = path.join(basedir, "README.md")
readme_rst = path.join(basedir, "README.rst")
requirements = path.join(basedir, "requirements.txt")


# 将markdown格式转换为rst格式
def md_to_rst(from_file, to_file):
    r = requests.post(
        url='http://c.docverter.com/convert',
        data={'to': 'rst', 'from': 'markdown'},
        files={'input_files[]': open(from_file, 'rb')}
    )
    if r.ok:
        with open(to_file, "wb") as f:
            f.write(r.content)


if os.path.exists(readme_md):
    md_to_rst(readme_md, readme_rst)

if os.path.exists(readme_rst):
    long_description = io.open(readme_rst, encoding="utf-8").read()
else:
    long_description = 'Add a fallback short description here'

if os.path.exists(requirements):
    install_requires = io.open(requirements).read().split("\n")
else:
    install_requires = []

setuptools.setup(
    name="pythink",
    version=version,
    author="Peng Shiyu",
    author_email="pengshiyuyx@gmail.com",
    description="simple CURD of mysql for python",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/mouday/PyThink",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    install_requires=install_requires,  # 常用
    package_data={
        # If any package contains *.txt or *.rst files, include them:
    }
)
