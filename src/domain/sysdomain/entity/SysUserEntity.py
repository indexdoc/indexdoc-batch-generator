from base.BaseEntity import BaseEntity

myref_tables = list()

myref_tables_str = ''
for s in myref_tables:
    myref_tables_str += s+','
if myref_tables_str != '':
    myref_tables_str = myref_tables_str[0:-1]
    
class SysUserEntity(BaseEntity):
    def __init__(self, sys_user_id ,user_name ,pwd ,last_login_time ,last_active_time ,create_time ,update_time ,last_login_info ,remark ):
        self.sys_user_id = sys_user_id
        self.user_name = user_name
        self.pwd = pwd
        self.last_login_time = last_login_time
        self.last_active_time = last_active_time
        self.create_time = create_time
        self.update_time = update_time
        self.last_login_info = last_login_info
        self.remark = remark

    @staticmethod
    def get_attrcodes():
        return ['sys_user_id','user_name','pwd','last_login_time','last_active_time','create_time','update_time','last_login_info','remark']

    @staticmethod
    def get_attrnames():
        return ['用户ID','用户名','密码','最近登录时间','最近活动时间','创建时间','修改时间','最近登录信息','备注']

    def get_name(self):
        return self.user_name

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
        return SysUserEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8])
