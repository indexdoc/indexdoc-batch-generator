from base.BaseEntity import BaseEntity

myref_tables = list()
myref_tables.append('ref_UpperId_SysOrg')

myref_tables_str = ''
for s in myref_tables:
    myref_tables_str += s+','
if myref_tables_str != '':
    myref_tables_str = myref_tables_str[0:-1]
    
class SysOrgEntity(BaseEntity):
    def __init__(self, sys_org_id ,org_name ,upper_id ,sort_no ,create_time ,update_time ):
        self.sys_org_id = sys_org_id
        self.org_name = org_name
        self.upper_id = upper_id
        self.sort_no = sort_no
        self.create_time = create_time
        self.update_time = update_time
        #外键数据 本表外键 多对一
        self.ref_UpperId_SysOrg = None #ref to sys_org

    @staticmethod
    def get_attrcodes():
        return ['sys_org_id','org_name','upper_id','sort_no','create_time','update_time']

    @staticmethod
    def get_attrnames():
        return ['组织机构ID','名称','上级组织机构ID','排序','创建时间','修改时间']

    def get_name(self):
        return self.org_name

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
        return SysOrgEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5])
