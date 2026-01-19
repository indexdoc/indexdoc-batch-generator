from sysdw import exesql
from utils import IDUtil
from domain.sysdomain.entity.SysDbLogEntity import SysDbLogEntity

from domain.sysdomain.entity.SysUserEntity import SysUserEntity

# sys_db_log_id, sys_user_id, op_datetime, op_duration, op_type, table_code, data_id, sql_str, sql_param, sql_result
# tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9]

def insert(entity):
    sql = "insert into phy_sys_db_log(sys_db_log_id, sys_user_id, op_datetime, op_duration, op_type, table_code, data_id, sql_str, sql_param, sql_result,ver_id) values"
    exesql(sql, [(entity.sys_db_log_id ,entity.sys_user_id ,entity.op_datetime ,entity.op_duration ,entity.op_type ,entity.table_code ,entity.data_id ,entity.sql_str ,entity.sql_param ,entity.sql_result ,IDUtil.get_long())])
    return entity

def delete_by_id(sys_db_log_id):
    sql = """insert into phy_sys_db_log(sys_db_log_id, sys_user_id, op_datetime, op_duration, op_type, table_code, data_id, sql_str, sql_param, sql_result,deleted,ver_id) 
        select sys_db_log_id, sys_user_id, op_datetime, op_duration, op_type, table_code, data_id, sql_str, sql_param, sql_result,1,%d from v_sys_db_log 
        where sys_db_log_id = %d"""%(IDUtil.get_long(),sys_db_log_id)
    exesql(sql)

def delete(entity):
    delete_by_id(entity.sys_db_log_id)

def update(entity):
    return insert(entity)

def update_by_id(sys_db_log_id,update_params):
    _entity = select_by_id(sys_db_log_id)
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

def full_search(search_str,row_cnt = 50000, row_begin=0, order_by = " order by sys_db_log_id desc"):
    if search_str is None or search_str.strip() == '' :
        return None
    _where = "where"
    _limit = " limit %s,%s"%(row_begin,row_cnt)
    attrs = ['sys_db_log_id','sys_user_id','op_datetime','op_duration','op_type','table_code','data_id','sql_str','sql_param','sql_result']
    for attr in attrs:
        _where += " toString(%s) like '%%%s%%' or"%(attr,search_str)
    _where += " %s like '%%%s%%' or"%("ref_SysUserId_SysUser.2", search_str)
    _where = _where + ' 1!=1'
    _myref_str = ','+SysDbLogEntity.get_myref_tables_str() if SysDbLogEntity.get_myref_tables_str() != '' else ''
    attrstr = 'sys_db_log_id, sys_user_id, op_datetime, op_duration, op_type, table_code, data_id, sql_str, sql_param, sql_result' +_myref_str
    sql = "select %s from vs_sys_db_log "%attrstr + _where + \
          order_by + _limit
    sql_count = "select count(*) from vs_sys_db_log " + _where
    entities = []
    rts = exesql(sql)
    rtscnt = exesql(sql_count)
    total_cnt = int(rtscnt[0][0])
    for tup in rts:
        i = 0
        e = SysDbLogEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9])
        i += len(SysDbLogEntity.get_attrcodes())
        stup1 = tup[i];i += 1
        if stup1[0] != 0:
            e.ref_SysUserId_SysUser = SysUserEntity.create_by_tuple(stup1)
        entities.append(e)
    return entities,total_cnt

def select_all(order_by = " order by sys_db_log_id desc"):
    entities = []
    sql = "select sys_db_log_id, sys_user_id, op_datetime, op_duration, op_type, table_code, data_id, sql_str, sql_param, sql_result from v_sys_db_log" + order_by
    rts = exesql(sql)
    for tup in rts:
        entities.append(SysDbLogEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9]))
    return entities

def select_count():
    sql = "select count(*) from v_sys_db_log"
    rts = exesql(sql)
    return int(rts[0][0])

