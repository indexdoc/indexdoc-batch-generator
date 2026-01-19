from base.BaseEntity import BaseEntity

myref_tables = list()
myref_tables.append('ref_UserFileId_UserFile')

myref_tables_str = ''
for s in myref_tables:
    myref_tables_str += s+','
if myref_tables_str != '':
    myref_tables_str = myref_tables_str[0:-1]
    
class WordTemplateEntity(BaseEntity):
    def __init__(self, word_tempalte_id ,user_file_id ,create_time ):
        self.word_tempalte_id = word_tempalte_id
        self.user_file_id = user_file_id
        self.create_time = create_time
        #外键数据 本表外键 多对一
        self.ref_UserFileId_UserFile = None #ref to user_file

    @staticmethod
    def get_attrcodes():
        return ['word_tempalte_id','user_file_id','create_time']

    @staticmethod
    def get_attrnames():
        return ['word模板ID','用户文件ID','创建时间']

    def get_name(self):
        return self.word_tempalte_id

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
        return WordTemplateEntity(tup[0], tup[1], tup[2])
