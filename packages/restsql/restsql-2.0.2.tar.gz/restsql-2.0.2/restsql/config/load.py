# -*- coding:utf-8 -*-
import logging
from enum import Enum, unique

from restsql.config.database import *
from restsql.config.table import Table
from restsql.config.value import *

__all__ = ['DatabaseType', 'register_database', 'register_table']

logger = logging.getLogger('config')


@unique
class DatabaseType(Enum):
    MYSQL = 'MYSQL'
    POSTGRESQL = 'POSTGRESQL'
    IMPALA = 'IMPALA'
    ELASTICSEARCH = 'ELASTICSEARCH'


def register_database(name, db_type, host,
                      port=None,
                      user=None,
                      password=None,
                      db_name=None,
                      ):
    if name in index4database:
        logger.warning('发现同名数据源%s，将忽略非首次出现的数据源配置', name)
        return
    database = None
    if DatabaseType.MYSQL.value == db_type:
        database = MySQLDatabase(host, port, user, password, db_name)
    elif DatabaseType.POSTGRESQL.value == db_type:
        database = PgDatabase(host, port, user, password, db_name)
    elif DatabaseType.ELASTICSEARCH.value == db_type:
        database = EsDatabase(host)
    elif DatabaseType.IMPALA.value == db_type:
        database = ImpalaDatabase(host, port, db_name)
    else:
        logger.warning('发现未知数据源类型%s，将忽略本次数据源载入', db_type)
    databases.append(database)
    index4database[name] = database


def register_table(name, table_name, fields, belong_to):
    index_name = '{}.{}'.format(belong_to, name)
    if index_name in index4table:
        logger.warning('发现同名表%s，将忽略非首次出现的表配置', index_name)
        return
    table = Table(name, table_name, fields)
    tables.append(table)
    index4table[index_name] = table
    # 存储相应表与数据源中
    database = index4database[belong_to]
    if isinstance(database, Database):
        database.tables.append(table)