#获取一页数据的同时也返回本表外键的数据
def select_vspage(row_cnt, row_begin, search_params,order_by = " order by sys_db_log_id desc"):
    _where = "where"
    attrs = ['sys_db_log_id','sys_user_id','op_datetime','op_duration','op_type','table_code','data_id','sql_str','sql_param','sql_result']
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
    _myref_str = ','+SysDbLogEntity.get_myref_tables_str() if SysDbLogEntity.get_myref_tables_str() != '' else ''
    attrstr = 'sys_db_log_id, sys_user_id, op_datetime, op_duration, op_type, table_code, data_id, sql_str, sql_param, sql_result' +_myref_str
    sql = "select %s from vs_sys_db_log "%attrstr + _where + \
          order_by + " limit %(row_begin)s,%(row_cnt)s"
    sql_count = "select count(*) from v_sys_db_log " + _where
    entities = []
    rts = exesql(sql,{'row_cnt':row_cnt,'row_begin':row_begin})
    rtscnt = exesql(sql_count)
    total_cnt = int(rtscnt[0][0])
    for tup in rts:
        i = 0
        e = SysDbLogEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9])
        i += len(SysDbLogEntity.get_attrcodes())
        stup1 = tup[i];i += 1
        if stup1[0] != 0:
            e.ref_SysUserId_SysUser = SysUserEntity.create_by_tuple(stup1)
        entities.append(e)
    return entities,total_cnt

def select_page(row_cnt, row_begin, search_params,order_by = " order by sys_db_log_id desc"):
    _where = "where"
    attrs = ['sys_db_log_id','sys_user_id','op_datetime','op_duration','op_type','table_code','data_id','sql_str','sql_param','sql_result']
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
    sql = "select sys_db_log_id, sys_user_id, op_datetime, op_duration, op_type, table_code, data_id, sql_str, sql_param, sql_result from v_sys_db_log " + _where + \
          order_by + " limit %(row_begin)s,%(row_cnt)s"
    sql_count = "select count(*) from v_sys_db_log " + _where
    entities = []
    rts = exesql(sql,{'row_cnt':row_cnt,'row_begin':row_begin})
    rtscnt = exesql(sql_count)
    total_cnt = int(rtscnt[0][0])
    for tup in rts:
        entities.append(SysDbLogEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9]))
    return entities,total_cnt

def select_by_id(sys_db_log_id):
    sql = "select sys_db_log_id, sys_user_id, op_datetime, op_duration, op_type, table_code, data_id, sql_str, sql_param, sql_result from  v_sys_db_log where sys_db_log_id = %(sys_db_log_id)s"
    rts = exesql(sql, {'sys_db_log_id':sys_db_log_id})
    if rts is None or len(rts) == 0:
        return None
    tup = rts[0]
    return SysDbLogEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9])

def select_by_SysDbLogId(sys_db_log_id, order_by = ' order by sys_db_log_id desc'):
    entities = []
    sql = "select sys_db_log_id, sys_user_id, op_datetime, op_duration, op_type, table_code, data_id, sql_str, sql_param, sql_result from v_sys_db_log " \
          "where sys_db_log_id = %(sys_db_log_id)s" + order_by
    rts = exesql(sql, {'sys_db_log_id':sys_db_log_id})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(SysDbLogEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9]))
    return entities
def select_by_SysUserId(sys_user_id, order_by = ' order by sys_db_log_id desc'):
    entities = []
    sql = "select sys_db_log_id, sys_user_id, op_datetime, op_duration, op_type, table_code, data_id, sql_str, sql_param, sql_result from v_sys_db_log " \
          "where sys_user_id = %(sys_user_id)s" + order_by
    rts = exesql(sql, {'sys_user_id':sys_user_id})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(SysDbLogEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9]))
    return entities
def select_by_OpDatetime(op_datetime, order_by = ' order by sys_db_log_id desc'):
    entities = []
    sql = "select sys_db_log_id, sys_user_id, op_datetime, op_duration, op_type, table_code, data_id, sql_str, sql_param, sql_result from v_sys_db_log " \
          "where op_datetime = %(op_datetime)s" + order_by
    rts = exesql(sql, {'op_datetime':op_datetime})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(SysDbLogEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9]))
    return entities
def select_by_OpDuration(op_duration, order_by = ' order by sys_db_log_id desc'):
    entities = []
    sql = "select sys_db_log_id, sys_user_id, op_datetime, op_duration, op_type, table_code, data_id, sql_str, sql_param, sql_result from v_sys_db_log " \
          "where op_duration = %(op_duration)s" + order_by
    rts = exesql(sql, {'op_duration':op_duration})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(SysDbLogEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9]))
    return entities
