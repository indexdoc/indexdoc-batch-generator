from domain.sysdomain.entity.SysRoleEntity import SysRoleEntity
from domain.sysdomain.daock import SysRoleDaoCK
from utils import IDUtil

def create(role_name ):
    newentity = SysRoleEntity(IDUtil.get_long(),role_name )
    SysRoleDaoCK.insert(newentity)
    return newentity

def delete(sys_role_id):
    SysRoleDaoCK.delete_by_id(sys_role_id)

def update(sys_role_id ,role_name ):
    newentity = SysRoleEntity(sys_role_id ,role_name )
    SysRoleDaoCK.update(newentity)
    return newentity

def get_entity_by_id(sys_role_id):
    return SysRoleDaoCK.select_by_id(sys_role_id)

def get_all():
    return SysRoleDaoCK.select_all()

def get_count():
    return SysRoleDaoCK.select_count()

def get_vspage(row_cnt, begin, search_params = None):
    entities,total_cnt = SysRoleDaoCK.select_vspage(row_cnt, begin,search_params)
#    id_list = [e.sys_role_id for e in entities]
    return entities,total_cnt

def get_page(row_cnt, begin, search_params = None):
    entities,total_cnt = SysRoleDaoCK.select_page(row_cnt, begin,search_params)
#    id_list = [e.sys_role_id for e in entities]
    return entities,total_cnt

def full_search(row_cnt, begin, search_str):
    entities,total_cnt = SysRoleDaoCK.full_search(row_cnt=row_cnt, row_begin=begin,search_str=search_str)
#    id_list = [e.sys_role_id for e in entities]
    return entities,total_cnt

def update_by_id(sys_role_id,update_params):
    entity = SysRoleDaoCK.update_by_id(sys_role_id,update_params)
    return entity
