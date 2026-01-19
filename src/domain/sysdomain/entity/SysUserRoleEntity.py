from base.BaseEntity import BaseEntity

myref_tables = list()
myref_tables.append('ref_SysUserId_SysUser')
myref_tables.append('ref_SysRoleId_SysRole')

myref_tables_str = ''
for s in myref_tables:
    myref_tables_str += s+','
if myref_tables_str != '':
    myref_tables_str = myref_tables_str[0:-1]
    
class SysUserRoleEntity(BaseEntity):
    def __init__(self, sys_user_role_id ,sys_user_id ,sys_role_id ):
        self.sys_user_role_id = sys_user_role_id
        self.sys_user_id = sys_user_id
        self.sys_role_id = sys_role_id
        #外键数据 本表外键 多对一
        self.ref_SysUserId_SysUser = None #ref to sys_user
        self.ref_SysRoleId_SysRole = None #ref to sys_role

    @staticmethod
    def get_attrcodes():
        return ['sys_user_role_id','sys_user_id','sys_role_id']

    @staticmethod
    def get_attrnames():
        return ['用户角色ID','用户ID','角色ID']

    def get_name(self):
        return self.sys_user_role_id

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
        return SysUserRoleEntity(tup[0], tup[1], tup[2])
