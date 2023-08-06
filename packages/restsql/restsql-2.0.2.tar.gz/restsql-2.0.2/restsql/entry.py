#!/usr/bin/env python
# -*- coding:utf-8 -*-
import logging
import re

import pandas as pd

from restsql.config.database import Database
from restsql.config.value import *
from restsql.exception import RunningException, UserConfigException

logging.basicConfig()
logger = logging.getLogger("main")
logger.setLevel("DEBUG")


class RestSQL:
    """
    RestSQL服务提供类。
    """

    JOIN_TYPE_MAP = {
        'left_join': 'left',
        'inner_join': 'inner',
        'full_join': 'outer'
    }

    def __init__(self):
        pass

    @staticmethod
    def query(query_dict):
        """
        查询入口。传入指定格式的字典，返回查询结果的dataframe。
        1. 预处理query_dict: 将子select全部拆出。
        2. 从主select开始，到所有子select完成，执行查询并获得一个个dataframe。
        3. 删除子dataframe中非export的字段与不在on的字段
        4. 将子dataframe join进主dataframe。
        5. 根据fields删除多余字段，并执行计算
        :return: dataframe存储的结果
        """
        # Query
        main_df = RestSQL._single_query(query_dict.get('select'))
        if isinstance(main_df, pd.DataFrame):
            if query_dict.get('join'):
                for join in query_dict.get('join'):  # 子select全部拆除单独query
                    df = RestSQL._single_query(join.get('query').get('select'))
                    # 删除子dataframe中非export与on的字段
                    fields = {}  # 旧列名 -> 目标列名
                    if isinstance(df, pd.DataFrame):
                        cur_fields = list(df)  # 当前列名列表
                        for export in join.get('export'):
                            real, alias = export.split('@', 1)
                            fields[real] = alias
                        for k, v in join.get('on').items():
                            fields[v] = v
                        for field in cur_fields:
                            if field not in fields:  # 当前列多余
                                df.drop(field, axis=1, inplace=True)
                            else:  # 当前列存在，需重命名
                                df.rename({field: fields[field]}, axis=1, inplace=True)
                    # Join
                    main_df = main_df.merge(df, left_on=list(join.get('on').keys()),
                                            right_on=list(join.get('on').values()),
                                            how=RestSQL.JOIN_TYPE_MAP[join.get('type')])
        # Sort
        if len(query_dict.get('sort', [])) != 0:
            ascending_sort = []
            for idx, val in enumerate(query_dict.get('sort')):  # 将'-'号设为倒序，无前缀设为正序
                if val.startswith('-'):
                    query_dict['sort'] = val[1:]
                    ascending_sort.append(False)
                else:
                    ascending_sort.append(True)
            main_df.sort_values(by=query_dict.get('sort'), ascending=ascending_sort, inplace=True)
        # Limit
        main_df.drop(labels=range(query_dict.get('limit', 10000), main_df.shape[0]), axis=0, inplace=True)
        # Alias and calculate
        exclude_list = []
        fields = {}
        for field in query_dict.get('fields'):
            real, alias = field.split('@', 1)
            fields[real] = alias
        columns_list = list(main_df)
        for column in columns_list:
            if column in fields.keys():  # 重命名 or exclude
                if fields[column] == 'exclude':  # 添加到exclude列表，最后统一删除。
                    exclude_list.append(column)
                elif fields[column] != column:
                    main_df.rename({column: fields[column]}, axis=1, inplace=True)
            else:  # 删除多余字段
                main_df.drop(column, axis=1, inplace=True)
        for field in fields:
            if ('+' in field) or ('-' in field) or ('*' in field) or ('/' in field):  # 表达式
                try:
                    main_df.eval('{}={}'.format(fields[field], field), inplace=True)
                except Exception as e:
                    logging.exception(e)
                    raise RunningException(1, '计算 %s 时出错', field)
        for column in exclude_list:  # 删除exclude部分
            main_df.drop(column, axis=1, inplace=True)
        return main_df

    @staticmethod
    def _single_query(select_dict):
        select_from = select_dict.get('from')
        if '.' in select_from:
            database_name, table_name = select_from.split('.', 1)
        else:
            raise UserConfigException(102, '查询中无法拆分from字段: 需要[数据源.数据表]的形式')
        table = index4table.get(select_from, None)
        database = index4database.get(database_name, None)
        if table is None:
            raise RunningException(9, '待查询表格不存在于索引中')
        if database is None:
            raise RunningException(10, '待查询表格所在数据源不存在于索引中')
        select_dict['from'] = table.table_name
        if isinstance(database, Database):
            stmt, params, fields = database.engine.parse(select_dict)
            logger.debug('Engine get the result:\nstmt = %s\nparams = %s\nfields = %s', stmt, params, fields)
            fields = database.list2map(database_name, table_name, fields)
            df = database.query(stmt, params, fields)  # 真正查询
            return df
        else:
            pass

    @staticmethod
    def _extract_var(expression):
        """
        将计算表达式中的变量提取出来
        :param expression:  (a+b)*(c-d)
        :return: [a,b,c,d]
        """
        return re.findall('[^\+,\-,\*,\/,(,)]+', expression)
