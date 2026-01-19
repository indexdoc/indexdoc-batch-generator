from domain.sysdomain.entity.UserUseLogEntity import UserUseLogEntity
from domain.sysdomain.daock import UserUseLogDaoCK
from utils import IDUtil

def create(sys_user_id ,ip_addr ,local_ip ,api_url ,gpu_info ,remark ,create_time ):
    newentity = UserUseLogEntity(IDUtil.get_long(),sys_user_id ,ip_addr ,local_ip ,api_url ,gpu_info ,remark ,create_time )
    UserUseLogDaoCK.insert(newentity)
    return newentity

def delete(user_use_log_id):
    UserUseLogDaoCK.delete_by_id(user_use_log_id)

def update(user_use_log_id ,sys_user_id ,ip_addr ,local_ip ,api_url ,gpu_info ,remark ,create_time ):
    newentity = UserUseLogEntity(user_use_log_id ,sys_user_id ,ip_addr ,local_ip ,api_url ,gpu_info ,remark ,create_time )
    UserUseLogDaoCK.update(newentity)
    return newentity

def get_entity_by_id(user_use_log_id):
    return UserUseLogDaoCK.select_by_id(user_use_log_id)

def get_all():
    return UserUseLogDaoCK.select_all()

def get_count():
    return UserUseLogDaoCK.select_count()

def get_vspage(row_cnt, begin, search_params = None):
    entities,total_cnt = UserUseLogDaoCK.select_vspage(row_cnt, begin,search_params)
#    id_list = [e.user_use_log_id for e in entities]
    return entities,total_cnt

def get_page(row_cnt, begin, search_params = None):
    entities,total_cnt = UserUseLogDaoCK.select_page(row_cnt, begin,search_params)
#    id_list = [e.user_use_log_id for e in entities]
    return entities,total_cnt

def full_search(row_cnt, begin, search_str):
    entities,total_cnt = UserUseLogDaoCK.full_search(row_cnt=row_cnt, row_begin=begin,search_str=search_str)
#    id_list = [e.user_use_log_id for e in entities]
    return entities,total_cnt

def update_by_id(user_use_log_id,update_params):
    entity = UserUseLogDaoCK.update_by_id(user_use_log_id,update_params)
    return entity
