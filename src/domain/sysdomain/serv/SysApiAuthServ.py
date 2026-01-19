from domain.sysdomain.entity.SysApiAuthEntity import SysApiAuthEntity
from domain.sysdomain.daock import SysApiAuthDaoCK
from utils import IDUtil

def create(api_name ,api_url ,sys_user_id ,sys_role_id ,sys_org_id ,org_duty_id ,auth_flag ,sys_menu_auth_id ,update_type ,remark ):
    newentity = SysApiAuthEntity(IDUtil.get_long(),api_name ,api_url ,sys_user_id ,sys_role_id ,sys_org_id ,org_duty_id ,auth_flag ,sys_menu_auth_id ,update_type ,remark )
    SysApiAuthDaoCK.insert(newentity)
    return newentity

def delete(sys_api_auth_id):
    SysApiAuthDaoCK.delete_by_id(sys_api_auth_id)

def update(sys_api_auth_id ,api_name ,api_url ,sys_user_id ,sys_role_id ,sys_org_id ,org_duty_id ,auth_flag ,sys_menu_auth_id ,update_type ,remark ):
    newentity = SysApiAuthEntity(sys_api_auth_id ,api_name ,api_url ,sys_user_id ,sys_role_id ,sys_org_id ,org_duty_id ,auth_flag ,sys_menu_auth_id ,update_type ,remark )
    SysApiAuthDaoCK.update(newentity)
    return newentity

def get_entity_by_id(sys_api_auth_id):
    return SysApiAuthDaoCK.select_by_id(sys_api_auth_id)

def get_all():
    return SysApiAuthDaoCK.select_all()

def get_count():
    return SysApiAuthDaoCK.select_count()

def get_vspage(row_cnt, begin, search_params = None):
    entities,total_cnt = SysApiAuthDaoCK.select_vspage(row_cnt, begin,search_params)
#    id_list = [e.sys_api_auth_id for e in entities]
    return entities,total_cnt

def get_page(row_cnt, begin, search_params = None):
    entities,total_cnt = SysApiAuthDaoCK.select_page(row_cnt, begin,search_params)
#    id_list = [e.sys_api_auth_id for e in entities]
    return entities,total_cnt

def full_search(row_cnt, begin, search_str):
    entities,total_cnt = SysApiAuthDaoCK.full_search(row_cnt=row_cnt, row_begin=begin,search_str=search_str)
#    id_list = [e.sys_api_auth_id for e in entities]
    return entities,total_cnt

def update_by_id(sys_api_auth_id,update_params):
    entity = SysApiAuthDaoCK.update_by_id(sys_api_auth_id,update_params)
    return entity
