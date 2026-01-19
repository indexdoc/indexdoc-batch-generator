from domain.sysdomain.entity.UserFileEntity import UserFileEntity
from domain.sysdomain.daock import UserFileDaoCK
from utils import IDUtil

def create(file_uuid ,upload_user_id ,file_name ,file_type ,content_type ,file_storage ,cdn_url ,file_suffix ,file_content ,file_preview ,file_summary ,upload_time ):
    newentity = UserFileEntity(IDUtil.get_long(),file_uuid ,upload_user_id ,file_name ,file_type ,content_type ,file_storage ,cdn_url ,file_suffix ,file_content ,file_preview ,file_summary ,upload_time )
    UserFileDaoCK.insert(newentity)
    return newentity

def delete(user_file_id):
    UserFileDaoCK.delete_by_id(user_file_id)

def update(user_file_id ,file_uuid ,upload_user_id ,file_name ,file_type ,content_type ,file_storage ,cdn_url ,file_suffix ,file_content ,file_preview ,file_summary ,upload_time ):
    newentity = UserFileEntity(user_file_id ,file_uuid ,upload_user_id ,file_name ,file_type ,content_type ,file_storage ,cdn_url ,file_suffix ,file_content ,file_preview ,file_summary ,upload_time )
    UserFileDaoCK.update(newentity)
    return newentity

def get_entity_by_id(user_file_id):
    return UserFileDaoCK.select_by_id(user_file_id)

def get_all():
    return UserFileDaoCK.select_all()

def get_count():
    return UserFileDaoCK.select_count()

def get_vspage(row_cnt, begin, search_params = None):
    entities,total_cnt = UserFileDaoCK.select_vspage(row_cnt, begin,search_params)
#    id_list = [e.user_file_id for e in entities]
    return entities,total_cnt


def get_vspage2(user_file_id_list):
    entities = UserFileDaoCK.select_by_UserFileIdList2(user_file_id_list)
    #    id_list = [e.user_file_id for e in entities]
    return entities


def get_page(row_cnt, begin, search_params=None):
    entities, total_cnt = UserFileDaoCK.select_page(row_cnt, begin, search_params)
    #    id_list = [e.user_file_id for e in entities]
    return entities, total_cnt

def full_search(row_cnt, begin, search_str):
    entities,total_cnt = UserFileDaoCK.full_search(row_cnt=row_cnt, row_begin=begin,search_str=search_str)
#    id_list = [e.user_file_id for e in entities]
    return entities,total_cnt

def update_by_id(user_file_id,update_params):
    entity = UserFileDaoCK.update_by_id(user_file_id,update_params)
    return entity
