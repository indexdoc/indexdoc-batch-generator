from sysdw import exesql
from utils import IDUtil
from domain.sysdomain.entity.SysMenuEntity import SysMenuEntity

from domain.sysdomain.entity.SysMenuEntity import SysMenuEntity

# sys_menu_id, menu_name, upper_id, order_no, menu_url, menu_icon, open_type, remark
# tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7]

def insert(entity):
    sql = "insert into phy_sys_menu(sys_menu_id, menu_name, upper_id, order_no, menu_url, menu_icon, open_type, remark,ver_id) values"
    exesql(sql, [(entity.sys_menu_id ,entity.menu_name ,entity.upper_id ,entity.order_no ,entity.menu_url ,entity.menu_icon ,entity.open_type ,entity.remark ,IDUtil.get_long())])
    return entity

def delete_by_id(sys_menu_id):
    sql = """insert into phy_sys_menu(sys_menu_id, menu_name, upper_id, order_no, menu_url, menu_icon, open_type, remark,deleted,ver_id) 
        select sys_menu_id, menu_name, upper_id, order_no, menu_url, menu_icon, open_type, remark,1,%d from v_sys_menu 
        where sys_menu_id = %d"""%(IDUtil.get_long(),sys_menu_id)
    exesql(sql)

def delete(entity):
    delete_by_id(entity.sys_menu_id)

def update(entity):
    return insert(entity)

def update_by_id(sys_menu_id,update_params):
    _entity = select_by_id(sys_menu_id)
    if _entity is None:
        return None
    if update_params is None:
        return _entity
    if len(update_params) == 0:
        return _entity
    for param in update_params.keys():
        if hasattr(_entity,param):
            _value = update_params[param]
            setattr(_entity,param,_value)
    return update(_entity)

def full_search(search_str,row_cnt = 50000, row_begin=0, order_by = " order by sys_menu_id desc"):
    if search_str is None or search_str.strip() == '' :
        return None
    _where = "where"
    _limit = " limit %s,%s"%(row_begin,row_cnt)
    attrs = ['sys_menu_id','menu_name','upper_id','order_no','menu_url','menu_icon','open_type','remark']
    for attr in attrs:
        _where += " toString(%s) like '%%%s%%' or"%(attr,search_str)
    _where += " %s like '%%%s%%' or"%("ref_UpperId_SysMenu.2", search_str)
    _where = _where + ' 1!=1'
    _myref_str = ','+SysMenuEntity.get_myref_tables_str() if SysMenuEntity.get_myref_tables_str() != '' else ''
    attrstr = 'sys_menu_id, menu_name, upper_id, order_no, menu_url, menu_icon, open_type, remark' +_myref_str
    sql = "select %s from vs_sys_menu "%attrstr + _where + \
          order_by + _limit
    sql_count = "select count(*) from vs_sys_menu " + _where
    entities = []
    rts = exesql(sql)
    rtscnt = exesql(sql_count)
    total_cnt = int(rtscnt[0][0])
    for tup in rts:
        i = 0
        e = SysMenuEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7])
        i += len(SysMenuEntity.get_attrcodes())
        stup1 = tup[i];i += 1
        if stup1[0] != 0:
            e.ref_UpperId_SysMenu = SysMenuEntity.create_by_tuple(stup1)
        entities.append(e)
    return entities,total_cnt

def select_all(order_by = " order by sys_menu_id desc"):
    entities = []
    sql = "select sys_menu_id, menu_name, upper_id, order_no, menu_url, menu_icon, open_type, remark from v_sys_menu" + order_by
    rts = exesql(sql)
    for tup in rts:
        entities.append(SysMenuEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7]))
    return entities

def select_count():
    sql = "select count(*) from v_sys_menu"
    rts = exesql(sql)
    return int(rts[0][0])

#获取一页数据的同时也返回本表外键的数据
def select_vspage(row_cnt, row_begin, search_params,order_by = " order by sys_menu_id desc"):
    _where = "where"
    attrs = ['sys_menu_id','menu_name','upper_id','order_no','menu_url','menu_icon','open_type','remark']
    if search_params is not None:
        for param in search_params.keys():
            if param in attrs:
                _value = str(search_params[param]).strip()
                if _value != "":
                     _value_splits = _value.split(' - ')
                     if len(_value_splits) == 2:
                         _where += " %s between '%s' and '%s' and"%(param,_value_splits[0],_value_splits[1])
                     else:
                         _where += " %s = '%s' and"%(param,_value)
    _where = _where + ' 1=1'
    _myref_str = ','+SysMenuEntity.get_myref_tables_str() if SysMenuEntity.get_myref_tables_str() != '' else ''
    attrstr = 'sys_menu_id, menu_name, upper_id, order_no, menu_url, menu_icon, open_type, remark' +_myref_str
    sql = "select %s from vs_sys_menu "%attrstr + _where + \
          order_by + " limit %(row_begin)s,%(row_cnt)s"
    sql_count = "select count(*) from v_sys_menu " + _where
    entities = []
    rts = exesql(sql,{'row_cnt':row_cnt,'row_begin':row_begin})
    rtscnt = exesql(sql_count)
    total_cnt = int(rtscnt[0][0])
    for tup in rts:
        i = 0
        e = SysMenuEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7])
        i += len(SysMenuEntity.get_attrcodes())
        stup1 = tup[i];i += 1
        if stup1[0] != 0:
            e.ref_UpperId_SysMenu = SysMenuEntity.create_by_tuple(stup1)
        entities.append(e)
    return entities,total_cnt

