from sysdw import exesql
from utils import IDUtil
from domain.sysdomain.entity.SysOrgEntity import SysOrgEntity

from domain.sysdomain.entity.SysOrgEntity import SysOrgEntity

# sys_org_id, org_name, upper_id, sort_no, create_time, update_time
# tup[0], tup[1], tup[2], tup[3], tup[4], tup[5]

def insert(entity):
    sql = "insert into phy_sys_org(sys_org_id, org_name, upper_id, sort_no, create_time, update_time,ver_id) values"
    exesql(sql, [(entity.sys_org_id ,entity.org_name ,entity.upper_id ,entity.sort_no ,entity.create_time ,entity.update_time ,IDUtil.get_long())])
    return entity

def delete_by_id(sys_org_id):
    sql = """insert into phy_sys_org(sys_org_id, org_name, upper_id, sort_no, create_time, update_time,deleted,ver_id) 
        select sys_org_id, org_name, upper_id, sort_no, create_time, update_time,1,%d from v_sys_org 
        where sys_org_id = %d"""%(IDUtil.get_long(),sys_org_id)
    exesql(sql)

def delete(entity):
    delete_by_id(entity.sys_org_id)

def update(entity):
    return insert(entity)

def update_by_id(sys_org_id,update_params):
    _entity = select_by_id(sys_org_id)
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

def full_search(search_str,row_cnt = 50000, row_begin=0, order_by = " order by sys_org_id desc"):
    if search_str is None or search_str.strip() == '' :
        return None
    _where = "where"
    _limit = " limit %s,%s"%(row_begin,row_cnt)
    attrs = ['sys_org_id','org_name','upper_id','sort_no','create_time','update_time']
    for attr in attrs:
        _where += " toString(%s) like '%%%s%%' or"%(attr,search_str)
    _where += " %s like '%%%s%%' or"%("ref_UpperId_SysOrg.2", search_str)
    _where = _where + ' 1!=1'
    _myref_str = ','+SysOrgEntity.get_myref_tables_str() if SysOrgEntity.get_myref_tables_str() != '' else ''
    attrstr = 'sys_org_id, org_name, upper_id, sort_no, create_time, update_time' +_myref_str
    sql = "select %s from vs_sys_org "%attrstr + _where + \
          order_by + _limit
    sql_count = "select count(*) from vs_sys_org " + _where
    entities = []
    rts = exesql(sql)
    rtscnt = exesql(sql_count)
    total_cnt = int(rtscnt[0][0])
    for tup in rts:
        i = 0
        e = SysOrgEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5])
        i += len(SysOrgEntity.get_attrcodes())
        stup1 = tup[i];i += 1
        if stup1[0] != 0:
            e.ref_UpperId_SysOrg = SysOrgEntity.create_by_tuple(stup1)
        entities.append(e)
    return entities,total_cnt

def select_all(order_by = " order by sys_org_id desc"):
    entities = []
    sql = "select sys_org_id, org_name, upper_id, sort_no, create_time, update_time from v_sys_org" + order_by
    rts = exesql(sql)
    for tup in rts:
        entities.append(SysOrgEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5]))
    return entities

def select_count():
    sql = "select count(*) from v_sys_org"
    rts = exesql(sql)
    return int(rts[0][0])

#获取一页数据的同时也返回本表外键的数据
def select_vspage(row_cnt, row_begin, search_params,order_by = " order by sys_org_id desc"):
    _where = "where"
    attrs = ['sys_org_id','org_name','upper_id','sort_no','create_time','update_time']
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
    _myref_str = ','+SysOrgEntity.get_myref_tables_str() if SysOrgEntity.get_myref_tables_str() != '' else ''
    attrstr = 'sys_org_id, org_name, upper_id, sort_no, create_time, update_time' +_myref_str
    sql = "select %s from vs_sys_org "%attrstr + _where + \
          order_by + " limit %(row_begin)s,%(row_cnt)s"
    sql_count = "select count(*) from v_sys_org " + _where
    entities = []
    rts = exesql(sql,{'row_cnt':row_cnt,'row_begin':row_begin})
    rtscnt = exesql(sql_count)
    total_cnt = int(rtscnt[0][0])
    for tup in rts:
        i = 0
        e = SysOrgEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5])
        i += len(SysOrgEntity.get_attrcodes())
        stup1 = tup[i];i += 1
        if stup1[0] != 0:
            e.ref_UpperId_SysOrg = SysOrgEntity.create_by_tuple(stup1)
        entities.append(e)
    return entities,total_cnt

def select_page(row_cnt, row_begin, search_params,order_by = " order by sys_org_id desc"):
    _where = "where"
    attrs = ['sys_org_id','org_name','upper_id','sort_no','create_time','update_time']
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
    sql = "select sys_org_id, org_name, upper_id, sort_no, create_time, update_time from v_sys_org " + _where + \
          order_by + " limit %(row_begin)s,%(row_cnt)s"
    sql_count = "select count(*) from v_sys_org " + _where
    entities = []
    rts = exesql(sql,{'row_cnt':row_cnt,'row_begin':row_begin})
    rtscnt = exesql(sql_count)
    total_cnt = int(rtscnt[0][0])
    for tup in rts:
        entities.append(SysOrgEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5]))
    return entities,total_cnt

def select_by_id(sys_org_id):
    sql = "select sys_org_id, org_name, upper_id, sort_no, create_time, update_time from  v_sys_org where sys_org_id = %(sys_org_id)s"
    rts = exesql(sql, {'sys_org_id':sys_org_id})
    if rts is None or len(rts) == 0:
        return None
    tup = rts[0]
    return SysOrgEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5])

