from base.BaseEntity import BaseEntity

myref_tables = list()
myref_tables.append('ref_UserFileId_UserFile')
myref_tables.append('ref_ExcelTemplateId_ExcelTemplate')

myref_tables_str = ''
for s in myref_tables:
    myref_tables_str += s+','
if myref_tables_str != '':
    myref_tables_str = myref_tables_str[0:-1]
    
class GenerateFilesEntity(BaseEntity):
    def __init__(self, generate_file_id ,user_file_id ,excel_template_id ,create_time ):
        self.generate_file_id = generate_file_id
        self.user_file_id = user_file_id
        self.excel_template_id = excel_template_id
        self.create_time = create_time
        #外键数据 本表外键 多对一
        self.ref_UserFileId_UserFile = None #ref to user_file
        self.ref_ExcelTemplateId_ExcelTemplate = None #ref to excel_template

    @staticmethod
    def get_attrcodes():
        return ['generate_file_id','user_file_id','excel_template_id','create_time']

    @staticmethod
    def get_attrnames():
        return ['生成文件ID','用户文件ID','excel模板ID','创建时间']

    def get_name(self):
        return self.generate_file_id

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
        return GenerateFilesEntity(tup[0], tup[1], tup[2], tup[3])
