'''
Descripttion: 
version: 1.0.0
Author: jiegemena
Date: 2020-07-11 13:51:37
LastEditors: jiegemena
LastEditTime: 2020-11-05 10:13:13
'''
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(name="jgconfig",
      description="jgconfig",
      version="1.2.11",
      author="jiegemena",
      author_email="jiegemena@outlook.com",
      packages=find_packages(),
      install_requires=[    # 依赖列表
          'requests',
          'pymysql',
          'redis'
      ]
    )
