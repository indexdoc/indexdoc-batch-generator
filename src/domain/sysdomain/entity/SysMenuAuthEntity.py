from base.BaseEntity import BaseEntity

myref_tables = list()
myref_tables.append('ref_SysMenuId_SysMenu')
myref_tables.append('ref_SysRoleId_SysRole')
myref_tables.append('ref_SysUserId_SysUser')
myref_tables.append('ref_SysOrgId_SysOrg')
myref_tables.append('ref_OrgDutyId_OrgDuty')

myref_tables_str = ''
for s in myref_tables:
    myref_tables_str += s+','
if myref_tables_str != '':
    myref_tables_str = myref_tables_str[0:-1]
    
class SysMenuAuthEntity(BaseEntity):
    def __init__(self, sys_menu_auth_id ,sys_menu_id ,sys_user_id ,sys_role_id ,sys_org_id ,org_duty_id ,remark ):
        self.sys_menu_auth_id = sys_menu_auth_id
        self.sys_menu_id = sys_menu_id
        self.sys_user_id = sys_user_id
        self.sys_role_id = sys_role_id
        self.sys_org_id = sys_org_id
        self.org_duty_id = org_duty_id
        self.remark = remark
        #外键数据 本表外键 多对一
        self.ref_SysMenuId_SysMenu = None #ref to sys_menu
        self.ref_SysRoleId_SysRole = None #ref to sys_role
        self.ref_SysUserId_SysUser = None #ref to sys_user
        self.ref_SysOrgId_SysOrg = None #ref to sys_org
        self.ref_OrgDutyId_OrgDuty = None #ref to org_duty

    @staticmethod
    def get_attrcodes():
        return ['sys_menu_auth_id','sys_menu_id','sys_user_id','sys_role_id','sys_org_id','org_duty_id','remark']

    @staticmethod
    def get_attrnames():
        return ['菜单权限ID','菜单ID','用户ID','角色ID','组织机构ID','组织机构职务ID','备注']

    def get_name(self):
        return self.sys_menu_auth_id

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
        return SysMenuAuthEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6])
