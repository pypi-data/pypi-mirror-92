# -*- coding:utf-8 -*-
import abc

import MySQLdb
import impala.dbapi as impyla
import pandas as pd
import psycopg2
from elasticsearch import Elasticsearch

from restsql.config.table import FType
from restsql.config.value import *
from restsql.engine import SqlEngine, EsEngine
from restsql.exception import ProgramConfigException, RunningException

__all__ = ['Database', 'PgDatabase', 'MySQLDatabase', 'ImpalaDatabase', 'EsDatabase']


class Database(metaclass=abc.ABCMeta):
    """
    数据源抽象类。存储与数据库连接相关信息。
    提供查询数据入口。
    """

    def __init__(self):
        self.tables = []
        self.conn = None
        self.engine = None

    def list2map(self, database_name, table_name, fields):
        """
        判断查询字段是否存在表中，并将字段列表转为map(field_name -> field_type)
        self.tables为属于本数据源的数据表。
        :param database_name: 目标数据源的name
        :param table_name: 目标数据表的name
        :param fields: 待检测字段
        :return: 若传入fields为list则返回转换后的map；否则返回待查表所有fields
        """
        index_name = '{}.{}'.format(database_name, table_name)
        if index_name not in index4table:  # 系统中不存在该表
            raise RunningException(4, '系统中不存在待查询的表')
        table = index4table[index_name]
        if table not in self.tables:  # 数据源中不存在该表
            raise RunningException(5, '目标数据源中不存在待查询的表')
        if isinstance(fields, list):
            field_map = {}
            for field in fields:
                if '__' in field:
                    field_temp = field.split('__', 1)[0]
                    if field_temp not in table.fields:  # 字段不存在
                        raise RunningException(6, '待查询表中不存在待查询字段')
                    field_map[field] = table.fields[field_temp]
                else:
                    if field not in table.fields:  # 字段不存在
                        raise RunningException(6, '待查询表中不存在待查询字段')
                    field_map[field] = table.fields[field]
            return field_map
        else:
            return table.fields

    @abc.abstractmethod
    def query(self, stmt, params, fields):
        """
        执行查询，并返回只包含fields的dataframe结构。
        self.conn为数据库连接，根据不同的库提供的api调用对应方法完成需求。
        应为静态方法，即每个数据源类型的查询方式都交由程序员实现。
        :param stmt: 查询语句。
        :param params: 查询参数。
        :param fields: 查询字段。
        """
        pass


class _SqlDatabase(Database):
    """
    Sql相关类的公共父类，抽取相同的sql逻辑于此。
    """

    def query(self, stmt, params, fields):
        if isinstance(fields, dict):
            # query
            cur = self.conn.cursor()
            cur.execute(stmt, params)
            # fetch
            result = list(cur.fetchall())
            cur.close()
            # parse
            fnames = list(fields.keys())
            df = pd.DataFrame.from_records(result, columns=fnames)
            # type
            for fname in fnames:
                if fields[fname] == FType.INT or fields[fname] == FType.NUMBER:
                    df[[fname]] = df[[fname]].apply(pd.to_numeric)
                elif fields[fname] == FType.DATETIME:
                    df[[fname]] = df[[fname]].apply(pd.to_datetime)
                elif fields[fname] == FType.TIMEDELTA:
                    df[[fname]] = df[[fname]].apply(pd.to_timedelta)
            return df
        else:
            raise ProgramConfigException(301, '无法识别的fields类型: {}', type(fields))


class PgDatabase(_SqlDatabase):

    def __init__(self, host, port, user, password, db_name):
        super().__init__()
        self.engine = SqlEngine()
        self.conn = psycopg2.connect(
            database=db_name,
            user=user,
            password=password,
            host=host,
            port=int(port),
        )


class MySQLDatabase(_SqlDatabase):

    def __init__(self, host, port, user, password, db_name):
        super().__init__()
        self.engine = SqlEngine('`')
        self.conn = MySQLdb.connect(
            db=db_name,
            user=user,
            passwd=password,
            host=host,
            port=int(port)
        )


class ImpalaDatabase(_SqlDatabase):

    def __init__(self, host, port, db_name):
        super().__init__()
        self.conn = impyla.connect(
            host=host,
            port=port,
            database=db_name,
        )
        self.engine = SqlEngine()


class EsDatabase(Database):

    def __init__(self, host):
        super().__init__()
        self.conn = Elasticsearch(host)
        self.engine = EsEngine()

    def query(self, stmt, params, fields):
        """
        执行查询并返回结果dataframe。结果dataframe中可能包含无关字段。 TODO: 实现这部分
        :param stmt: 查询语句
        :param params: 查询index
        :param fields: 字段->类型的dict
        """
        raw_result = self.conn.search(index=params, body=stmt)
        df = None
        if 'aggs' in raw_result or 'aggregations' in raw_result:  # dsl中有aggs.groupby.aggs
            if raw_result.get('aggregations'):
                if not raw_result.get('aggregations').get('groupby').get('buckets'):
                    return pd.DataFrame(columns=[])
                df = pd.DataFrame(raw_result['aggregations']['groupby']['buckets'])
            else:
                if not raw_result.get('aggregations').get('groupby').get('buckets'):
                    return pd.DataFrame(columns=[])
                df = pd.DataFrame(raw_result['aggs']['groupby']['buckets'])
            df.drop('doc_count', axis=1, inplace=True)
            # Dealing with others but key
            columns = list(df)
            for column in columns:
                if column != 'key':
                    df[column] = df[column].map(lambda x: x['value'])
            # Dealing with key
            example_val = df['key'].iat[0]
            col_count = len(example_val.split(';'))
            for i in range(col_count):
                col_name = example_val.split(';')[i].split(':', 1)[0]
                df[col_name] = df['key'].map(lambda x: x.split(';')[i].split(':', 1)[1])
            df.drop('key', axis=1, inplace=True)
        elif 'hits' in raw_result and 'hits' in raw_result['hits']:
            df = pd.concat(map(pd.DataFrame.from_dict, raw_result['hits']['hits']), axis=1)['_source'].T
            df.reset_index(drop=True, inplace=True)  # 重置索引
        else:
            raise RunningException(1, 'es查询失败: 未在结果中看到aggs、hits数据部分。请查看日志')
        # 字段类型转换
        columns = list(df)
        for column in columns:
            column_without_suffix = column
            if '__' in column:
                column_without_suffix = column.split('__', 1)[0]
            if column_without_suffix in fields:  # 该字段存在 -> 将该字段的字段格式转为基本格式类型
                if fields[column_without_suffix] == FType.INT or fields[column_without_suffix] == FType.NUMBER:
                    df[[column]] = df[[column]].apply(pd.to_numeric)
                elif fields[column_without_suffix] == FType.DATETIME:
                    df[[column]] = df[[column]].apply(pd.to_datetime)
                elif fields[column_without_suffix] == FType.TIMEDELTA:
                    df[[column]] = df[[column]].apply(pd.to_timedelta)
            else:
                raise RunningException(8, 'ES查询结果中未知字段: {}', column)
        return df
