from domain.sysdomain.entity.SysDictEntity import SysDictEntity
from domain.sysdomain.daock import SysDictDaoCK
from utils import IDUtil

def create(module_name ,table_name ,column_name ,select_mode ,data_value ,remark ):
    newentity = SysDictEntity(IDUtil.get_long(),module_name ,table_name ,column_name ,select_mode ,data_value ,remark )
    SysDictDaoCK.insert(newentity)
    return newentity

def delete(sys_dict_id):
    SysDictDaoCK.delete_by_id(sys_dict_id)

def update(sys_dict_id ,module_name ,table_name ,column_name ,select_mode ,data_value ,remark ):
    newentity = SysDictEntity(sys_dict_id ,module_name ,table_name ,column_name ,select_mode ,data_value ,remark )
    SysDictDaoCK.update(newentity)
    return newentity

def get_entity_by_id(sys_dict_id):
    return SysDictDaoCK.select_by_id(sys_dict_id)

def get_all():
    return SysDictDaoCK.select_all()

def get_count():
    return SysDictDaoCK.select_count()

def get_vspage(row_cnt, begin, search_params = None):
    entities,total_cnt = SysDictDaoCK.select_vspage(row_cnt, begin,search_params)
#    id_list = [e.sys_dict_id for e in entities]
    return entities,total_cnt

def get_page(row_cnt, begin, search_params = None):
    entities,total_cnt = SysDictDaoCK.select_page(row_cnt, begin,search_params)
#    id_list = [e.sys_dict_id for e in entities]
    return entities,total_cnt

def full_search(row_cnt, begin, search_str):
    entities,total_cnt = SysDictDaoCK.full_search(row_cnt=row_cnt, row_begin=begin,search_str=search_str)
#    id_list = [e.sys_dict_id for e in entities]
    return entities,total_cnt

def update_by_id(sys_dict_id,update_params):
    entity = SysDictDaoCK.update_by_id(sys_dict_id,update_params)
    return entity
