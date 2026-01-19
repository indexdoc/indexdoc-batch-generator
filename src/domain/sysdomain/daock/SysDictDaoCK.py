from sysdw import exesql
from utils import IDUtil
from domain.sysdomain.entity.SysDictEntity import SysDictEntity


# sys_dict_id, module_name, table_name, column_name, select_mode, data_value, remark
# tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6]

def insert(entity):
    sql = "insert into phy_sys_dict(sys_dict_id, module_name, table_name, column_name, select_mode, data_value, remark,ver_id) values"
    exesql(sql, [(entity.sys_dict_id ,entity.module_name ,entity.table_name ,entity.column_name ,entity.select_mode ,entity.data_value ,entity.remark ,IDUtil.get_long())])
    return entity

def delete_by_id(sys_dict_id):
    sql = """insert into phy_sys_dict(sys_dict_id, module_name, table_name, column_name, select_mode, data_value, remark,deleted,ver_id) 
        select sys_dict_id, module_name, table_name, column_name, select_mode, data_value, remark,1,%d from v_sys_dict 
        where sys_dict_id = %d"""%(IDUtil.get_long(),sys_dict_id)
    exesql(sql)

def delete(entity):
    delete_by_id(entity.sys_dict_id)

def update(entity):
    return insert(entity)

def update_by_id(sys_dict_id,update_params):
    _entity = select_by_id(sys_dict_id)
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

def full_search(search_str,row_cnt = 50000, row_begin=0, order_by = " order by sys_dict_id desc"):
    if search_str is None or search_str.strip() == '' :
        return None
    _where = "where"
    _limit = " limit %s,%s"%(row_begin,row_cnt)
    attrs = ['sys_dict_id','module_name','table_name','column_name','select_mode','data_value','remark']
    for attr in attrs:
        _where += " toString(%s) like '%%%s%%' or"%(attr,search_str)
    _where = _where + ' 1!=1'
    _myref_str = ','+SysDictEntity.get_myref_tables_str() if SysDictEntity.get_myref_tables_str() != '' else ''
    attrstr = 'sys_dict_id, module_name, table_name, column_name, select_mode, data_value, remark' +_myref_str
    sql = "select %s from vs_sys_dict "%attrstr + _where + \
          order_by + _limit
    sql_count = "select count(*) from vs_sys_dict " + _where
    entities = []
    rts = exesql(sql)
    rtscnt = exesql(sql_count)
    total_cnt = int(rtscnt[0][0])
    for tup in rts:
        i = 0
        e = SysDictEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6])
        i += len(SysDictEntity.get_attrcodes())
        entities.append(e)
    return entities,total_cnt

def select_all(order_by = " order by sys_dict_id desc"):
    entities = []
    sql = "select sys_dict_id, module_name, table_name, column_name, select_mode, data_value, remark from v_sys_dict" + order_by
    rts = exesql(sql)
    for tup in rts:
        entities.append(SysDictEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6]))
    return entities

def select_count():
    sql = "select count(*) from v_sys_dict"
    rts = exesql(sql)
    return int(rts[0][0])

#获取一页数据的同时也返回本表外键的数据
def select_vspage(row_cnt, row_begin, search_params,order_by = " order by sys_dict_id desc"):
    _where = "where"
    attrs = ['sys_dict_id','module_name','table_name','column_name','select_mode','data_value','remark']
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
    _myref_str = ','+SysDictEntity.get_myref_tables_str() if SysDictEntity.get_myref_tables_str() != '' else ''
    attrstr = 'sys_dict_id, module_name, table_name, column_name, select_mode, data_value, remark' +_myref_str
    sql = "select %s from vs_sys_dict "%attrstr + _where + \
          order_by + " limit %(row_begin)s,%(row_cnt)s"
    sql_count = "select count(*) from v_sys_dict " + _where
    entities = []
    rts = exesql(sql,{'row_cnt':row_cnt,'row_begin':row_begin})
    rtscnt = exesql(sql_count)
    total_cnt = int(rtscnt[0][0])
    for tup in rts:
        i = 0
        e = SysDictEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6])
        i += len(SysDictEntity.get_attrcodes())
        entities.append(e)
    return entities,total_cnt

