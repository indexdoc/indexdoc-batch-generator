from domain.sysdomain.entity.SysMenuAuthEntity import SysMenuAuthEntity
from domain.sysdomain.daock import SysMenuAuthDaoCK
from utils import IDUtil

def create(sys_menu_id ,sys_user_id ,sys_role_id ,sys_org_id ,org_duty_id ,remark ):
    newentity = SysMenuAuthEntity(IDUtil.get_long(),sys_menu_id ,sys_user_id ,sys_role_id ,sys_org_id ,org_duty_id ,remark )
    SysMenuAuthDaoCK.insert(newentity)
    return newentity

def delete(sys_menu_auth_id):
    SysMenuAuthDaoCK.delete_by_id(sys_menu_auth_id)

def update(sys_menu_auth_id ,sys_menu_id ,sys_user_id ,sys_role_id ,sys_org_id ,org_duty_id ,remark ):
    newentity = SysMenuAuthEntity(sys_menu_auth_id ,sys_menu_id ,sys_user_id ,sys_role_id ,sys_org_id ,org_duty_id ,remark )
    SysMenuAuthDaoCK.update(newentity)
    return newentity

def get_entity_by_id(sys_menu_auth_id):
    return SysMenuAuthDaoCK.select_by_id(sys_menu_auth_id)

def get_all():
    return SysMenuAuthDaoCK.select_all()

def get_count():
    return SysMenuAuthDaoCK.select_count()

def get_vspage(row_cnt, begin, search_params = None):
    entities,total_cnt = SysMenuAuthDaoCK.select_vspage(row_cnt, begin,search_params)
#    id_list = [e.sys_menu_auth_id for e in entities]
    return entities,total_cnt

def get_page(row_cnt, begin, search_params = None):
    entities,total_cnt = SysMenuAuthDaoCK.select_page(row_cnt, begin,search_params)
#    id_list = [e.sys_menu_auth_id for e in entities]
    return entities,total_cnt

def full_search(row_cnt, begin, search_str):
    entities,total_cnt = SysMenuAuthDaoCK.full_search(row_cnt=row_cnt, row_begin=begin,search_str=search_str)
#    id_list = [e.sys_menu_auth_id for e in entities]
    return entities,total_cnt

def update_by_id(sys_menu_auth_id,update_params):
    entity = SysMenuAuthDaoCK.update_by_id(sys_menu_auth_id,update_params)
    return entity
