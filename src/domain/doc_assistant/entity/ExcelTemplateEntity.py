from base.BaseEntity import BaseEntity

myref_tables = list()
myref_tables.append('ref_UserFileId_UserFile')

myref_tables_str = ''
for s in myref_tables:
    myref_tables_str += s+','
if myref_tables_str != '':
    myref_tables_str = myref_tables_str[0:-1]
    
class ExcelTemplateEntity(BaseEntity):
    def __init__(self, excel_template_id ,user_file_id ,create_time ):
        self.excel_template_id = excel_template_id
        self.user_file_id = user_file_id
        self.create_time = create_time
        #外键数据 本表外键 多对一
        self.ref_UserFileId_UserFile = None #ref to user_file

    @staticmethod
    def get_attrcodes():
        return ['excel_template_id','user_file_id','create_time']

    @staticmethod
    def get_attrnames():
        return ['excel模板ID','用户文件ID','创建时间']

    def get_name(self):
        return self.excel_template_id

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
        return ExcelTemplateEntity(tup[0], tup[1], tup[2])
