from domain.sysdomain.entity.SysUserOrgEntity import SysUserOrgEntity
from domain.sysdomain.daock import SysUserOrgDaoCK
from utils import IDUtil

def create(sys_user_id ,sys_org_id ,org_duty_id ,update_time ,create_time ):
    newentity = SysUserOrgEntity(IDUtil.get_long(),sys_user_id ,sys_org_id ,org_duty_id ,update_time ,create_time )
    SysUserOrgDaoCK.insert(newentity)
    return newentity

def delete(sys_user_org_id):
    SysUserOrgDaoCK.delete_by_id(sys_user_org_id)

def update(sys_user_org_id ,sys_user_id ,sys_org_id ,org_duty_id ,update_time ,create_time ):
    newentity = SysUserOrgEntity(sys_user_org_id ,sys_user_id ,sys_org_id ,org_duty_id ,update_time ,create_time )
    SysUserOrgDaoCK.update(newentity)
    return newentity

def get_entity_by_id(sys_user_org_id):
    return SysUserOrgDaoCK.select_by_id(sys_user_org_id)

def get_all():
    return SysUserOrgDaoCK.select_all()

def get_count():
    return SysUserOrgDaoCK.select_count()

def get_vspage(row_cnt, begin, search_params = None):
    entities,total_cnt = SysUserOrgDaoCK.select_vspage(row_cnt, begin,search_params)
#    id_list = [e.sys_user_org_id for e in entities]
    return entities,total_cnt

def get_page(row_cnt, begin, search_params = None):
    entities,total_cnt = SysUserOrgDaoCK.select_page(row_cnt, begin,search_params)
#    id_list = [e.sys_user_org_id for e in entities]
    return entities,total_cnt

def full_search(row_cnt, begin, search_str):
    entities,total_cnt = SysUserOrgDaoCK.full_search(row_cnt=row_cnt, row_begin=begin,search_str=search_str)
#    id_list = [e.sys_user_org_id for e in entities]
    return entities,total_cnt

def update_by_id(sys_user_org_id,update_params):
    entity = SysUserOrgDaoCK.update_by_id(sys_user_org_id,update_params)
    return entity