def select_by_OpType(op_type, order_by = ' order by sys_db_log_id desc'):
    entities = []
    sql = "select sys_db_log_id, sys_user_id, op_datetime, op_duration, op_type, table_code, data_id, sql_str, sql_param, sql_result from v_sys_db_log " \
          "where op_type = %(op_type)s" + order_by
    rts = exesql(sql, {'op_type':op_type})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(SysDbLogEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9]))
    return entities
def select_by_TableCode(table_code, order_by = ' order by sys_db_log_id desc'):
    entities = []
    sql = "select sys_db_log_id, sys_user_id, op_datetime, op_duration, op_type, table_code, data_id, sql_str, sql_param, sql_result from v_sys_db_log " \
          "where table_code = %(table_code)s" + order_by
    rts = exesql(sql, {'table_code':table_code})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(SysDbLogEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9]))
    return entities
def select_by_DataId(data_id, order_by = ' order by sys_db_log_id desc'):
    entities = []
    sql = "select sys_db_log_id, sys_user_id, op_datetime, op_duration, op_type, table_code, data_id, sql_str, sql_param, sql_result from v_sys_db_log " \
          "where data_id = %(data_id)s" + order_by
    rts = exesql(sql, {'data_id':data_id})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(SysDbLogEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9]))
    return entities
def select_by_SqlStr(sql_str, order_by = ' order by sys_db_log_id desc'):
    entities = []
    sql = "select sys_db_log_id, sys_user_id, op_datetime, op_duration, op_type, table_code, data_id, sql_str, sql_param, sql_result from v_sys_db_log " \
          "where sql_str = %(sql_str)s" + order_by
    rts = exesql(sql, {'sql_str':sql_str})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(SysDbLogEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9]))
    return entities
def select_by_SqlParam(sql_param, order_by = ' order by sys_db_log_id desc'):
    entities = []
    sql = "select sys_db_log_id, sys_user_id, op_datetime, op_duration, op_type, table_code, data_id, sql_str, sql_param, sql_result from v_sys_db_log " \
          "where sql_param = %(sql_param)s" + order_by
    rts = exesql(sql, {'sql_param':sql_param})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(SysDbLogEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9]))
    return entities
def select_by_SqlResult(sql_result, order_by = ' order by sys_db_log_id desc'):
    entities = []
    sql = "select sys_db_log_id, sys_user_id, op_datetime, op_duration, op_type, table_code, data_id, sql_str, sql_param, sql_result from v_sys_db_log " \
          "where sql_result = %(sql_result)s" + order_by
    rts = exesql(sql, {'sql_result':sql_result})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(SysDbLogEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9]))
    return entities

def select_by_SysDbLogIdList(sys_db_log_id_list,order_by = ' order by sys_db_log_id desc'):
    _dict = {}
    sql = "select sys_db_log_id, sys_user_id, op_datetime, op_duration, op_type, table_code, data_id, sql_str, sql_param, sql_result from v_sys_db_log" \
          " where sys_db_log_id in (%(sys_db_log_id_list)s)" + order_by
    rts = exesql(sql, {'sys_db_log_id_list':sys_db_log_id_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = SysDbLogEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9])
        if _dict.get(entity.sys_db_log_id) is None:
            _dict[entity.sys_db_log_id] = list()
        _dict[entity.sys_db_log_id].append(entity)
    return _dict
def select_by_SysUserIdList(sys_user_id_list,order_by = ' order by sys_db_log_id desc'):
    _dict = {}
    sql = "select sys_db_log_id, sys_user_id, op_datetime, op_duration, op_type, table_code, data_id, sql_str, sql_param, sql_result from v_sys_db_log" \
          " where sys_user_id in (%(sys_user_id_list)s)" + order_by
    rts = exesql(sql, {'sys_user_id_list':sys_user_id_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = SysDbLogEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9])
        if _dict.get(entity.sys_user_id) is None:
            _dict[entity.sys_user_id] = list()
        _dict[entity.sys_user_id].append(entity)
    return _dict
def select_by_OpDatetimeList(op_datetime_list,order_by = ' order by sys_db_log_id desc'):
    _dict = {}
    sql = "select sys_db_log_id, sys_user_id, op_datetime, op_duration, op_type, table_code, data_id, sql_str, sql_param, sql_result from v_sys_db_log" \
          " where op_datetime in (%(op_datetime_list)s)" + order_by
    rts = exesql(sql, {'op_datetime_list':op_datetime_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = SysDbLogEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9])
        if _dict.get(entity.op_datetime) is None:
            _dict[entity.op_datetime] = list()
        _dict[entity.op_datetime].append(entity)
    return _dict
