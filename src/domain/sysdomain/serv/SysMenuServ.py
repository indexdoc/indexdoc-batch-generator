from domain.sysdomain.entity.SysMenuEntity import SysMenuEntity
from domain.sysdomain.daock import SysMenuDaoCK
from utils import IDUtil

def create(menu_name ,upper_id ,order_no ,menu_url ,menu_icon ,open_type ,remark ):
    newentity = SysMenuEntity(IDUtil.get_long(),menu_name ,upper_id ,order_no ,menu_url ,menu_icon ,open_type ,remark )
    SysMenuDaoCK.insert(newentity)
    return newentity

def delete(sys_menu_id):
    SysMenuDaoCK.delete_by_id(sys_menu_id)

def update(sys_menu_id ,menu_name ,upper_id ,order_no ,menu_url ,menu_icon ,open_type ,remark ):
    newentity = SysMenuEntity(sys_menu_id ,menu_name ,upper_id ,order_no ,menu_url ,menu_icon ,open_type ,remark )
    SysMenuDaoCK.update(newentity)
    return newentity

def get_entity_by_id(sys_menu_id):
    return SysMenuDaoCK.select_by_id(sys_menu_id)

def get_all():
    return SysMenuDaoCK.select_all()

def get_count():
    return SysMenuDaoCK.select_count()

def get_vspage(row_cnt, begin, search_params = None):
    entities,total_cnt = SysMenuDaoCK.select_vspage(row_cnt, begin,search_params)
#    id_list = [e.sys_menu_id for e in entities]
    return entities,total_cnt

def get_page(row_cnt, begin, search_params = None):
    entities,total_cnt = SysMenuDaoCK.select_page(row_cnt, begin,search_params)
#    id_list = [e.sys_menu_id for e in entities]
    return entities,total_cnt

def full_search(row_cnt, begin, search_str):
    entities,total_cnt = SysMenuDaoCK.full_search(row_cnt=row_cnt, row_begin=begin,search_str=search_str)
#    id_list = [e.sys_menu_id for e in entities]
    return entities,total_cnt

def update_by_id(sys_menu_id,update_params):
    entity = SysMenuDaoCK.update_by_id(sys_menu_id,update_params)
    return entity
