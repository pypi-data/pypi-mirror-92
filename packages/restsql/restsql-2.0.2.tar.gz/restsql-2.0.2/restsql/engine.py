#!/usr/bin/env python
# -*- coding:utf-8 -*-
import abc
import copy
import logging

from restsql.exception import JsonFormatException, ProgramConfigException


class Engine(metaclass=abc.ABCMeta):
    """
    转换引擎。将grafana传入的json查询格式转为数据库直接使用的查询语句，如sql、dsl等等。
    """

    @abc.abstractmethod
    def parse(self, select_dict):
        """
        将QueryObject对象转为查询的语句。
        :param select_dict: QueryObject对象
        :return: 返回三参数元组，查询语句、查询参数、字段
        """
        pass


class SqlEngine(Engine):

    def __init__(self, quote='"'):
        """
        初始化一个sql engine实例。传入参数为System identifier，也就是为了兼容mysql'`'
        :param quote: system identifier
        """
        self.quote = quote

    def _parse_agg(self, agg):
        """
        处理aggregation段。
        :param agg: 属于aggregation的字符串。
        :return: sql格式的字符串
        """
        if isinstance(agg, str):
            agg_field, agg_suffix = agg.split('__', 1)
            if agg_suffix == 'avg':
                return 'AVG({}t0{}.{}{}{})'.format(self.quote, self.quote, self.quote, agg_field,
                                                   self.quote)
            elif agg_suffix == 'sum':
                return 'SUM({}t0{}.{}{}{})'.format(self.quote, self.quote, self.quote, agg_field,
                                                   self.quote)
            elif agg_suffix == 'max':
                return 'MAX({}t0{}.{}{}{})'.format(self.quote, self.quote, self.quote, agg_field,
                                                   self.quote)
            elif agg_suffix == 'min':
                return 'MIN({}t0{}.{}{}{})'.format(self.quote, self.quote, self.quote, agg_field,
                                                   self.quote)
            elif agg_suffix == 'count':
                return 'COUNT({}t0{}.{}{}{})'.format(self.quote, self.quote, self.quote, agg_field,
                                                     self.quote)
            elif agg_suffix == 'count_distinct':
                return 'COUNT(DISTINCT {}t0{}.{}{}{})'.format(self.quote, self.quote, self.quote,
                                                              agg_field, self.quote)
            else:
                raise ProgramConfigException(401, '请联系开发者，parse agg后缀错误。无法识别的后缀{}。', agg_suffix)
        else:
            raise ProgramConfigException(401, '请联系开发者，parse agg参数错误。需要字符串，而不是{}。', type(agg))

    def _parse_filter(self, key, value):
        """
        处理filter段。
        注意，本方法返回元组，第二个为sql语句的变量部分。为什么不像其他的一样直接编码进去呢？参考了peewee，为了防止时间字段缺少引号。
        :param key: filter元素的左值
        :param value: filter元素的右
        :return: 两元素元组: (sql字符串, 变量字符串 or None)
        """
        if isinstance(key, str):
            if '__' in key:
                field, suffix = key.split('__', 1)
                if suffix == 'gt':
                    return '{}t0{}.{}{}{} > %s'.format(self.quote, self.quote, self.quote, field,
                                                       self.quote), (value,)
                elif suffix == 'gte':
                    return '{}t0{}.{}{}{} >= %s'.format(self.quote, self.quote, self.quote, field,
                                                        self.quote), (value,)
                elif suffix == 'lt':
                    return '{}t0{}.{}{}{} < %s'.format(self.quote, self.quote, self.quote, field,
                                                       self.quote), (value,)
                elif suffix == 'lte':
                    return '{}t0{}.{}{}{} <= %s'.format(self.quote, self.quote, self.quote, field,
                                                        self.quote), (value,)
                elif suffix == 'contains':
                    return '{}t0{}.{}{}{} LIKE {}%{}%{}'.format(self.quote, self.quote, self.quote,
                                                                field, self.quote, self.quote,
                                                                value,
                                                                self.quote), None
                elif suffix == 'startswith':
                    return '{}t0{}.{}{}{} LIKE {}{}%{}'.format(self.quote, self.quote, self.quote,
                                                               field, self.quote, self.quote, value,
                                                               self.quote), None
                elif suffix == 'endswith':
                    return '{}t0{}.{}{}{} LIKE {}%{}{}'.format(self.quote, self.quote, self.quote,
                                                               field, self.quote, self.quote, value,
                                                               self.quote), None
                elif suffix == 'range':
                    if isinstance(value, list) and len(value) == 2:
                        return '{}t0{}.{}{}{} BETWEEN %s AND %s'.format(self.quote, self.quote, self.quote,
                                                                        field, self.quote), value
                    else:
                        raise JsonFormatException(3, 'range需要传入长度为2的范围列表。如: [1, 2]。')
                elif suffix == 'in':
                    if isinstance(value, list):
                        template = '%s, {}'
                        in_str = ''
                        for i in range(len(value)):
                            in_str = template.format(in_str)
                        in_str = in_str.rsplit(',', 1)[0]
                        return '{}t0{}.{}{}{} IN ({})'.format(self.quote, self.quote, self.quote,
                                                              field, self.quote, in_str), value
                    else:
                        raise JsonFormatException(3, 'in需要传入元素列表，而不是{}。', type(value))
                else:
                    raise ProgramConfigException(401, '请联系开发者，parse filter后缀错误。无法识别的后缀{}。', suffix)
            else:
                return '{}t0{}.{}{}{} == %s'.format(self.quote, self.quote, self.quote, key,
                                                    self.quote), (value,)
        else:
            raise ProgramConfigException(401, '请联系开发者，parse filter参数错误。需要字符串，而不是{}。', type(key))

    def parse(self, select_dict):
        """
        将QueryObject对象转为sql查询语句。
        确保from字段为table_name，而不是database_name.table_name
        :param select_dict: select_dict部分dict
        :return: 返回三元素元组，第一个是查询语句，第二个是参数列表，第三个是查询结果的列名列表
        """
        if isinstance(select_dict, dict):
            #
            # 拆分
            #
            params_list = []  # 最终sql参数
            fields_list = []  # 最终列表列名
            # select字段
            select_part = []
            for field in list(select_dict.get('fields')):  # select.fields
                select_part.append('{}t0{}.{}{}{}'.format(self.quote, self.quote, self.quote, field, self.quote))
            fields_list.extend(select_dict.get('fields'))
            if select_dict.get('aggregation'):
                for agg in select_dict.get('aggregation'):  # select.aggregation
                    select_part.append(self._parse_agg(agg))
                    fields_list.append(agg)
            # where字段
            where_part = []
            if select_dict.get('filter'):
                for (k, v) in select_dict.get('filter').items():  # select.filter
                    where, params = self._parse_filter(k, v)
                    where_part.append(where)
                    if params is not None:
                        params_list.extend(list(params))
            # group by 字段
            group_by_part = []
            if select_dict.get('group_by'):
                for group_by_field in select_dict.get('group_by'):  # main-group-by
                    group_by_part.append('{}t0{}.{}{}{}'.format(self.quote, self.quote, self.quote, group_by_field, self.quote))
            #
            # 拼凑SQL语句
            #
            query = 'SELECT '
            for select in select_part:
                if select == select_part[-1]:
                    query += '{} '.format(select)
                else:
                    query += '{}, '.format(select)
            query += 'FROM {}{}{} AS {}t0{} '.format(self.quote, select_dict.get('from'), self.quote, self.quote,
                                                     self.quote)
            if len(where_part) != 0:
                query += 'WHERE ( ( TRUE ) '
            for where in where_part:
                query += 'AND ( {} ) '.format(where)
            if len(where_part) != 0:
                query += ') '
            if len(group_by_part) != 0:
                query += 'GROUP BY '
            for group_by in group_by_part:
                if group_by == group_by_part[-1]:
                    query += '{} '.format(group_by)
                else:
                    query += '{}, '.format(group_by)
            query += 'LIMIT {}'.format(select_dict.get('limit', 10000))
            return query, params_list, fields_list
        else:
            raise ProgramConfigException(400, '请联系开发者，parse object参数错误。请传入query的select部分')


