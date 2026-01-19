from domain.sysdomain.entity.SysOrgEntity import SysOrgEntity
from domain.sysdomain.daock import SysOrgDaoCK
from utils import IDUtil

def create(org_name ,upper_id ,sort_no ,create_time ,update_time ):
    newentity = SysOrgEntity(IDUtil.get_long(),org_name ,upper_id ,sort_no ,create_time ,update_time )
    SysOrgDaoCK.insert(newentity)
    return newentity

def delete(sys_org_id):
    SysOrgDaoCK.delete_by_id(sys_org_id)

def update(sys_org_id ,org_name ,upper_id ,sort_no ,create_time ,update_time ):
    newentity = SysOrgEntity(sys_org_id ,org_name ,upper_id ,sort_no ,create_time ,update_time )
    SysOrgDaoCK.update(newentity)
    return newentity

def get_entity_by_id(sys_org_id):
    return SysOrgDaoCK.select_by_id(sys_org_id)

def get_all():
    return SysOrgDaoCK.select_all()

def get_count():
    return SysOrgDaoCK.select_count()

def get_vspage(row_cnt, begin, search_params = None):
    entities,total_cnt = SysOrgDaoCK.select_vspage(row_cnt, begin,search_params)
#    id_list = [e.sys_org_id for e in entities]
    return entities,total_cnt

def get_page(row_cnt, begin, search_params = None):
    entities,total_cnt = SysOrgDaoCK.select_page(row_cnt, begin,search_params)
#    id_list = [e.sys_org_id for e in entities]
    return entities,total_cnt

def full_search(row_cnt, begin, search_str):
    entities,total_cnt = SysOrgDaoCK.full_search(row_cnt=row_cnt, row_begin=begin,search_str=search_str)
#    id_list = [e.sys_org_id for e in entities]
    return entities,total_cnt

def update_by_id(sys_org_id,update_params):
    entity = SysOrgDaoCK.update_by_id(sys_org_id,update_params)
    return entity