def select_page(row_cnt, row_begin, search_params,order_by = " order by sys_menu_id desc"):
    _where = "where"
    attrs = ['sys_menu_id','menu_name','upper_id','order_no','menu_url','menu_icon','open_type','remark']
    if search_params is not None:
        for param in search_params.keys():
            if param in attrs:
                _value = str(search_params[param]).strip()
                if _value != "":
                     _value_splits = _value.split(' - ')
                     if len(_value_splits) == 2:
                         _where += " %s between '%s' and '%s' and"%(param,_value_splits[0],_value_splits[1])
                     else:
                         _where += " %s = '%s' and"%(param,_value)
    _where = _where + ' 1=1'
    sql = "select sys_menu_id, menu_name, upper_id, order_no, menu_url, menu_icon, open_type, remark from v_sys_menu " + _where + \
          order_by + " limit %(row_begin)s,%(row_cnt)s"
    sql_count = "select count(*) from v_sys_menu " + _where
    entities = []
    rts = exesql(sql,{'row_cnt':row_cnt,'row_begin':row_begin})
    rtscnt = exesql(sql_count)
    total_cnt = int(rtscnt[0][0])
    for tup in rts:
        entities.append(SysMenuEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7]))
    return entities,total_cnt

def select_by_id(sys_menu_id):
    sql = "select sys_menu_id, menu_name, upper_id, order_no, menu_url, menu_icon, open_type, remark from  v_sys_menu where sys_menu_id = %(sys_menu_id)s"
    rts = exesql(sql, {'sys_menu_id':sys_menu_id})
    if rts is None or len(rts) == 0:
        return None
    tup = rts[0]
    return SysMenuEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7])

def select_by_SysMenuId(sys_menu_id, order_by = ' order by sys_menu_id desc'):
    entities = []
    sql = "select sys_menu_id, menu_name, upper_id, order_no, menu_url, menu_icon, open_type, remark from v_sys_menu " \
          "where sys_menu_id = %(sys_menu_id)s" + order_by
    rts = exesql(sql, {'sys_menu_id':sys_menu_id})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(SysMenuEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7]))
    return entities
def select_by_MenuName(menu_name, order_by = ' order by sys_menu_id desc'):
    entities = []
    sql = "select sys_menu_id, menu_name, upper_id, order_no, menu_url, menu_icon, open_type, remark from v_sys_menu " \
          "where menu_name = %(menu_name)s" + order_by
    rts = exesql(sql, {'menu_name':menu_name})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(SysMenuEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7]))
    return entities
def select_by_UpperId(upper_id, order_by = ' order by sys_menu_id desc'):
    entities = []
    sql = "select sys_menu_id, menu_name, upper_id, order_no, menu_url, menu_icon, open_type, remark from v_sys_menu " \
          "where upper_id = %(upper_id)s" + order_by
    rts = exesql(sql, {'upper_id':upper_id})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(SysMenuEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7]))
    return entities
def select_by_OrderNo(order_no, order_by = ' order by sys_menu_id desc'):
    entities = []
    sql = "select sys_menu_id, menu_name, upper_id, order_no, menu_url, menu_icon, open_type, remark from v_sys_menu " \
          "where order_no = %(order_no)s" + order_by
    rts = exesql(sql, {'order_no':order_no})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(SysMenuEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7]))
    return entities
def select_by_MenuUrl(menu_url, order_by = ' order by sys_menu_id desc'):
    entities = []
    sql = "select sys_menu_id, menu_name, upper_id, order_no, menu_url, menu_icon, open_type, remark from v_sys_menu " \
          "where menu_url = %(menu_url)s" + order_by
    rts = exesql(sql, {'menu_url':menu_url})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(SysMenuEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7]))
    return entities
def select_by_MenuIcon(menu_icon, order_by = ' order by sys_menu_id desc'):
    entities = []
    sql = "select sys_menu_id, menu_name, upper_id, order_no, menu_url, menu_icon, open_type, remark from v_sys_menu " \
          "where menu_icon = %(menu_icon)s" + order_by
    rts = exesql(sql, {'menu_icon':menu_icon})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(SysMenuEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7]))
    return entities
def select_by_OpenType(open_type, order_by = ' order by sys_menu_id desc'):
    entities = []
    sql = "select sys_menu_id, menu_name, upper_id, order_no, menu_url, menu_icon, open_type, remark from v_sys_menu " \
          "where open_type = %(open_type)s" + order_by
    rts = exesql(sql, {'open_type':open_type})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(SysMenuEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7]))
    return entities
