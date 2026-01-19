from base.BaseEntity import BaseEntity

myref_tables = list()
myref_tables.append('ref_SysUserId_SysUser')
myref_tables.append('ref_SysRoleId_SysRole')
myref_tables.append('ref_SysOrgId_SysOrg')
myref_tables.append('ref_OrgDutyId_OrgDuty')
myref_tables.append('ref_SysMenuAuthId_SysMenuAuth')

myref_tables_str = ''
for s in myref_tables:
    myref_tables_str += s+','
if myref_tables_str != '':
    myref_tables_str = myref_tables_str[0:-1]
    
class SysApiAuthEntity(BaseEntity):
    def __init__(self, sys_api_auth_id ,api_name ,api_url ,sys_user_id ,sys_role_id ,sys_org_id ,org_duty_id ,auth_flag ,sys_menu_auth_id ,update_type ,remark ):
        self.sys_api_auth_id = sys_api_auth_id
        self.api_name = api_name
        self.api_url = api_url
        self.sys_user_id = sys_user_id
        self.sys_role_id = sys_role_id
        self.sys_org_id = sys_org_id
        self.org_duty_id = org_duty_id
        self.auth_flag = auth_flag
        self.sys_menu_auth_id = sys_menu_auth_id
        self.update_type = update_type
        self.remark = remark
        #外键数据 本表外键 多对一
        self.ref_SysUserId_SysUser = None #ref to sys_user
        self.ref_SysRoleId_SysRole = None #ref to sys_role
        self.ref_SysOrgId_SysOrg = None #ref to sys_org
        self.ref_OrgDutyId_OrgDuty = None #ref to org_duty
        self.ref_SysMenuAuthId_SysMenuAuth = None #ref to sys_menu_auth

    @staticmethod
    def get_attrcodes():
        return ['sys_api_auth_id','api_name','api_url','sys_user_id','sys_role_id','sys_org_id','org_duty_id','auth_flag','sys_menu_auth_id','update_type','remark']

    @staticmethod
    def get_attrnames():
        return ['接口权限ID','接口名称','接口URL','用户ID','角色ID','组织机构ID','组织机构职务ID','权限标识','菜单权限ID','更新标识','说明']

    def get_name(self):
        return self.api_name

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
        return SysApiAuthEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9], tup[10])
