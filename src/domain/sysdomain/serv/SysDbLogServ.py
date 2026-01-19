from domain.sysdomain.entity.SysDbLogEntity import SysDbLogEntity
from domain.sysdomain.daock import SysDbLogDaoCK
from utils import IDUtil

def create(sys_user_id ,op_datetime ,op_duration ,op_type ,table_code ,data_id ,sql_str ,sql_param ,sql_result ):
    newentity = SysDbLogEntity(IDUtil.get_long(),sys_user_id ,op_datetime ,op_duration ,op_type ,table_code ,data_id ,sql_str ,sql_param ,sql_result )
    SysDbLogDaoCK.insert(newentity)
    return newentity

def delete(sys_db_log_id):
    SysDbLogDaoCK.delete_by_id(sys_db_log_id)

def update(sys_db_log_id ,sys_user_id ,op_datetime ,op_duration ,op_type ,table_code ,data_id ,sql_str ,sql_param ,sql_result ):
    newentity = SysDbLogEntity(sys_db_log_id ,sys_user_id ,op_datetime ,op_duration ,op_type ,table_code ,data_id ,sql_str ,sql_param ,sql_result )
    SysDbLogDaoCK.update(newentity)
    return newentity

def get_entity_by_id(sys_db_log_id):
    return SysDbLogDaoCK.select_by_id(sys_db_log_id)

def get_all():
    return SysDbLogDaoCK.select_all()

def get_count():
    return SysDbLogDaoCK.select_count()

def get_vspage(row_cnt, begin, search_params = None):
    entities,total_cnt = SysDbLogDaoCK.select_vspage(row_cnt, begin,search_params)
#    id_list = [e.sys_db_log_id for e in entities]
    return entities,total_cnt

def get_page(row_cnt, begin, search_params = None):
    entities,total_cnt = SysDbLogDaoCK.select_page(row_cnt, begin,search_params)
#    id_list = [e.sys_db_log_id for e in entities]
    return entities,total_cnt

def full_search(row_cnt, begin, search_str):
    entities,total_cnt = SysDbLogDaoCK.full_search(row_cnt=row_cnt, row_begin=begin,search_str=search_str)
#    id_list = [e.sys_db_log_id for e in entities]
    return entities,total_cnt

def update_by_id(sys_db_log_id,update_params):
    entity = SysDbLogDaoCK.update_by_id(sys_db_log_id,update_params)
    return entity
