from base.BaseEntity import BaseEntity

myref_tables = list()
myref_tables.append('ref_UploadUserId_SysUser')

myref_tables_str = ''
for s in myref_tables:
    myref_tables_str += s+','
if myref_tables_str != '':
    myref_tables_str = myref_tables_str[0:-1]
    
class UserFileEntity(BaseEntity):
    def __init__(self, user_file_id ,file_uuid ,upload_user_id ,file_name ,file_type ,content_type ,file_storage ,cdn_url ,file_suffix ,file_content ,file_preview ,file_summary ,upload_time ):
        self.user_file_id = user_file_id
        self.file_uuid = file_uuid
        self.upload_user_id = upload_user_id
        self.file_name = file_name
        self.file_type = file_type
        self.content_type = content_type
        self.file_storage = file_storage
        self.cdn_url = cdn_url
        self.file_suffix = file_suffix
        self.file_content = file_content
        self.file_preview = file_preview
        self.file_summary = file_summary
        self.upload_time = upload_time
        #外键数据 本表外键 多对一
        self.ref_UploadUserId_SysUser = None #ref to sys_user

    @staticmethod
    def get_attrcodes():
        return ['user_file_id','file_uuid','upload_user_id','file_name','file_type','content_type','file_storage','cdn_url','file_suffix','file_content','file_preview','file_summary','upload_time']

    @staticmethod
    def get_attrnames():
        return ['用户文件ID','文件UUID','文件上传用户ID','文件名称','文件类别','内容类别','文件存储地址','CDN地址','文件后缀','文件内容','文件预览图','文件摘要','文件上传时间']

    def get_name(self):
        return self.file_name

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
        return UserFileEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9], tup[10], tup[11], tup[12])
