from sysdw import exesql
from utils import IDUtil
from domain.sysdomain.entity.OrgDutyEntity import OrgDutyEntity

from domain.sysdomain.entity.SysOrgEntity import SysOrgEntity

# org_duty_id, sys_org_id, org_duty_name, update_time, create_time
# tup[0], tup[1], tup[2], tup[3], tup[4]

def insert(entity):
    sql = "insert into phy_org_duty(org_duty_id, sys_org_id, org_duty_name, update_time, create_time,ver_id) values"
    exesql(sql, [(entity.org_duty_id ,entity.sys_org_id ,entity.org_duty_name ,entity.update_time ,entity.create_time ,IDUtil.get_long())])
    return entity

def delete_by_id(org_duty_id):
    sql = """insert into phy_org_duty(org_duty_id, sys_org_id, org_duty_name, update_time, create_time,deleted,ver_id) 
        select org_duty_id, sys_org_id, org_duty_name, update_time, create_time,1,%d from v_org_duty 
        where org_duty_id = %d"""%(IDUtil.get_long(),org_duty_id)
    exesql(sql)

def delete(entity):
    delete_by_id(entity.org_duty_id)

def update(entity):
    return insert(entity)

def update_by_id(org_duty_id,update_params):
    _entity = select_by_id(org_duty_id)
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

def full_search(search_str,row_cnt = 50000, row_begin=0, order_by = " order by org_duty_id desc"):
    if search_str is None or search_str.strip() == '' :
        return None
    _where = "where"
    _limit = " limit %s,%s"%(row_begin,row_cnt)
    attrs = ['org_duty_id','sys_org_id','org_duty_name','update_time','create_time']
    for attr in attrs:
        _where += " toString(%s) like '%%%s%%' or"%(attr,search_str)
    _where += " %s like '%%%s%%' or"%("ref_SysOrgId_SysOrg.2", search_str)
    _where = _where + ' 1!=1'
    _myref_str = ','+OrgDutyEntity.get_myref_tables_str() if OrgDutyEntity.get_myref_tables_str() != '' else ''
    attrstr = 'org_duty_id, sys_org_id, org_duty_name, update_time, create_time' +_myref_str
    sql = "select %s from vs_org_duty "%attrstr + _where + \
          order_by + _limit
    sql_count = "select count(*) from vs_org_duty " + _where
    entities = []
    rts = exesql(sql)
    rtscnt = exesql(sql_count)
    total_cnt = int(rtscnt[0][0])
    for tup in rts:
        i = 0
        e = OrgDutyEntity(tup[0], tup[1], tup[2], tup[3], tup[4])
        i += len(OrgDutyEntity.get_attrcodes())
        stup1 = tup[i];i += 1
        if stup1[0] != 0:
            e.ref_SysOrgId_SysOrg = SysOrgEntity.create_by_tuple(stup1)
        entities.append(e)
    return entities,total_cnt

def select_all(order_by = " order by org_duty_id desc"):
    entities = []
    sql = "select org_duty_id, sys_org_id, org_duty_name, update_time, create_time from v_org_duty" + order_by
    rts = exesql(sql)
    for tup in rts:
        entities.append(OrgDutyEntity(tup[0], tup[1], tup[2], tup[3], tup[4]))
    return entities

def select_count():
    sql = "select count(*) from v_org_duty"
    rts = exesql(sql)
    return int(rts[0][0])

#获取一页数据的同时也返回本表外键的数据
def select_vspage(row_cnt, row_begin, search_params,order_by = " order by org_duty_id desc"):
    _where = "where"
    attrs = ['org_duty_id','sys_org_id','org_duty_name','update_time','create_time']
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
    _myref_str = ','+OrgDutyEntity.get_myref_tables_str() if OrgDutyEntity.get_myref_tables_str() != '' else ''
    attrstr = 'org_duty_id, sys_org_id, org_duty_name, update_time, create_time' +_myref_str
    sql = "select %s from vs_org_duty "%attrstr + _where + \
          order_by + " limit %(row_begin)s,%(row_cnt)s"
    sql_count = "select count(*) from v_org_duty " + _where
    entities = []
    rts = exesql(sql,{'row_cnt':row_cnt,'row_begin':row_begin})
    rtscnt = exesql(sql_count)
    total_cnt = int(rtscnt[0][0])
    for tup in rts:
        i = 0
        e = OrgDutyEntity(tup[0], tup[1], tup[2], tup[3], tup[4])
        i += len(OrgDutyEntity.get_attrcodes())
        stup1 = tup[i];i += 1
        if stup1[0] != 0:
            e.ref_SysOrgId_SysOrg = SysOrgEntity.create_by_tuple(stup1)
        entities.append(e)
    return entities,total_cnt

def select_page(row_cnt, row_begin, search_params,order_by = " order by org_duty_id desc"):
    _where = "where"
    attrs = ['org_duty_id','sys_org_id','org_duty_name','update_time','create_time']
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
    sql = "select org_duty_id, sys_org_id, org_duty_name, update_time, create_time from v_org_duty " + _where + \
          order_by + " limit %(row_begin)s,%(row_cnt)s"
    sql_count = "select count(*) from v_org_duty " + _where
    entities = []
    rts = exesql(sql,{'row_cnt':row_cnt,'row_begin':row_begin})
    rtscnt = exesql(sql_count)
    total_cnt = int(rtscnt[0][0])
    for tup in rts:
        entities.append(OrgDutyEntity(tup[0], tup[1], tup[2], tup[3], tup[4]))
    return entities,total_cnt

