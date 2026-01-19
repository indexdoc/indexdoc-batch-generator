from domain.sysdomain.entity.SysUserRoleEntity import SysUserRoleEntity
from domain.sysdomain.daock import SysUserRoleDaoCK
from utils import IDUtil


def create(sys_user_id, sys_role_id):
    newentity = SysUserRoleEntity(IDUtil.get_long(), sys_user_id, sys_role_id)
    SysUserRoleDaoCK.insert(newentity)
    return newentity


def delete(sys_user_role_id):
    SysUserRoleDaoCK.delete_by_id(sys_user_role_id)


def update(sys_user_role_id, sys_user_id, sys_role_id):
    newentity = SysUserRoleEntity(sys_user_role_id, sys_user_id, sys_role_id)
    SysUserRoleDaoCK.update(newentity)
    return newentity


def get_entity_by_id(sys_user_role_id):
    return SysUserRoleDaoCK.select_by_id(sys_user_role_id)


def get_all():
    return SysUserRoleDaoCK.select_all()


def get_count():
    return SysUserRoleDaoCK.select_count()


def get_vspage(row_cnt, begin, search_params=None):
    entities, total_cnt = SysUserRoleDaoCK.select_vspage(row_cnt, begin, search_params)
    #    id_list = [e.sys_user_role_id for e in entities]
    return entities, total_cnt


def get_page(row_cnt, begin, search_params=None):
    entities, total_cnt = SysUserRoleDaoCK.select_page(row_cnt, begin, search_params)
    #    id_list = [e.sys_user_role_id for e in entities]
    return entities, total_cnt


def full_search(row_cnt, begin, search_str):
    entities, total_cnt = SysUserRoleDaoCK.full_search(row_cnt=row_cnt, row_begin=begin, search_str=search_str)
    #    id_list = [e.sys_user_role_id for e in entities]
    return entities, total_cnt


def update_by_id(sys_user_role_id, update_params):
    entity = SysUserRoleDaoCK.update_by_id(sys_user_role_id, update_params)
    return entity


def get_entity_by_userId(sys_user_id):
    entity = SysUserRoleDaoCK.select_by_SysUserId(sys_user_id)
    return entity
