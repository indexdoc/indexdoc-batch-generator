from domain.sysdomain.entity.SysUserEntity import SysUserEntity
from domain.sysdomain.daock import SysUserDaoCK
from utils import IDUtil

def create(user_name ,pwd ,last_login_time ,last_active_time ,create_time ,update_time ,last_login_info ,remark ):
    newentity = SysUserEntity(IDUtil.get_long(),user_name ,pwd ,last_login_time ,last_active_time ,create_time ,update_time ,last_login_info ,remark )
    SysUserDaoCK.insert(newentity)
    return newentity

def delete(sys_user_id):
    SysUserDaoCK.delete_by_id(sys_user_id)

def update(sys_user_id ,user_name ,pwd ,last_login_time ,last_active_time ,create_time ,update_time ,last_login_info ,remark ):
    newentity = SysUserEntity(sys_user_id ,user_name ,pwd ,last_login_time ,last_active_time ,create_time ,update_time ,last_login_info ,remark )
    SysUserDaoCK.update(newentity)
    return newentity

def get_entity_by_id(sys_user_id):
    return SysUserDaoCK.select_by_id(sys_user_id)

def get_all():
    return SysUserDaoCK.select_all()

def get_count():
    return SysUserDaoCK.select_count()

def get_vspage(row_cnt, begin, search_params = None):
    entities,total_cnt = SysUserDaoCK.select_vspage(row_cnt, begin,search_params)
#    id_list = [e.sys_user_id for e in entities]
    return entities,total_cnt

def get_page(row_cnt, begin, search_params = None):
    entities,total_cnt = SysUserDaoCK.select_page(row_cnt, begin,search_params)
#    id_list = [e.sys_user_id for e in entities]
    return entities,total_cnt

def full_search(row_cnt, begin, search_str):
    entities,total_cnt = SysUserDaoCK.full_search(row_cnt=row_cnt, row_begin=begin,search_str=search_str)
#    id_list = [e.sys_user_id for e in entities]
    return entities,total_cnt

def update_by_id(sys_user_id,update_params):
    entity = SysUserDaoCK.update_by_id(sys_user_id,update_params)
    return entity
