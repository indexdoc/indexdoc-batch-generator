from base.BaseEntity import BaseEntity

myref_tables = list()

myref_tables_str = ''
for s in myref_tables:
    myref_tables_str += s+','
if myref_tables_str != '':
    myref_tables_str = myref_tables_str[0:-1]
    
class SysRoleEntity(BaseEntity):
    def __init__(self, sys_role_id ,role_name ):
        self.sys_role_id = sys_role_id
        self.role_name = role_name

    @staticmethod
    def get_attrcodes():
        return ['sys_role_id','role_name']

    @staticmethod
    def get_attrnames():
        return ['角色ID','角色名称']

    def get_name(self):
        return self.role_name

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
        return SysRoleEntity(tup[0], tup[1])
