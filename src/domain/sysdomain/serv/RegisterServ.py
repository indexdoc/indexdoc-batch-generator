from domain.sysdomain.entity.RegisterEntity import RegisterEntity
from domain.sysdomain.daock import RegisterDaoCK
from utils import IDUtil

def create(sys_user_id ,phone_no ,name ,user_name ,company_name ,pwd ,status ,create_time ,update_time ,remark ):
    newentity = RegisterEntity(IDUtil.get_long(),sys_user_id ,phone_no ,name ,user_name ,company_name ,pwd ,status ,create_time ,update_time ,remark )
    RegisterDaoCK.insert(newentity)
    return newentity

def delete(register_id):
    RegisterDaoCK.delete_by_id(register_id)

def update(register_id ,sys_user_id ,phone_no ,name ,user_name ,company_name ,pwd ,status ,create_time ,update_time ,remark ):
    newentity = RegisterEntity(register_id ,sys_user_id ,phone_no ,name ,user_name ,company_name ,pwd ,status ,create_time ,update_time ,remark )
    RegisterDaoCK.update(newentity)
    return newentity

def get_entity_by_id(register_id):
    return RegisterDaoCK.select_by_id(register_id)

def get_all():
    return RegisterDaoCK.select_all()

def get_count():
    return RegisterDaoCK.select_count()

def get_vspage(row_cnt, begin, search_params = None):
    entities,total_cnt = RegisterDaoCK.select_vspage(row_cnt, begin,search_params)
#    id_list = [e.register_id for e in entities]
    return entities,total_cnt

def get_page(row_cnt, begin, search_params = None):
    entities,total_cnt = RegisterDaoCK.select_page(row_cnt, begin,search_params)
#    id_list = [e.register_id for e in entities]
    return entities,total_cnt

def full_search(row_cnt, begin, search_str):
    entities,total_cnt = RegisterDaoCK.full_search(row_cnt=row_cnt, row_begin=begin,search_str=search_str)
#    id_list = [e.register_id for e in entities]
    return entities,total_cnt

def update_by_id(register_id,update_params):
    entity = RegisterDaoCK.update_by_id(register_id,update_params)
    return entity