def select_page(row_cnt, row_begin, search_params,order_by = " order by sys_dict_id desc"):
    _where = "where"
    attrs = ['sys_dict_id','module_name','table_name','column_name','select_mode','data_value','remark']
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
    sql = "select sys_dict_id, module_name, table_name, column_name, select_mode, data_value, remark from v_sys_dict " + _where + \
          order_by + " limit %(row_begin)s,%(row_cnt)s"
    sql_count = "select count(*) from v_sys_dict " + _where
    entities = []
    rts = exesql(sql,{'row_cnt':row_cnt,'row_begin':row_begin})
    rtscnt = exesql(sql_count)
    total_cnt = int(rtscnt[0][0])
    for tup in rts:
        entities.append(SysDictEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6]))
    return entities,total_cnt

def select_by_id(sys_dict_id):
    sql = "select sys_dict_id, module_name, table_name, column_name, select_mode, data_value, remark from  v_sys_dict where sys_dict_id = %(sys_dict_id)s"
    rts = exesql(sql, {'sys_dict_id':sys_dict_id})
    if rts is None or len(rts) == 0:
        return None
    tup = rts[0]
    return SysDictEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6])

def select_by_SysDictId(sys_dict_id, order_by = ' order by sys_dict_id desc'):
    entities = []
    sql = "select sys_dict_id, module_name, table_name, column_name, select_mode, data_value, remark from v_sys_dict " \
          "where sys_dict_id = %(sys_dict_id)s" + order_by
    rts = exesql(sql, {'sys_dict_id':sys_dict_id})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(SysDictEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6]))
    return entities
def select_by_ModuleName(module_name, order_by = ' order by sys_dict_id desc'):
    entities = []
    sql = "select sys_dict_id, module_name, table_name, column_name, select_mode, data_value, remark from v_sys_dict " \
          "where module_name = %(module_name)s" + order_by
    rts = exesql(sql, {'module_name':module_name})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(SysDictEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6]))
    return entities
def select_by_TableName(table_name, order_by = ' order by sys_dict_id desc'):
    entities = []
    sql = "select sys_dict_id, module_name, table_name, column_name, select_mode, data_value, remark from v_sys_dict " \
          "where table_name = %(table_name)s" + order_by
    rts = exesql(sql, {'table_name':table_name})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(SysDictEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6]))
    return entities
def select_by_ColumnName(column_name, order_by = ' order by sys_dict_id desc'):
    entities = []
    sql = "select sys_dict_id, module_name, table_name, column_name, select_mode, data_value, remark from v_sys_dict " \
          "where column_name = %(column_name)s" + order_by
    rts = exesql(sql, {'column_name':column_name})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(SysDictEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6]))
    return entities
def select_by_SelectMode(select_mode, order_by = ' order by sys_dict_id desc'):
    entities = []
    sql = "select sys_dict_id, module_name, table_name, column_name, select_mode, data_value, remark from v_sys_dict " \
          "where select_mode = %(select_mode)s" + order_by
    rts = exesql(sql, {'select_mode':select_mode})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(SysDictEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6]))
    return entities
def select_by_DataValue(data_value, order_by = ' order by sys_dict_id desc'):
    entities = []
    sql = "select sys_dict_id, module_name, table_name, column_name, select_mode, data_value, remark from v_sys_dict " \
          "where data_value = %(data_value)s" + order_by
    rts = exesql(sql, {'data_value':data_value})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(SysDictEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6]))
    return entities
def select_by_Remark(remark, order_by = ' order by sys_dict_id desc'):
    entities = []
    sql = "select sys_dict_id, module_name, table_name, column_name, select_mode, data_value, remark from v_sys_dict " \
          "where remark = %(remark)s" + order_by
    rts = exesql(sql, {'remark':remark})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(SysDictEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6]))
    return entities

