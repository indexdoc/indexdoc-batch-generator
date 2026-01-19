from base.BaseEntity import BaseEntity

myref_tables = list()
myref_tables.append('ref_SysOrgId_SysOrg')

myref_tables_str = ''
for s in myref_tables:
    myref_tables_str += s+','
if myref_tables_str != '':
    myref_tables_str = myref_tables_str[0:-1]
    
class OrgDutyEntity(BaseEntity):
    def __init__(self, org_duty_id ,sys_org_id ,org_duty_name ,update_time ,create_time ):
        self.org_duty_id = org_duty_id
        self.sys_org_id = sys_org_id
        self.org_duty_name = org_duty_name
        self.update_time = update_time
        self.create_time = create_time
        #外键数据 本表外键 多对一
        self.ref_SysOrgId_SysOrg = None #ref to sys_org

    @staticmethod
    def get_attrcodes():
        return ['org_duty_id','sys_org_id','org_duty_name','update_time','create_time']

    @staticmethod
    def get_attrnames():
        return ['组织机构职务ID','组织机构ID','职务名称','修改时间','创建时间']

    def get_name(self):
        return self.org_duty_name

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
        return OrgDutyEntity(tup[0], tup[1], tup[2], tup[3], tup[4])
