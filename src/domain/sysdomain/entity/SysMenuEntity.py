from base.BaseEntity import BaseEntity

myref_tables = list()
myref_tables.append('ref_UpperId_SysMenu')

myref_tables_str = ''
for s in myref_tables:
    myref_tables_str += s+','
if myref_tables_str != '':
    myref_tables_str = myref_tables_str[0:-1]
    
class SysMenuEntity(BaseEntity):
    def __init__(self, sys_menu_id ,menu_name ,upper_id ,order_no ,menu_url ,menu_icon ,open_type ,remark ):
        self.sys_menu_id = sys_menu_id
        self.menu_name = menu_name
        self.upper_id = upper_id
        self.order_no = order_no
        self.menu_url = menu_url
        self.menu_icon = menu_icon
        self.open_type = open_type
        self.remark = remark
        #外键数据 本表外键 多对一
        self.ref_UpperId_SysMenu = None #ref to sys_menu

    @staticmethod
    def get_attrcodes():
        return ['sys_menu_id','menu_name','upper_id','order_no','menu_url','menu_icon','open_type','remark']

    @staticmethod
    def get_attrnames():
        return ['菜单ID','菜单名称','上级ID','排序','菜单URL','菜单图标','打开方式','备注']

    def get_name(self):
        return self.menu_name

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
        return SysMenuEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7])
