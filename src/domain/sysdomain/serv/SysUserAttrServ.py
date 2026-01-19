from domain.sysdomain.entity.SysUserAttrEntity import SysUserAttrEntity
from domain.sysdomain.daock import SysUserAttrDaoCK
from utils import IDUtil

def create(sys_user_id ,attr_name ,attr_value ,create_time ,update_time ):
    newentity = SysUserAttrEntity(IDUtil.get_long(),sys_user_id ,attr_name ,attr_value ,create_time ,update_time )
    SysUserAttrDaoCK.insert(newentity)
    return newentity

def delete(sys_user_attr_id):
    SysUserAttrDaoCK.delete_by_id(sys_user_attr_id)

def update(sys_user_attr_id ,sys_user_id ,attr_name ,attr_value ,create_time ,update_time ):
    newentity = SysUserAttrEntity(sys_user_attr_id ,sys_user_id ,attr_name ,attr_value ,create_time ,update_time )
    SysUserAttrDaoCK.update(newentity)
    return newentity

def get_entity_by_id(sys_user_attr_id):
    return SysUserAttrDaoCK.select_by_id(sys_user_attr_id)

def get_all():
    return SysUserAttrDaoCK.select_all()

def get_count():
    return SysUserAttrDaoCK.select_count()

def get_vspage(row_cnt, begin, search_params = None):
    entities,total_cnt = SysUserAttrDaoCK.select_vspage(row_cnt, begin,search_params)
#    id_list = [e.sys_user_attr_id for e in entities]
    return entities,total_cnt

def get_page(row_cnt, begin, search_params = None):
    entities,total_cnt = SysUserAttrDaoCK.select_page(row_cnt, begin,search_params)
#    id_list = [e.sys_user_attr_id for e in entities]
    return entities,total_cnt

def full_search(row_cnt, begin, search_str):
    entities,total_cnt = SysUserAttrDaoCK.full_search(row_cnt=row_cnt, row_begin=begin,search_str=search_str)
#    id_list = [e.sys_user_attr_id for e in entities]
    return entities,total_cnt

def update_by_id(sys_user_attr_id,update_params):
    entity = SysUserAttrDaoCK.update_by_id(sys_user_attr_id,update_params)
    return entity
