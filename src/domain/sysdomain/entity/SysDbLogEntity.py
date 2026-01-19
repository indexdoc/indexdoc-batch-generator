from base.BaseEntity import BaseEntity

myref_tables = list()
myref_tables.append('ref_SysUserId_SysUser')

myref_tables_str = ''
for s in myref_tables:
    myref_tables_str += s+','
if myref_tables_str != '':
    myref_tables_str = myref_tables_str[0:-1]
    
class SysDbLogEntity(BaseEntity):
    def __init__(self, sys_db_log_id ,sys_user_id ,op_datetime ,op_duration ,op_type ,table_code ,data_id ,sql_str ,sql_param ,sql_result ):
        self.sys_db_log_id = sys_db_log_id
        self.sys_user_id = sys_user_id
        self.op_datetime = op_datetime
        self.op_duration = op_duration
        self.op_type = op_type
        self.table_code = table_code
        self.data_id = data_id
        self.sql_str = sql_str
        self.sql_param = sql_param
        self.sql_result = sql_result
        #外键数据 本表外键 多对一
        self.ref_SysUserId_SysUser = None #ref to sys_user

    @staticmethod
    def get_attrcodes():
        return ['sys_db_log_id','sys_user_id','op_datetime','op_duration','op_type','table_code','data_id','sql_str','sql_param','sql_result']

    @staticmethod
    def get_attrnames():
        return ['数据库日志ID','系统用户ID','操作时间','执行时长','操作类型','表名','数据ID','操作语句','语句参数','执行结果']

    def get_name(self):
        return self.sys_db_log_id

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
        return SysDbLogEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9])
