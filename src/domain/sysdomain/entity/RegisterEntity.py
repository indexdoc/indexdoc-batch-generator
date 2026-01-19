from base.BaseEntity import BaseEntity

myref_tables = list()
myref_tables.append('ref_SysUserId_SysUser')

myref_tables_str = ''
for s in myref_tables:
    myref_tables_str += s+','
if myref_tables_str != '':
    myref_tables_str = myref_tables_str[0:-1]
    
class RegisterEntity(BaseEntity):
    def __init__(self, register_id ,sys_user_id ,phone_no ,name ,user_name ,company_name ,pwd ,status ,create_time ,update_time ,remark ):
        self.register_id = register_id
        self.sys_user_id = sys_user_id
        self.phone_no = phone_no
        self.name = name
        self.user_name = user_name
        self.company_name = company_name
        self.pwd = pwd
        self.status = status
        self.create_time = create_time
        self.update_time = update_time
        self.remark = remark
        #外键数据 本表外键 多对一
        self.ref_SysUserId_SysUser = None #ref to sys_user

    @staticmethod
    def get_attrcodes():
        return ['register_id','sys_user_id','phone_no','name','user_name','company_name','pwd','status','create_time','update_time','remark']

    @staticmethod
    def get_attrnames():
        return ['用户注册ID','用户ID','手机号','姓名','用户名','公司名称','登录密码','审核状态','创建时间','修改时间','备注']

    def get_name(self):
        return self.name

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
        return RegisterEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9], tup[10])
