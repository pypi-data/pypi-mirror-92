# -*- coding:utf-8 -*-

__all__ = ['databases', 'index4database', 'tables', 'index4table']

#
# 将数据池提出，防止循环import问题出现
#

# 数据源
databases = []  # Database
# 数据源索引
index4database = {}  # name -> database (string -> Database)

# 数据表
tables = []  # Table
# 数据表索引
index4table = {}  # database_name.table_name -> table (string -> Table)