def select_by_SysDictIdList(sys_dict_id_list,order_by = ' order by sys_dict_id desc'):
    _dict = {}
    sql = "select sys_dict_id, module_name, table_name, column_name, select_mode, data_value, remark from v_sys_dict" \
          " where sys_dict_id in (%(sys_dict_id_list)s)" + order_by
    rts = exesql(sql, {'sys_dict_id_list':sys_dict_id_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = SysDictEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6])
        if _dict.get(entity.sys_dict_id) is None:
            _dict[entity.sys_dict_id] = list()
        _dict[entity.sys_dict_id].append(entity)
    return _dict
def select_by_ModuleNameList(module_name_list,order_by = ' order by sys_dict_id desc'):
    _dict = {}
    sql = "select sys_dict_id, module_name, table_name, column_name, select_mode, data_value, remark from v_sys_dict" \
          " where module_name in (%(module_name_list)s)" + order_by
    rts = exesql(sql, {'module_name_list':module_name_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = SysDictEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6])
        if _dict.get(entity.module_name) is None:
            _dict[entity.module_name] = list()
        _dict[entity.module_name].append(entity)
    return _dict
def select_by_TableNameList(table_name_list,order_by = ' order by sys_dict_id desc'):
    _dict = {}
    sql = "select sys_dict_id, module_name, table_name, column_name, select_mode, data_value, remark from v_sys_dict" \
          " where table_name in (%(table_name_list)s)" + order_by
    rts = exesql(sql, {'table_name_list':table_name_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = SysDictEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6])
        if _dict.get(entity.table_name) is None:
            _dict[entity.table_name] = list()
        _dict[entity.table_name].append(entity)
    return _dict
def select_by_ColumnNameList(column_name_list,order_by = ' order by sys_dict_id desc'):
    _dict = {}
    sql = "select sys_dict_id, module_name, table_name, column_name, select_mode, data_value, remark from v_sys_dict" \
          " where column_name in (%(column_name_list)s)" + order_by
    rts = exesql(sql, {'column_name_list':column_name_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = SysDictEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6])
        if _dict.get(entity.column_name) is None:
            _dict[entity.column_name] = list()
        _dict[entity.column_name].append(entity)
    return _dict
def select_by_SelectModeList(select_mode_list,order_by = ' order by sys_dict_id desc'):
    _dict = {}
    sql = "select sys_dict_id, module_name, table_name, column_name, select_mode, data_value, remark from v_sys_dict" \
          " where select_mode in (%(select_mode_list)s)" + order_by
    rts = exesql(sql, {'select_mode_list':select_mode_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = SysDictEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6])
        if _dict.get(entity.select_mode) is None:
            _dict[entity.select_mode] = list()
        _dict[entity.select_mode].append(entity)
    return _dict
def select_by_DataValueList(data_value_list,order_by = ' order by sys_dict_id desc'):
    _dict = {}
    sql = "select sys_dict_id, module_name, table_name, column_name, select_mode, data_value, remark from v_sys_dict" \
          " where data_value in (%(data_value_list)s)" + order_by
    rts = exesql(sql, {'data_value_list':data_value_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = SysDictEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6])
        if _dict.get(entity.data_value) is None:
            _dict[entity.data_value] = list()
        _dict[entity.data_value].append(entity)
    return _dict
def select_by_RemarkList(remark_list,order_by = ' order by sys_dict_id desc'):
    _dict = {}
    sql = "select sys_dict_id, module_name, table_name, column_name, select_mode, data_value, remark from v_sys_dict" \
          " where remark in (%(remark_list)s)" + order_by
    rts = exesql(sql, {'remark_list':remark_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = SysDictEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6])
        if _dict.get(entity.remark) is None:
            _dict[entity.remark] = list()
        _dict[entity.remark].append(entity)
    return _dict