def select_by_SysOrgId(sys_org_id, order_by = ' order by sys_org_id desc'):
    entities = []
    sql = "select sys_org_id, org_name, upper_id, sort_no, create_time, update_time from v_sys_org " \
          "where sys_org_id = %(sys_org_id)s" + order_by
    rts = exesql(sql, {'sys_org_id':sys_org_id})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(SysOrgEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5]))
    return entities
def select_by_OrgName(org_name, order_by = ' order by sys_org_id desc'):
    entities = []
    sql = "select sys_org_id, org_name, upper_id, sort_no, create_time, update_time from v_sys_org " \
          "where org_name = %(org_name)s" + order_by
    rts = exesql(sql, {'org_name':org_name})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(SysOrgEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5]))
    return entities
def select_by_UpperId(upper_id, order_by = ' order by sys_org_id desc'):
    entities = []
    sql = "select sys_org_id, org_name, upper_id, sort_no, create_time, update_time from v_sys_org " \
          "where upper_id = %(upper_id)s" + order_by
    rts = exesql(sql, {'upper_id':upper_id})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(SysOrgEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5]))
    return entities
def select_by_SortNo(sort_no, order_by = ' order by sys_org_id desc'):
    entities = []
    sql = "select sys_org_id, org_name, upper_id, sort_no, create_time, update_time from v_sys_org " \
          "where sort_no = %(sort_no)s" + order_by
    rts = exesql(sql, {'sort_no':sort_no})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(SysOrgEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5]))
    return entities
def select_by_CreateTime(create_time, order_by = ' order by sys_org_id desc'):
    entities = []
    sql = "select sys_org_id, org_name, upper_id, sort_no, create_time, update_time from v_sys_org " \
          "where create_time = %(create_time)s" + order_by
    rts = exesql(sql, {'create_time':create_time})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(SysOrgEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5]))
    return entities
def select_by_UpdateTime(update_time, order_by = ' order by sys_org_id desc'):
    entities = []
    sql = "select sys_org_id, org_name, upper_id, sort_no, create_time, update_time from v_sys_org " \
          "where update_time = %(update_time)s" + order_by
    rts = exesql(sql, {'update_time':update_time})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(SysOrgEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5]))
    return entities

def select_by_SysOrgIdList(sys_org_id_list,order_by = ' order by sys_org_id desc'):
    _dict = {}
    sql = "select sys_org_id, org_name, upper_id, sort_no, create_time, update_time from v_sys_org" \
          " where sys_org_id in (%(sys_org_id_list)s)" + order_by
    rts = exesql(sql, {'sys_org_id_list':sys_org_id_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = SysOrgEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5])
        if _dict.get(entity.sys_org_id) is None:
            _dict[entity.sys_org_id] = list()
        _dict[entity.sys_org_id].append(entity)
    return _dict
def select_by_OrgNameList(org_name_list,order_by = ' order by sys_org_id desc'):
    _dict = {}
    sql = "select sys_org_id, org_name, upper_id, sort_no, create_time, update_time from v_sys_org" \
          " where org_name in (%(org_name_list)s)" + order_by
    rts = exesql(sql, {'org_name_list':org_name_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = SysOrgEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5])
        if _dict.get(entity.org_name) is None:
            _dict[entity.org_name] = list()
        _dict[entity.org_name].append(entity)
    return _dict
def select_by_UpperIdList(upper_id_list,order_by = ' order by sys_org_id desc'):
    _dict = {}
    sql = "select sys_org_id, org_name, upper_id, sort_no, create_time, update_time from v_sys_org" \
          " where upper_id in (%(upper_id_list)s)" + order_by
    rts = exesql(sql, {'upper_id_list':upper_id_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = SysOrgEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5])
        if _dict.get(entity.upper_id) is None:
            _dict[entity.upper_id] = list()
        _dict[entity.upper_id].append(entity)
    return _dict
def select_by_SortNoList(sort_no_list,order_by = ' order by sys_org_id desc'):
    _dict = {}
    sql = "select sys_org_id, org_name, upper_id, sort_no, create_time, update_time from v_sys_org" \
          " where sort_no in (%(sort_no_list)s)" + order_by
    rts = exesql(sql, {'sort_no_list':sort_no_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = SysOrgEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5])
        if _dict.get(entity.sort_no) is None:
            _dict[entity.sort_no] = list()
        _dict[entity.sort_no].append(entity)
    return _dict
def select_by_CreateTimeList(create_time_list,order_by = ' order by sys_org_id desc'):
    _dict = {}
    sql = "select sys_org_id, org_name, upper_id, sort_no, create_time, update_time from v_sys_org" \
          " where create_time in (%(create_time_list)s)" + order_by
    rts = exesql(sql, {'create_time_list':create_time_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = SysOrgEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5])
        if _dict.get(entity.create_time) is None:
            _dict[entity.create_time] = list()
        _dict[entity.create_time].append(entity)
    return _dict
def select_by_UpdateTimeList(update_time_list,order_by = ' order by sys_org_id desc'):
    _dict = {}
    sql = "select sys_org_id, org_name, upper_id, sort_no, create_time, update_time from v_sys_org" \
          " where update_time in (%(update_time_list)s)" + order_by
    rts = exesql(sql, {'update_time_list':update_time_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = SysOrgEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5])
        if _dict.get(entity.update_time) is None:
            _dict[entity.update_time] = list()
        _dict[entity.update_time].append(entity)
    return _dict