def select_by_id(org_duty_id):
    sql = "select org_duty_id, sys_org_id, org_duty_name, update_time, create_time from  v_org_duty where org_duty_id = %(org_duty_id)s"
    rts = exesql(sql, {'org_duty_id':org_duty_id})
    if rts is None or len(rts) == 0:
        return None
    tup = rts[0]
    return OrgDutyEntity(tup[0], tup[1], tup[2], tup[3], tup[4])

def select_by_OrgDutyId(org_duty_id, order_by = ' order by org_duty_id desc'):
    entities = []
    sql = "select org_duty_id, sys_org_id, org_duty_name, update_time, create_time from v_org_duty " \
          "where org_duty_id = %(org_duty_id)s" + order_by
    rts = exesql(sql, {'org_duty_id':org_duty_id})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(OrgDutyEntity(tup[0], tup[1], tup[2], tup[3], tup[4]))
    return entities
def select_by_SysOrgId(sys_org_id, order_by = ' order by org_duty_id desc'):
    entities = []
    sql = "select org_duty_id, sys_org_id, org_duty_name, update_time, create_time from v_org_duty " \
          "where sys_org_id = %(sys_org_id)s" + order_by
    rts = exesql(sql, {'sys_org_id':sys_org_id})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(OrgDutyEntity(tup[0], tup[1], tup[2], tup[3], tup[4]))
    return entities
def select_by_OrgDutyName(org_duty_name, order_by = ' order by org_duty_id desc'):
    entities = []
    sql = "select org_duty_id, sys_org_id, org_duty_name, update_time, create_time from v_org_duty " \
          "where org_duty_name = %(org_duty_name)s" + order_by
    rts = exesql(sql, {'org_duty_name':org_duty_name})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(OrgDutyEntity(tup[0], tup[1], tup[2], tup[3], tup[4]))
    return entities
def select_by_UpdateTime(update_time, order_by = ' order by org_duty_id desc'):
    entities = []
    sql = "select org_duty_id, sys_org_id, org_duty_name, update_time, create_time from v_org_duty " \
          "where update_time = %(update_time)s" + order_by
    rts = exesql(sql, {'update_time':update_time})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(OrgDutyEntity(tup[0], tup[1], tup[2], tup[3], tup[4]))
    return entities
def select_by_CreateTime(create_time, order_by = ' order by org_duty_id desc'):
    entities = []
    sql = "select org_duty_id, sys_org_id, org_duty_name, update_time, create_time from v_org_duty " \
          "where create_time = %(create_time)s" + order_by
    rts = exesql(sql, {'create_time':create_time})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(OrgDutyEntity(tup[0], tup[1], tup[2], tup[3], tup[4]))
    return entities

def select_by_OrgDutyIdList(org_duty_id_list,order_by = ' order by org_duty_id desc'):
    _dict = {}
    sql = "select org_duty_id, sys_org_id, org_duty_name, update_time, create_time from v_org_duty" \
          " where org_duty_id in (%(org_duty_id_list)s)" + order_by
    rts = exesql(sql, {'org_duty_id_list':org_duty_id_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = OrgDutyEntity(tup[0], tup[1], tup[2], tup[3], tup[4])
        if _dict.get(entity.org_duty_id) is None:
            _dict[entity.org_duty_id] = list()
        _dict[entity.org_duty_id].append(entity)
    return _dict
def select_by_SysOrgIdList(sys_org_id_list,order_by = ' order by org_duty_id desc'):
    _dict = {}
    sql = "select org_duty_id, sys_org_id, org_duty_name, update_time, create_time from v_org_duty" \
          " where sys_org_id in (%(sys_org_id_list)s)" + order_by
    rts = exesql(sql, {'sys_org_id_list':sys_org_id_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = OrgDutyEntity(tup[0], tup[1], tup[2], tup[3], tup[4])
        if _dict.get(entity.sys_org_id) is None:
            _dict[entity.sys_org_id] = list()
        _dict[entity.sys_org_id].append(entity)
    return _dict
def select_by_OrgDutyNameList(org_duty_name_list,order_by = ' order by org_duty_id desc'):
    _dict = {}
    sql = "select org_duty_id, sys_org_id, org_duty_name, update_time, create_time from v_org_duty" \
          " where org_duty_name in (%(org_duty_name_list)s)" + order_by
    rts = exesql(sql, {'org_duty_name_list':org_duty_name_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = OrgDutyEntity(tup[0], tup[1], tup[2], tup[3], tup[4])
        if _dict.get(entity.org_duty_name) is None:
            _dict[entity.org_duty_name] = list()
        _dict[entity.org_duty_name].append(entity)
    return _dict
def select_by_UpdateTimeList(update_time_list,order_by = ' order by org_duty_id desc'):
    _dict = {}
    sql = "select org_duty_id, sys_org_id, org_duty_name, update_time, create_time from v_org_duty" \
          " where update_time in (%(update_time_list)s)" + order_by
    rts = exesql(sql, {'update_time_list':update_time_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = OrgDutyEntity(tup[0], tup[1], tup[2], tup[3], tup[4])
        if _dict.get(entity.update_time) is None:
            _dict[entity.update_time] = list()
        _dict[entity.update_time].append(entity)
    return _dict
def select_by_CreateTimeList(create_time_list,order_by = ' order by org_duty_id desc'):
    _dict = {}
    sql = "select org_duty_id, sys_org_id, org_duty_name, update_time, create_time from v_org_duty" \
          " where create_time in (%(create_time_list)s)" + order_by
    rts = exesql(sql, {'create_time_list':create_time_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = OrgDutyEntity(tup[0], tup[1], tup[2], tup[3], tup[4])
        if _dict.get(entity.create_time) is None:
            _dict[entity.create_time] = list()
        _dict[entity.create_time].append(entity)
    return _dict

