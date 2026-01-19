from sysdw import exesql
from utils import IDUtil
from domain.sysdomain.entity.SysUserAttrEntity import SysUserAttrEntity

from domain.sysdomain.entity.SysUserEntity import SysUserEntity

# sys_user_attr_id, sys_user_id, attr_name, attr_value, create_time, update_time
# tup[0], tup[1], tup[2], tup[3], tup[4], tup[5]

def insert(entity):
    sql = "insert into phy_sys_user_attr(sys_user_attr_id, sys_user_id, attr_name, attr_value, create_time, update_time,ver_id) values"
    exesql(sql, [(entity.sys_user_attr_id ,entity.sys_user_id ,entity.attr_name ,entity.attr_value ,entity.create_time ,entity.update_time ,IDUtil.get_long())])
    return entity

def delete_by_id(sys_user_attr_id):
    sql = """insert into phy_sys_user_attr(sys_user_attr_id, sys_user_id, attr_name, attr_value, create_time, update_time,deleted,ver_id) 
        select sys_user_attr_id, sys_user_id, attr_name, attr_value, create_time, update_time,1,%d from v_sys_user_attr 
        where sys_user_attr_id = %d"""%(IDUtil.get_long(),sys_user_attr_id)
    exesql(sql)

def delete(entity):
    delete_by_id(entity.sys_user_attr_id)

def update(entity):
    return insert(entity)

def update_by_id(sys_user_attr_id,update_params):
    _entity = select_by_id(sys_user_attr_id)
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

def full_search(search_str,row_cnt = 50000, row_begin=0, order_by = " order by sys_user_attr_id desc"):
    if search_str is None or search_str.strip() == '' :
        return None
    _where = "where"
    _limit = " limit %s,%s"%(row_begin,row_cnt)
    attrs = ['sys_user_attr_id','sys_user_id','attr_name','attr_value','create_time','update_time']
    for attr in attrs:
        _where += " toString(%s) like '%%%s%%' or"%(attr,search_str)
    _where += " %s like '%%%s%%' or"%("ref_SysUserId_SysUser.2", search_str)
    _where = _where + ' 1!=1'
    _myref_str = ','+SysUserAttrEntity.get_myref_tables_str() if SysUserAttrEntity.get_myref_tables_str() != '' else ''
    attrstr = 'sys_user_attr_id, sys_user_id, attr_name, attr_value, create_time, update_time' +_myref_str
    sql = "select %s from vs_sys_user_attr "%attrstr + _where + \
          order_by + _limit
    sql_count = "select count(*) from vs_sys_user_attr " + _where
    entities = []
    rts = exesql(sql)
    rtscnt = exesql(sql_count)
    total_cnt = int(rtscnt[0][0])
    for tup in rts:
        i = 0
        e = SysUserAttrEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5])
        i += len(SysUserAttrEntity.get_attrcodes())
        stup1 = tup[i];i += 1
        if stup1[0] != 0:
            e.ref_SysUserId_SysUser = SysUserEntity.create_by_tuple(stup1)
        entities.append(e)
    return entities,total_cnt

def select_all(order_by = " order by sys_user_attr_id desc"):
    entities = []
    sql = "select sys_user_attr_id, sys_user_id, attr_name, attr_value, create_time, update_time from v_sys_user_attr" + order_by
    rts = exesql(sql)
    for tup in rts:
        entities.append(SysUserAttrEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5]))
    return entities

def select_count():
    sql = "select count(*) from v_sys_user_attr"
    rts = exesql(sql)
    return int(rts[0][0])

