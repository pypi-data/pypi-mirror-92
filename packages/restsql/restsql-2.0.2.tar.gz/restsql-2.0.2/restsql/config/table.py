# -*- coding:utf-8 -*-

from enum import Enum, unique

from restsql.exception import ProgramConfigException

__all__ = ['FType', 'Table']


@unique
class FType(Enum):
    INT = 'int'
    NUMBER = 'float'
    STRING = 'string'
    DATETIME = 'datetime'
    TIMEDELTA = 'timedelta'


class Table:

    def __init__(self, name, table_name, fields):
        """
        :param name: 该表对外展示的名。string。
        :param table_name: 表名。string。
        :param fields: 该表字段。map。
        """
        if isinstance(fields, dict):
            self.name = name
            self.table_name = table_name
            for (fname, ftype) in fields.items():
                if FType.INT.value == ftype:
                    fields[fname] = FType.INT
                elif FType.NUMBER.value == ftype:
                    fields[fname] = FType.NUMBER
                elif FType.STRING.value == ftype:
                    fields[fname] = FType.STRING
                elif FType.DATETIME.value == ftype:
                    fields[fname] = FType.DATETIME
                elif FType.TIMEDELTA.value == ftype:
                    fields[fname] = FType.TIMEDELTA
                else:
                    raise ProgramConfigException(301, '表字段类型出错，无法识别的类型{}', ftype)
            self.fields = fields
        else:
            raise ProgramConfigException(301, '无法识别的fields类型: {}', type(fields))