class EsEngine(Engine):
    """
    ElasticSearch查询引擎
    """

    _template = {
        'size': 10000,
        'query': {  # Query context
            'bool': {
                'filter': [  # Filter context
                ],
            },
        },
        '_source': {
            'includes': []
        },
        'aggs': {
            'groupby': {
                'terms': {
                    'script': {
                        'source': ''
                    },
                    'size': 10000,
                },
                'aggs': {}
            },
        },
    }

    def _parse_filter(self, filters):
        must_list = []
        for key, val in filters.items():
            if '__' in key:
                field, suffix = key.split('__', 1)
                if suffix == 'gt':
                    must_list.append({
                        'range': {
                            field: {'gt': val}
                        }
                    })
                elif suffix == 'gte':
                    must_list.append({
                        'range': {
                            field: {'gte': val}
                        }
                    })
                elif suffix == 'lt':
                    must_list.append({
                        'range': {
                            field: {'lt': val}
                        }
                    })
                elif suffix == 'lte':
                    must_list.append({
                        'range': {
                            field: {'lte': val}
                        }
                    })
                elif suffix == 'contains':
                    """"
                    TODO: 本来想用match/match_phrase来进行模糊匹配，但是由于这两种查询由于分词的缘故，现有的
                          分词情况并不能完美的模拟sql中的like，所以暂时采用正则查询。正则查询的效率很低。
                    must_list.append({
                        'match_phrase': {
                            field_name: {
                                'query': value
                            }
                        }
                    })
                    """
                    must_list.append({
                        'wildcard': {field: ''.join(['*', val, '*'])}
                    })
                elif suffix == 'startswith':
                    must_list.append({
                        'prefix': {field: val}
                    })
                elif suffix == 'endswith':
                    must_list.append({
                        'wildcard': {field: ''.join(['*', val])}
                    })
                elif suffix == 'range':
                    if len(val) != 2:
                        raise JsonFormatException(3, 'range需要传入长度为2的范围列表。如: [1, 2]。')
                    must_list.append({
                        'range': {
                            field: {'gte': val[0], 'lte': val[1]}
                        }
                    })
                elif suffix == 'in':
                    if isinstance(val, list):
                        must_list.append({
                            'terms': {field: val}
                        })
                    else:
                        raise JsonFormatException(3, 'in需要传入元素列表，而不是{}。', type(val))
                else:
                    raise ProgramConfigException(401, '请联系开发者，parse filter后缀错误。无法识别的后缀{}。', suffix)
            else:
                must_list.append({
                    'term': {
                        key: val
                    }
                })
        return must_list

    def parse(self, select_dict):
        """
        转为elasticsearch的查询dsl。
        :param select_dict: select_dict部分dict
        :return: 返回三元素元组，第一个是查询语句，第二个是index，第三个是fields
        """
        if isinstance(select_dict, dict):
            fields = []
            dsl = copy.deepcopy(EsEngine._template)
            dsl['size'] = select_dict.get('limit', 10000)
            dsl['aggs']['groupby']['terms']['size'] = select_dict.get('limit', 10000)
            dsl['_source']['includes'].extend([field for field in select_dict.get('fields')])

            if select_dict.get('filter'):
                must_list = self._parse_filter(select_dict.get('filter'))
            else:
                must_list = []
            dsl['query']['bool']['filter'].extend(must_list)
            if not dsl['query']['bool']['filter']:  # 若filter为空直接删除
                del dsl['query']['bool']['filter']
            if not dsl['query']['bool']:  # 若bool为空直接删除
                del dsl['query']['bool']
            if not dsl['query']:  # 若query为空直接删除
                del dsl['query']

            dsl_group_by = ''
            dsl_aggs = dsl['aggs']['groupby']['aggs']
            if select_dict.get('group_by') and len(select_dict.get('group_by')) != 0:  # 只有有group by，agg才有意义
                """
                由于ES 6.x以下版本不支持 composite 语法，所以这里采用script方式来实现group by，用来兼容不同版本ES这部分语法的差异性
                script中source的格式：key:value;key:value
                定义成这个样子是方便后面从查询结果中提取数据
                """
                for field in select_dict.get('group_by', []):
                    dsl_group_by = ''.join(
                        [dsl_group_by, "'", field, "'", " + ':' + ", "doc['", field, "'].value", " + ';' + "])
                dsl_group_by = dsl_group_by[:len(dsl_group_by) - len(" + ';' + ")]  # 去掉结尾的 " + ';' + "
                dsl['aggs']['groupby']['terms']['script']['source'] = dsl_group_by
                # 处理 aggregation
                func_map = {'count': 'value_count', 'sum': 'sum', 'avg': 'avg', 'max': 'max', 'min': 'min',
                            'count_distinct': 'cardinality'}
                for agg in select_dict.get('aggregation', []):
                    field, suffix = agg.split('__', 1)
                    if suffix in func_map:
                        dsl_aggs['{}__{}'.format(field, suffix)] = {
                            func_map[suffix]: {'field': field}}
                    else:
                        raise ProgramConfigException(401, '请联系开发者，parse agg后缀错误。无法识别的后缀{}。', suffix)
            else:
                del dsl['aggs']
            return dsl, select_dict.get('from'), None
        else:
            raise ProgramConfigException(400, '请联系开发者，parse object参数错误。需要dict类实例')
