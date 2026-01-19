from base.BaseEntity import BaseEntity

myref_tables = list()

myref_tables_str = ''
for s in myref_tables:
    myref_tables_str += s+','
if myref_tables_str != '':
    myref_tables_str = myref_tables_str[0:-1]
    
class SysDictEntity(BaseEntity):
    def __init__(self, sys_dict_id ,module_name ,table_name ,column_name ,select_mode ,data_value ,remark ):
        self.sys_dict_id = sys_dict_id
        self.module_name = module_name
        self.table_name = table_name
        self.column_name = column_name
        self.select_mode = select_mode
        self.data_value = data_value
        self.remark = remark

    @staticmethod
    def get_attrcodes():
        return ['sys_dict_id','module_name','table_name','column_name','select_mode','data_value','remark']

    @staticmethod
    def get_attrnames():
        return ['系统字典ID','模块名','表名','字段名','选择方式','数值','备注']

    def get_name(self):
        return self.module_name

    @staticmethod
    def get_myref_tables():
        return myref_tables
        
    @staticmethod
    def get_myref_tables_str():
        return myref_tables_str
        
    @staticmethod
    def create_by_tuple(tup:tuple):
        if tup is None:
            return None
        return SysDictEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6])