def select_by_OpDurationList(op_duration_list,order_by = ' order by sys_db_log_id desc'):
    _dict = {}
    sql = "select sys_db_log_id, sys_user_id, op_datetime, op_duration, op_type, table_code, data_id, sql_str, sql_param, sql_result from v_sys_db_log" \
          " where op_duration in (%(op_duration_list)s)" + order_by
    rts = exesql(sql, {'op_duration_list':op_duration_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = SysDbLogEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9])
        if _dict.get(entity.op_duration) is None:
            _dict[entity.op_duration] = list()
        _dict[entity.op_duration].append(entity)
    return _dict
def select_by_OpTypeList(op_type_list,order_by = ' order by sys_db_log_id desc'):
    _dict = {}
    sql = "select sys_db_log_id, sys_user_id, op_datetime, op_duration, op_type, table_code, data_id, sql_str, sql_param, sql_result from v_sys_db_log" \
          " where op_type in (%(op_type_list)s)" + order_by
    rts = exesql(sql, {'op_type_list':op_type_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = SysDbLogEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9])
        if _dict.get(entity.op_type) is None:
            _dict[entity.op_type] = list()
        _dict[entity.op_type].append(entity)
    return _dict
def select_by_TableCodeList(table_code_list,order_by = ' order by sys_db_log_id desc'):
    _dict = {}
    sql = "select sys_db_log_id, sys_user_id, op_datetime, op_duration, op_type, table_code, data_id, sql_str, sql_param, sql_result from v_sys_db_log" \
          " where table_code in (%(table_code_list)s)" + order_by
    rts = exesql(sql, {'table_code_list':table_code_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = SysDbLogEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9])
        if _dict.get(entity.table_code) is None:
            _dict[entity.table_code] = list()
        _dict[entity.table_code].append(entity)
    return _dict
def select_by_DataIdList(data_id_list,order_by = ' order by sys_db_log_id desc'):
    _dict = {}
    sql = "select sys_db_log_id, sys_user_id, op_datetime, op_duration, op_type, table_code, data_id, sql_str, sql_param, sql_result from v_sys_db_log" \
          " where data_id in (%(data_id_list)s)" + order_by
    rts = exesql(sql, {'data_id_list':data_id_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = SysDbLogEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9])
        if _dict.get(entity.data_id) is None:
            _dict[entity.data_id] = list()
        _dict[entity.data_id].append(entity)
    return _dict
def select_by_SqlStrList(sql_str_list,order_by = ' order by sys_db_log_id desc'):
    _dict = {}
    sql = "select sys_db_log_id, sys_user_id, op_datetime, op_duration, op_type, table_code, data_id, sql_str, sql_param, sql_result from v_sys_db_log" \
          " where sql_str in (%(sql_str_list)s)" + order_by
    rts = exesql(sql, {'sql_str_list':sql_str_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = SysDbLogEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9])
        if _dict.get(entity.sql_str) is None:
            _dict[entity.sql_str] = list()
        _dict[entity.sql_str].append(entity)
    return _dict
def select_by_SqlParamList(sql_param_list,order_by = ' order by sys_db_log_id desc'):
    _dict = {}
    sql = "select sys_db_log_id, sys_user_id, op_datetime, op_duration, op_type, table_code, data_id, sql_str, sql_param, sql_result from v_sys_db_log" \
          " where sql_param in (%(sql_param_list)s)" + order_by
    rts = exesql(sql, {'sql_param_list':sql_param_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = SysDbLogEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9])
        if _dict.get(entity.sql_param) is None:
            _dict[entity.sql_param] = list()
        _dict[entity.sql_param].append(entity)
    return _dict
def select_by_SqlResultList(sql_result_list,order_by = ' order by sys_db_log_id desc'):
    _dict = {}
    sql = "select sys_db_log_id, sys_user_id, op_datetime, op_duration, op_type, table_code, data_id, sql_str, sql_param, sql_result from v_sys_db_log" \
          " where sql_result in (%(sql_result_list)s)" + order_by
    rts = exesql(sql, {'sql_result_list':sql_result_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = SysDbLogEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9])
        if _dict.get(entity.sql_result) is None:
            _dict[entity.sql_result] = list()
        _dict[entity.sql_result].append(entity)
    return _dict