#获取一页数据的同时也返回本表外键的数据
def select_vspage(row_cnt, row_begin, search_params,order_by = " order by sys_user_attr_id desc"):
    _where = "where"
    attrs = ['sys_user_attr_id','sys_user_id','attr_name','attr_value','create_time','update_time']
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
    _myref_str = ','+SysUserAttrEntity.get_myref_tables_str() if SysUserAttrEntity.get_myref_tables_str() != '' else ''
    attrstr = 'sys_user_attr_id, sys_user_id, attr_name, attr_value, create_time, update_time' +_myref_str
    sql = "select %s from vs_sys_user_attr "%attrstr + _where + \
          order_by + " limit %(row_begin)s,%(row_cnt)s"
    sql_count = "select count(*) from v_sys_user_attr " + _where
    entities = []
    rts = exesql(sql,{'row_cnt':row_cnt,'row_begin':row_begin})
    rtscnt = exesql(sql_count)
    total_cnt = int(rtscnt[0][0])
    for tup in rts:
        i = 0
        e = SysUserAttrEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5])
        i += len(SysUserAttrEntity.get_attrcodes())
        stup1 = tup[i];i += 1
        if stup1[0] != 0:
            e.ref_SysUserId_SysUser = SysUserEntity.create_by_tuple(stup1)
        entities.append(e)
    return entities,total_cnt

def select_page(row_cnt, row_begin, search_params,order_by = " order by sys_user_attr_id desc"):
    _where = "where"
    attrs = ['sys_user_attr_id','sys_user_id','attr_name','attr_value','create_time','update_time']
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
    sql = "select sys_user_attr_id, sys_user_id, attr_name, attr_value, create_time, update_time from v_sys_user_attr " + _where + \
          order_by + " limit %(row_begin)s,%(row_cnt)s"
    sql_count = "select count(*) from v_sys_user_attr " + _where
    entities = []
    rts = exesql(sql,{'row_cnt':row_cnt,'row_begin':row_begin})
    rtscnt = exesql(sql_count)
    total_cnt = int(rtscnt[0][0])
    for tup in rts:
        entities.append(SysUserAttrEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5]))
    return entities,total_cnt

def select_by_id(sys_user_attr_id):
    sql = "select sys_user_attr_id, sys_user_id, attr_name, attr_value, create_time, update_time from  v_sys_user_attr where sys_user_attr_id = %(sys_user_attr_id)s"
    rts = exesql(sql, {'sys_user_attr_id':sys_user_attr_id})
    if rts is None or len(rts) == 0:
        return None
    tup = rts[0]
    return SysUserAttrEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5])

def select_by_SysUserAttrId(sys_user_attr_id, order_by = ' order by sys_user_attr_id desc'):
    entities = []
    sql = "select sys_user_attr_id, sys_user_id, attr_name, attr_value, create_time, update_time from v_sys_user_attr " \
          "where sys_user_attr_id = %(sys_user_attr_id)s" + order_by
    rts = exesql(sql, {'sys_user_attr_id':sys_user_attr_id})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(SysUserAttrEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5]))
    return entities
def select_by_SysUserId(sys_user_id, order_by = ' order by sys_user_attr_id desc'):
    entities = []
    sql = "select sys_user_attr_id, sys_user_id, attr_name, attr_value, create_time, update_time from v_sys_user_attr " \
          "where sys_user_id = %(sys_user_id)s" + order_by
    rts = exesql(sql, {'sys_user_id':sys_user_id})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(SysUserAttrEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5]))
    return entities
def select_by_AttrName(attr_name, order_by = ' order by sys_user_attr_id desc'):
    entities = []
    sql = "select sys_user_attr_id, sys_user_id, attr_name, attr_value, create_time, update_time from v_sys_user_attr " \
          "where attr_name = %(attr_name)s" + order_by
    rts = exesql(sql, {'attr_name':attr_name})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(SysUserAttrEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5]))
    return entities
def select_by_AttrValue(attr_value, order_by = ' order by sys_user_attr_id desc'):
    entities = []
    sql = "select sys_user_attr_id, sys_user_id, attr_name, attr_value, create_time, update_time from v_sys_user_attr " \
          "where attr_value = %(attr_value)s" + order_by
    rts = exesql(sql, {'attr_value':attr_value})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(SysUserAttrEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5]))
    return entities
def select_by_CreateTime(create_time, order_by = ' order by sys_user_attr_id desc'):
    entities = []
    sql = "select sys_user_attr_id, sys_user_id, attr_name, attr_value, create_time, update_time from v_sys_user_attr " \
          "where create_time = %(create_time)s" + order_by
    rts = exesql(sql, {'create_time':create_time})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(SysUserAttrEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5]))
    return entities
