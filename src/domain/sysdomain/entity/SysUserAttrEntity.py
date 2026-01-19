from base.BaseEntity import BaseEntity

myref_tables = list()
myref_tables.append('ref_SysUserId_SysUser')

myref_tables_str = ''
for s in myref_tables:
    myref_tables_str += s+','
if myref_tables_str != '':
    myref_tables_str = myref_tables_str[0:-1]
    
class SysUserAttrEntity(BaseEntity):
    def __init__(self, sys_user_attr_id ,sys_user_id ,attr_name ,attr_value ,create_time ,update_time ):
        self.sys_user_attr_id = sys_user_attr_id
        self.sys_user_id = sys_user_id
        self.attr_name = attr_name
        self.attr_value = attr_value
        self.create_time = create_time
        self.update_time = update_time
        #外键数据 本表外键 多对一
        self.ref_SysUserId_SysUser = None #ref to sys_user

    @staticmethod
    def get_attrcodes():
        return ['sys_user_attr_id','sys_user_id','attr_name','attr_value','create_time','update_time']

    @staticmethod
    def get_attrnames():
        return ['用户属性ID','用户ID','属性名称','属性值','创建时间','修改时间']

    def get_name(self):
        return self.attr_name

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
        return SysUserAttrEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5])
