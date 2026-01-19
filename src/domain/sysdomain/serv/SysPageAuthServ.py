from domain.sysdomain.entity.SysPageAuthEntity import SysPageAuthEntity
from domain.sysdomain.daock import SysPageAuthDaoCK
from utils import IDUtil

def create(page_name ,page_path ,sys_user_id ,sys_role_id ,sys_org_id ,org_duty_id ,auth_flag ,sys_menu_auth_id ,update_type ,remark ):
    newentity = SysPageAuthEntity(IDUtil.get_long(),page_name ,page_path ,sys_user_id ,sys_role_id ,sys_org_id ,org_duty_id ,auth_flag ,sys_menu_auth_id ,update_type ,remark )
    SysPageAuthDaoCK.insert(newentity)
    return newentity

def delete(sys_page_auth_id):
    SysPageAuthDaoCK.delete_by_id(sys_page_auth_id)

def update(sys_page_auth_id ,page_name ,page_path ,sys_user_id ,sys_role_id ,sys_org_id ,org_duty_id ,auth_flag ,sys_menu_auth_id ,update_type ,remark ):
    newentity = SysPageAuthEntity(sys_page_auth_id ,page_name ,page_path ,sys_user_id ,sys_role_id ,sys_org_id ,org_duty_id ,auth_flag ,sys_menu_auth_id ,update_type ,remark )
    SysPageAuthDaoCK.update(newentity)
    return newentity

def get_entity_by_id(sys_page_auth_id):
    return SysPageAuthDaoCK.select_by_id(sys_page_auth_id)

def get_all():
    return SysPageAuthDaoCK.select_all()

def get_count():
    return SysPageAuthDaoCK.select_count()

def get_vspage(row_cnt, begin, search_params = None):
    entities,total_cnt = SysPageAuthDaoCK.select_vspage(row_cnt, begin,search_params)
#    id_list = [e.sys_page_auth_id for e in entities]
    return entities,total_cnt

def get_page(row_cnt, begin, search_params = None):
    entities,total_cnt = SysPageAuthDaoCK.select_page(row_cnt, begin,search_params)
#    id_list = [e.sys_page_auth_id for e in entities]
    return entities,total_cnt

def full_search(row_cnt, begin, search_str):
    entities,total_cnt = SysPageAuthDaoCK.full_search(row_cnt=row_cnt, row_begin=begin,search_str=search_str)
#    id_list = [e.sys_page_auth_id for e in entities]
    return entities,total_cnt

def update_by_id(sys_page_auth_id,update_params):
    entity = SysPageAuthDaoCK.update_by_id(sys_page_auth_id,update_params)
    return entity