def select_by_UpdateTime(update_time, order_by = ' order by sys_user_attr_id desc'):
    entities = []
    sql = "select sys_user_attr_id, sys_user_id, attr_name, attr_value, create_time, update_time from v_sys_user_attr " \
          "where update_time = %(update_time)s" + order_by
    rts = exesql(sql, {'update_time':update_time})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(SysUserAttrEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5]))
    return entities

def select_by_SysUserAttrIdList(sys_user_attr_id_list,order_by = ' order by sys_user_attr_id desc'):
    _dict = {}
    sql = "select sys_user_attr_id, sys_user_id, attr_name, attr_value, create_time, update_time from v_sys_user_attr" \
          " where sys_user_attr_id in (%(sys_user_attr_id_list)s)" + order_by
    rts = exesql(sql, {'sys_user_attr_id_list':sys_user_attr_id_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = SysUserAttrEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5])
        if _dict.get(entity.sys_user_attr_id) is None:
            _dict[entity.sys_user_attr_id] = list()
        _dict[entity.sys_user_attr_id].append(entity)
    return _dict
def select_by_SysUserIdList(sys_user_id_list,order_by = ' order by sys_user_attr_id desc'):
    _dict = {}
    sql = "select sys_user_attr_id, sys_user_id, attr_name, attr_value, create_time, update_time from v_sys_user_attr" \
          " where sys_user_id in (%(sys_user_id_list)s)" + order_by
    rts = exesql(sql, {'sys_user_id_list':sys_user_id_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = SysUserAttrEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5])
        if _dict.get(entity.sys_user_id) is None:
            _dict[entity.sys_user_id] = list()
        _dict[entity.sys_user_id].append(entity)
    return _dict
def select_by_AttrNameList(attr_name_list,order_by = ' order by sys_user_attr_id desc'):
    _dict = {}
    sql = "select sys_user_attr_id, sys_user_id, attr_name, attr_value, create_time, update_time from v_sys_user_attr" \
          " where attr_name in (%(attr_name_list)s)" + order_by
    rts = exesql(sql, {'attr_name_list':attr_name_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = SysUserAttrEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5])
        if _dict.get(entity.attr_name) is None:
            _dict[entity.attr_name] = list()
        _dict[entity.attr_name].append(entity)
    return _dict
def select_by_AttrValueList(attr_value_list,order_by = ' order by sys_user_attr_id desc'):
    _dict = {}
    sql = "select sys_user_attr_id, sys_user_id, attr_name, attr_value, create_time, update_time from v_sys_user_attr" \
          " where attr_value in (%(attr_value_list)s)" + order_by
    rts = exesql(sql, {'attr_value_list':attr_value_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = SysUserAttrEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5])
        if _dict.get(entity.attr_value) is None:
            _dict[entity.attr_value] = list()
        _dict[entity.attr_value].append(entity)
    return _dict
def select_by_CreateTimeList(create_time_list,order_by = ' order by sys_user_attr_id desc'):
    _dict = {}
    sql = "select sys_user_attr_id, sys_user_id, attr_name, attr_value, create_time, update_time from v_sys_user_attr" \
          " where create_time in (%(create_time_list)s)" + order_by
    rts = exesql(sql, {'create_time_list':create_time_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = SysUserAttrEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5])
        if _dict.get(entity.create_time) is None:
            _dict[entity.create_time] = list()
        _dict[entity.create_time].append(entity)
    return _dict
def select_by_UpdateTimeList(update_time_list,order_by = ' order by sys_user_attr_id desc'):
    _dict = {}
    sql = "select sys_user_attr_id, sys_user_id, attr_name, attr_value, create_time, update_time from v_sys_user_attr" \
          " where update_time in (%(update_time_list)s)" + order_by
    rts = exesql(sql, {'update_time_list':update_time_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = SysUserAttrEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5])
        if _dict.get(entity.update_time) is None:
            _dict[entity.update_time] = list()
        _dict[entity.update_time].append(entity)
    return _dict