def select_by_Remark(remark, order_by = ' order by sys_menu_id desc'):
    entities = []
    sql = "select sys_menu_id, menu_name, upper_id, order_no, menu_url, menu_icon, open_type, remark from v_sys_menu " \
          "where remark = %(remark)s" + order_by
    rts = exesql(sql, {'remark':remark})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(SysMenuEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7]))
    return entities

def select_by_SysMenuIdList(sys_menu_id_list,order_by = ' order by sys_menu_id desc'):
    _dict = {}
    sql = "select sys_menu_id, menu_name, upper_id, order_no, menu_url, menu_icon, open_type, remark from v_sys_menu" \
          " where sys_menu_id in (%(sys_menu_id_list)s)" + order_by
    rts = exesql(sql, {'sys_menu_id_list':sys_menu_id_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = SysMenuEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7])
        if _dict.get(entity.sys_menu_id) is None:
            _dict[entity.sys_menu_id] = list()
        _dict[entity.sys_menu_id].append(entity)
    return _dict
def select_by_MenuNameList(menu_name_list,order_by = ' order by sys_menu_id desc'):
    _dict = {}
    sql = "select sys_menu_id, menu_name, upper_id, order_no, menu_url, menu_icon, open_type, remark from v_sys_menu" \
          " where menu_name in (%(menu_name_list)s)" + order_by
    rts = exesql(sql, {'menu_name_list':menu_name_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = SysMenuEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7])
        if _dict.get(entity.menu_name) is None:
            _dict[entity.menu_name] = list()
        _dict[entity.menu_name].append(entity)
    return _dict
def select_by_UpperIdList(upper_id_list,order_by = ' order by sys_menu_id desc'):
    _dict = {}
    sql = "select sys_menu_id, menu_name, upper_id, order_no, menu_url, menu_icon, open_type, remark from v_sys_menu" \
          " where upper_id in (%(upper_id_list)s)" + order_by
    rts = exesql(sql, {'upper_id_list':upper_id_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = SysMenuEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7])
        if _dict.get(entity.upper_id) is None:
            _dict[entity.upper_id] = list()
        _dict[entity.upper_id].append(entity)
    return _dict
def select_by_OrderNoList(order_no_list,order_by = ' order by sys_menu_id desc'):
    _dict = {}
    sql = "select sys_menu_id, menu_name, upper_id, order_no, menu_url, menu_icon, open_type, remark from v_sys_menu" \
          " where order_no in (%(order_no_list)s)" + order_by
    rts = exesql(sql, {'order_no_list':order_no_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = SysMenuEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7])
        if _dict.get(entity.order_no) is None:
            _dict[entity.order_no] = list()
        _dict[entity.order_no].append(entity)
    return _dict
def select_by_MenuUrlList(menu_url_list,order_by = ' order by sys_menu_id desc'):
    _dict = {}
    sql = "select sys_menu_id, menu_name, upper_id, order_no, menu_url, menu_icon, open_type, remark from v_sys_menu" \
          " where menu_url in (%(menu_url_list)s)" + order_by
    rts = exesql(sql, {'menu_url_list':menu_url_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = SysMenuEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7])
        if _dict.get(entity.menu_url) is None:
            _dict[entity.menu_url] = list()
        _dict[entity.menu_url].append(entity)
    return _dict
def select_by_MenuIconList(menu_icon_list,order_by = ' order by sys_menu_id desc'):
    _dict = {}
    sql = "select sys_menu_id, menu_name, upper_id, order_no, menu_url, menu_icon, open_type, remark from v_sys_menu" \
          " where menu_icon in (%(menu_icon_list)s)" + order_by
    rts = exesql(sql, {'menu_icon_list':menu_icon_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = SysMenuEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7])
        if _dict.get(entity.menu_icon) is None:
            _dict[entity.menu_icon] = list()
        _dict[entity.menu_icon].append(entity)
    return _dict
def select_by_OpenTypeList(open_type_list,order_by = ' order by sys_menu_id desc'):
    _dict = {}
    sql = "select sys_menu_id, menu_name, upper_id, order_no, menu_url, menu_icon, open_type, remark from v_sys_menu" \
          " where open_type in (%(open_type_list)s)" + order_by
    rts = exesql(sql, {'open_type_list':open_type_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = SysMenuEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7])
        if _dict.get(entity.open_type) is None:
            _dict[entity.open_type] = list()
        _dict[entity.open_type].append(entity)
    return _dict
def select_by_RemarkList(remark_list,order_by = ' order by sys_menu_id desc'):
    _dict = {}
    sql = "select sys_menu_id, menu_name, upper_id, order_no, menu_url, menu_icon, open_type, remark from v_sys_menu" \
          " where remark in (%(remark_list)s)" + order_by
    rts = exesql(sql, {'remark_list':remark_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = SysMenuEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7])
        if _dict.get(entity.remark) is None:
            _dict[entity.remark] = list()
        _dict[entity.remark].append(entity)
    return _dict

