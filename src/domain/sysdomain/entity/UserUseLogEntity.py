from base.BaseEntity import BaseEntity

myref_tables = list()
myref_tables.append('ref_SysUserId_SysUser')

myref_tables_str = ''
for s in myref_tables:
    myref_tables_str += s+','
if myref_tables_str != '':
    myref_tables_str = myref_tables_str[0:-1]
    
class UserUseLogEntity(BaseEntity):
    def __init__(self, user_use_log_id ,sys_user_id ,ip_addr ,local_ip ,api_url ,gpu_info ,remark ,create_time ):
        self.user_use_log_id = user_use_log_id
        self.sys_user_id = sys_user_id
        self.ip_addr = ip_addr
        self.local_ip = local_ip
        self.api_url = api_url
        self.gpu_info = gpu_info
        self.remark = remark
        self.create_time = create_time
        #外键数据 本表外键 多对一
        self.ref_SysUserId_SysUser = None #ref to sys_user

    @staticmethod
    def get_attrcodes():
        return ['user_use_log_id','sys_user_id','ip_addr','local_ip','api_url','gpu_info','remark','create_time']

    @staticmethod
    def get_attrnames():
        return ['用户操作日志ID','用户ID','ip地址','本地ip','接口url','GPU信息','备注','创建时间']

    def get_name(self):
        return self.user_use_log_id

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
        return UserUseLogEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7])
