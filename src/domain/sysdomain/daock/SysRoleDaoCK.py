from sysdw import exesql
from utils import IDUtil
from domain.sysdomain.entity.SysRoleEntity import SysRoleEntity


# sys_role_id, role_name
# tup[0], tup[1]

def insert(entity):
    sql = "insert into phy_sys_role(sys_role_id, role_name,ver_id) values"
    exesql(sql, [(entity.sys_role_id ,entity.role_name ,IDUtil.get_long())])
    return entity

def delete_by_id(sys_role_id):
    sql = """insert into phy_sys_role(sys_role_id, role_name,deleted,ver_id) 
        select sys_role_id, role_name,1,%d from v_sys_role 
        where sys_role_id = %d"""%(IDUtil.get_long(),sys_role_id)
    exesql(sql)

def delete(entity):
    delete_by_id(entity.sys_role_id)

def update(entity):
    return insert(entity)

def update_by_id(sys_role_id,update_params):
    _entity = select_by_id(sys_role_id)
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

def full_search(search_str,row_cnt = 50000, row_begin=0, order_by = " order by sys_role_id desc"):
    if search_str is None or search_str.strip() == '' :
        return None
    _where = "where"
    _limit = " limit %s,%s"%(row_begin,row_cnt)
    attrs = ['sys_role_id','role_name']
    for attr in attrs:
        _where += " toString(%s) like '%%%s%%' or"%(attr,search_str)
    _where = _where + ' 1!=1'
    _myref_str = ','+SysRoleEntity.get_myref_tables_str() if SysRoleEntity.get_myref_tables_str() != '' else ''
    attrstr = 'sys_role_id, role_name' +_myref_str
    sql = "select %s from vs_sys_role "%attrstr + _where + \
          order_by + _limit
    sql_count = "select count(*) from vs_sys_role " + _where
    entities = []
    rts = exesql(sql)
    rtscnt = exesql(sql_count)
    total_cnt = int(rtscnt[0][0])
    for tup in rts:
        i = 0
        e = SysRoleEntity(tup[0], tup[1])
        i += len(SysRoleEntity.get_attrcodes())
        entities.append(e)
    return entities,total_cnt

def select_all(order_by = " order by sys_role_id desc"):
    entities = []
    sql = "select sys_role_id, role_name from v_sys_role" + order_by
    rts = exesql(sql)
    for tup in rts:
        entities.append(SysRoleEntity(tup[0], tup[1]))
    return entities

def select_count():
    sql = "select count(*) from v_sys_role"
    rts = exesql(sql)
    return int(rts[0][0])

#获取一页数据的同时也返回本表外键的数据
def select_vspage(row_cnt, row_begin, search_params,order_by = " order by sys_role_id desc"):
    _where = "where"
    attrs = ['sys_role_id','role_name']
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
    _myref_str = ','+SysRoleEntity.get_myref_tables_str() if SysRoleEntity.get_myref_tables_str() != '' else ''
    attrstr = 'sys_role_id, role_name' +_myref_str
    sql = "select %s from vs_sys_role "%attrstr + _where + \
          order_by + " limit %(row_begin)s,%(row_cnt)s"
    sql_count = "select count(*) from v_sys_role " + _where
    entities = []
    rts = exesql(sql,{'row_cnt':row_cnt,'row_begin':row_begin})
    rtscnt = exesql(sql_count)
    total_cnt = int(rtscnt[0][0])
    for tup in rts:
        i = 0
        e = SysRoleEntity(tup[0], tup[1])
        i += len(SysRoleEntity.get_attrcodes())
        entities.append(e)
    return entities,total_cnt

def select_page(row_cnt, row_begin, search_params,order_by = " order by sys_role_id desc"):
    _where = "where"
    attrs = ['sys_role_id','role_name']
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
    sql = "select sys_role_id, role_name from v_sys_role " + _where + \
          order_by + " limit %(row_begin)s,%(row_cnt)s"
    sql_count = "select count(*) from v_sys_role " + _where
    entities = []
    rts = exesql(sql,{'row_cnt':row_cnt,'row_begin':row_begin})
    rtscnt = exesql(sql_count)
    total_cnt = int(rtscnt[0][0])
    for tup in rts:
        entities.append(SysRoleEntity(tup[0], tup[1]))
    return entities,total_cnt

def select_by_id(sys_role_id):
    sql = "select sys_role_id, role_name from  v_sys_role where sys_role_id = %(sys_role_id)s"
    rts = exesql(sql, {'sys_role_id':sys_role_id})
    if rts is None or len(rts) == 0:
        return None
    tup = rts[0]
    return SysRoleEntity(tup[0], tup[1])

def select_by_SysRoleId(sys_role_id, order_by = ' order by sys_role_id desc'):
    entities = []
    sql = "select sys_role_id, role_name from v_sys_role " \
          "where sys_role_id = %(sys_role_id)s" + order_by
    rts = exesql(sql, {'sys_role_id':sys_role_id})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(SysRoleEntity(tup[0], tup[1]))
    return entities
def select_by_RoleName(role_name, order_by = ' order by sys_role_id desc'):
    entities = []
    sql = "select sys_role_id, role_name from v_sys_role " \
          "where role_name = %(role_name)s" + order_by
    rts = exesql(sql, {'role_name':role_name})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(SysRoleEntity(tup[0], tup[1]))
    return entities

def select_by_SysRoleIdList(sys_role_id_list,order_by = ' order by sys_role_id desc'):
    _dict = {}
    sql = "select sys_role_id, role_name from v_sys_role" \
          " where sys_role_id in (%(sys_role_id_list)s)" + order_by
    rts = exesql(sql, {'sys_role_id_list':sys_role_id_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = SysRoleEntity(tup[0], tup[1])
        if _dict.get(entity.sys_role_id) is None:
            _dict[entity.sys_role_id] = list()
        _dict[entity.sys_role_id].append(entity)
    return _dict
def select_by_RoleNameList(role_name_list,order_by = ' order by sys_role_id desc'):
    _dict = {}
    sql = "select sys_role_id, role_name from v_sys_role" \
          " where role_name in (%(role_name_list)s)" + order_by
    rts = exesql(sql, {'role_name_list':role_name_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = SysRoleEntity(tup[0], tup[1])
        if _dict.get(entity.role_name) is None:
            _dict[entity.role_name] = list()
        _dict[entity.role_name].append(entity)
    return _dict

