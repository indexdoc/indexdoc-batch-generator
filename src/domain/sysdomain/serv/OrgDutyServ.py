from domain.sysdomain.entity.OrgDutyEntity import OrgDutyEntity
from domain.sysdomain.daock import OrgDutyDaoCK
from utils import IDUtil

def create(sys_org_id ,org_duty_name ,update_time ,create_time ):
    newentity = OrgDutyEntity(IDUtil.get_long(),sys_org_id ,org_duty_name ,update_time ,create_time )
    OrgDutyDaoCK.insert(newentity)
    return newentity

def delete(org_duty_id):
    OrgDutyDaoCK.delete_by_id(org_duty_id)

def update(org_duty_id ,sys_org_id ,org_duty_name ,update_time ,create_time ):
    newentity = OrgDutyEntity(org_duty_id ,sys_org_id ,org_duty_name ,update_time ,create_time )
    OrgDutyDaoCK.update(newentity)
    return newentity

def get_entity_by_id(org_duty_id):
    return OrgDutyDaoCK.select_by_id(org_duty_id)

def get_all():
    return OrgDutyDaoCK.select_all()

def get_count():
    return OrgDutyDaoCK.select_count()

def get_vspage(row_cnt, begin, search_params = None):
    entities,total_cnt = OrgDutyDaoCK.select_vspage(row_cnt, begin,search_params)
#    id_list = [e.org_duty_id for e in entities]
    return entities,total_cnt

def get_page(row_cnt, begin, search_params = None):
    entities,total_cnt = OrgDutyDaoCK.select_page(row_cnt, begin,search_params)
#    id_list = [e.org_duty_id for e in entities]
    return entities,total_cnt

def full_search(row_cnt, begin, search_str):
    entities,total_cnt = OrgDutyDaoCK.full_search(row_cnt=row_cnt, row_begin=begin,search_str=search_str)
#    id_list = [e.org_duty_id for e in entities]
    return entities,total_cnt

def update_by_id(org_duty_id,update_params):
    entity = OrgDutyDaoCK.update_by_id(org_duty_id,update_params)
    return entity
