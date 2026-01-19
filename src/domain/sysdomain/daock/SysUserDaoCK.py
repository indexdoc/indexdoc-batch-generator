from sysdw import exesql
from utils import IDUtil
from domain.sysdomain.entity.SysUserEntity import SysUserEntity


# sys_user_id, user_name, pwd, last_login_time, last_active_time, create_time, update_time, last_login_info, remark
# tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8]

def insert(entity):
    sql = "insert into phy_sys_user(sys_user_id, user_name, pwd, last_login_time, last_active_time, create_time, update_time, last_login_info, remark,ver_id) values"
    exesql(sql, [(entity.sys_user_id ,entity.user_name ,entity.pwd ,entity.last_login_time ,entity.last_active_time ,entity.create_time ,entity.update_time ,entity.last_login_info ,entity.remark ,IDUtil.get_long())])
    return entity

def delete_by_id(sys_user_id):
    sql = """insert into phy_sys_user(sys_user_id, user_name, pwd, last_login_time, last_active_time, create_time, update_time, last_login_info, remark,deleted,ver_id) 
        select sys_user_id, user_name, pwd, last_login_time, last_active_time, create_time, update_time, last_login_info, remark,1,%d from v_sys_user 
        where sys_user_id = %d"""%(IDUtil.get_long(),sys_user_id)
    exesql(sql)

def delete(entity):
    delete_by_id(entity.sys_user_id)

def update(entity):
    return insert(entity)

def update_by_id(sys_user_id,update_params):
    _entity = select_by_id(sys_user_id)
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

def full_search(search_str,row_cnt = 50000, row_begin=0, order_by = " order by sys_user_id desc"):
    if search_str is None or search_str.strip() == '' :
        return None
    _where = "where"
    _limit = " limit %s,%s"%(row_begin,row_cnt)
    attrs = ['sys_user_id','user_name','pwd','last_login_time','last_active_time','create_time','update_time','last_login_info','remark']
    for attr in attrs:
        _where += " toString(%s) like '%%%s%%' or"%(attr,search_str)
    _where = _where + ' 1!=1'
    _myref_str = ','+SysUserEntity.get_myref_tables_str() if SysUserEntity.get_myref_tables_str() != '' else ''
    attrstr = 'sys_user_id, user_name, pwd, last_login_time, last_active_time, create_time, update_time, last_login_info, remark' +_myref_str
    sql = "select %s from vs_sys_user "%attrstr + _where + \
          order_by + _limit
    sql_count = "select count(*) from vs_sys_user " + _where
    entities = []
    rts = exesql(sql)
    rtscnt = exesql(sql_count)
    total_cnt = int(rtscnt[0][0])
    for tup in rts:
        i = 0
        e = SysUserEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8])
        i += len(SysUserEntity.get_attrcodes())
        entities.append(e)
    return entities,total_cnt

def select_all(order_by = " order by sys_user_id desc"):
    entities = []
    sql = "select sys_user_id, user_name, pwd, last_login_time, last_active_time, create_time, update_time, last_login_info, remark from v_sys_user" + order_by
    rts = exesql(sql)
    for tup in rts:
        entities.append(SysUserEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8]))
    return entities

def select_count():
    sql = "select count(*) from v_sys_user"
    rts = exesql(sql)
    return int(rts[0][0])

#获取一页数据的同时也返回本表外键的数据
def select_vspage(row_cnt, row_begin, search_params,order_by = " order by sys_user_id desc"):
    _where = "where"
    attrs = ['sys_user_id','user_name','pwd','last_login_time','last_active_time','create_time','update_time','last_login_info','remark']
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
    _myref_str = ','+SysUserEntity.get_myref_tables_str() if SysUserEntity.get_myref_tables_str() != '' else ''
    attrstr = 'sys_user_id, user_name, pwd, last_login_time, last_active_time, create_time, update_time, last_login_info, remark' +_myref_str
    sql = "select %s from vs_sys_user "%attrstr + _where + \
          order_by + " limit %(row_begin)s,%(row_cnt)s"
    sql_count = "select count(*) from v_sys_user " + _where
    entities = []
    rts = exesql(sql,{'row_cnt':row_cnt,'row_begin':row_begin})
    rtscnt = exesql(sql_count)
    total_cnt = int(rtscnt[0][0])
    for tup in rts:
        i = 0
        e = SysUserEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8])
        i += len(SysUserEntity.get_attrcodes())
        entities.append(e)
    return entities,total_cnt

def select_page(row_cnt, row_begin, search_params,order_by = " order by sys_user_id desc"):
    _where = "where"
    attrs = ['sys_user_id','user_name','pwd','last_login_time','last_active_time','create_time','update_time','last_login_info','remark']
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
    sql = "select sys_user_id, user_name, pwd, last_login_time, last_active_time, create_time, update_time, last_login_info, remark from v_sys_user " + _where + \
          order_by + " limit %(row_begin)s,%(row_cnt)s"
    sql_count = "select count(*) from v_sys_user " + _where
    entities = []
    rts = exesql(sql,{'row_cnt':row_cnt,'row_begin':row_begin})
    rtscnt = exesql(sql_count)
    total_cnt = int(rtscnt[0][0])
    for tup in rts:
        entities.append(SysUserEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8]))
    return entities,total_cnt

def select_by_id(sys_user_id):
    sql = "select sys_user_id, user_name, pwd, last_login_time, last_active_time, create_time, update_time, last_login_info, remark from  v_sys_user where sys_user_id = %(sys_user_id)s"
    rts = exesql(sql, {'sys_user_id':sys_user_id})
    if rts is None or len(rts) == 0:
        return None
    tup = rts[0]
    return SysUserEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8])

def select_by_SysUserId(sys_user_id, order_by = ' order by sys_user_id desc'):
    entities = []
    sql = "select sys_user_id, user_name, pwd, last_login_time, last_active_time, create_time, update_time, last_login_info, remark from v_sys_user " \
          "where sys_user_id = %(sys_user_id)s" + order_by
    rts = exesql(sql, {'sys_user_id':sys_user_id})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(SysUserEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8]))
    return entities
def select_by_UserName(user_name, order_by = ' order by sys_user_id desc'):
    entities = []
    sql = "select sys_user_id, user_name, pwd, last_login_time, last_active_time, create_time, update_time, last_login_info, remark from v_sys_user " \
          "where user_name = %(user_name)s" + order_by
    rts = exesql(sql, {'user_name':user_name})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(SysUserEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8]))
    return entities
def select_by_Pwd(pwd, order_by = ' order by sys_user_id desc'):
    entities = []
    sql = "select sys_user_id, user_name, pwd, last_login_time, last_active_time, create_time, update_time, last_login_info, remark from v_sys_user " \
          "where pwd = %(pwd)s" + order_by
    rts = exesql(sql, {'pwd':pwd})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(SysUserEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8]))
    return entities
def select_by_LastLoginTime(last_login_time, order_by = ' order by sys_user_id desc'):
    entities = []
    sql = "select sys_user_id, user_name, pwd, last_login_time, last_active_time, create_time, update_time, last_login_info, remark from v_sys_user " \
          "where last_login_time = %(last_login_time)s" + order_by
    rts = exesql(sql, {'last_login_time':last_login_time})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(SysUserEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8]))
    return entities
def select_by_LastActiveTime(last_active_time, order_by = ' order by sys_user_id desc'):
    entities = []
    sql = "select sys_user_id, user_name, pwd, last_login_time, last_active_time, create_time, update_time, last_login_info, remark from v_sys_user " \
          "where last_active_time = %(last_active_time)s" + order_by
    rts = exesql(sql, {'last_active_time':last_active_time})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(SysUserEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8]))
    return entities
def select_by_CreateTime(create_time, order_by = ' order by sys_user_id desc'):
    entities = []
    sql = "select sys_user_id, user_name, pwd, last_login_time, last_active_time, create_time, update_time, last_login_info, remark from v_sys_user " \
          "where create_time = %(create_time)s" + order_by
    rts = exesql(sql, {'create_time':create_time})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(SysUserEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8]))
    return entities
def select_by_UpdateTime(update_time, order_by = ' order by sys_user_id desc'):
    entities = []
    sql = "select sys_user_id, user_name, pwd, last_login_time, last_active_time, create_time, update_time, last_login_info, remark from v_sys_user " \
          "where update_time = %(update_time)s" + order_by
    rts = exesql(sql, {'update_time':update_time})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(SysUserEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8]))
    return entities
def select_by_LastLoginInfo(last_login_info, order_by = ' order by sys_user_id desc'):
    entities = []
    sql = "select sys_user_id, user_name, pwd, last_login_time, last_active_time, create_time, update_time, last_login_info, remark from v_sys_user " \
          "where last_login_info = %(last_login_info)s" + order_by
    rts = exesql(sql, {'last_login_info':last_login_info})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(SysUserEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8]))
    return entities
def select_by_Remark(remark, order_by = ' order by sys_user_id desc'):
    entities = []
    sql = "select sys_user_id, user_name, pwd, last_login_time, last_active_time, create_time, update_time, last_login_info, remark from v_sys_user " \
          "where remark = %(remark)s" + order_by
    rts = exesql(sql, {'remark':remark})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(SysUserEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8]))
    return entities

def select_by_SysUserIdList(sys_user_id_list,order_by = ' order by sys_user_id desc'):
    _dict = {}
    sql = "select sys_user_id, user_name, pwd, last_login_time, last_active_time, create_time, update_time, last_login_info, remark from v_sys_user" \
          " where sys_user_id in (%(sys_user_id_list)s)" + order_by
    rts = exesql(sql, {'sys_user_id_list':sys_user_id_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = SysUserEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8])
        if _dict.get(entity.sys_user_id) is None:
            _dict[entity.sys_user_id] = list()
        _dict[entity.sys_user_id].append(entity)
    return _dict
def select_by_UserNameList(user_name_list,order_by = ' order by sys_user_id desc'):
    _dict = {}
    sql = "select sys_user_id, user_name, pwd, last_login_time, last_active_time, create_time, update_time, last_login_info, remark from v_sys_user" \
          " where user_name in (%(user_name_list)s)" + order_by
    rts = exesql(sql, {'user_name_list':user_name_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = SysUserEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8])
        if _dict.get(entity.user_name) is None:
            _dict[entity.user_name] = list()
        _dict[entity.user_name].append(entity)
    return _dict
def select_by_PwdList(pwd_list,order_by = ' order by sys_user_id desc'):
    _dict = {}
    sql = "select sys_user_id, user_name, pwd, last_login_time, last_active_time, create_time, update_time, last_login_info, remark from v_sys_user" \
          " where pwd in (%(pwd_list)s)" + order_by
    rts = exesql(sql, {'pwd_list':pwd_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = SysUserEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8])
        if _dict.get(entity.pwd) is None:
            _dict[entity.pwd] = list()
        _dict[entity.pwd].append(entity)
    return _dict
def select_by_LastLoginTimeList(last_login_time_list,order_by = ' order by sys_user_id desc'):
    _dict = {}
    sql = "select sys_user_id, user_name, pwd, last_login_time, last_active_time, create_time, update_time, last_login_info, remark from v_sys_user" \
          " where last_login_time in (%(last_login_time_list)s)" + order_by
    rts = exesql(sql, {'last_login_time_list':last_login_time_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = SysUserEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8])
        if _dict.get(entity.last_login_time) is None:
            _dict[entity.last_login_time] = list()
        _dict[entity.last_login_time].append(entity)
    return _dict
def select_by_LastActiveTimeList(last_active_time_list,order_by = ' order by sys_user_id desc'):
    _dict = {}
    sql = "select sys_user_id, user_name, pwd, last_login_time, last_active_time, create_time, update_time, last_login_info, remark from v_sys_user" \
          " where last_active_time in (%(last_active_time_list)s)" + order_by
    rts = exesql(sql, {'last_active_time_list':last_active_time_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = SysUserEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8])
        if _dict.get(entity.last_active_time) is None:
            _dict[entity.last_active_time] = list()
        _dict[entity.last_active_time].append(entity)
    return _dict
def select_by_CreateTimeList(create_time_list,order_by = ' order by sys_user_id desc'):
    _dict = {}
    sql = "select sys_user_id, user_name, pwd, last_login_time, last_active_time, create_time, update_time, last_login_info, remark from v_sys_user" \
          " where create_time in (%(create_time_list)s)" + order_by
    rts = exesql(sql, {'create_time_list':create_time_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = SysUserEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8])
        if _dict.get(entity.create_time) is None:
            _dict[entity.create_time] = list()
        _dict[entity.create_time].append(entity)
    return _dict
def select_by_UpdateTimeList(update_time_list,order_by = ' order by sys_user_id desc'):
    _dict = {}
    sql = "select sys_user_id, user_name, pwd, last_login_time, last_active_time, create_time, update_time, last_login_info, remark from v_sys_user" \
          " where update_time in (%(update_time_list)s)" + order_by
    rts = exesql(sql, {'update_time_list':update_time_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = SysUserEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8])
        if _dict.get(entity.update_time) is None:
            _dict[entity.update_time] = list()
        _dict[entity.update_time].append(entity)
    return _dict
def select_by_LastLoginInfoList(last_login_info_list,order_by = ' order by sys_user_id desc'):
    _dict = {}
    sql = "select sys_user_id, user_name, pwd, last_login_time, last_active_time, create_time, update_time, last_login_info, remark from v_sys_user" \
          " where last_login_info in (%(last_login_info_list)s)" + order_by
    rts = exesql(sql, {'last_login_info_list':last_login_info_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = SysUserEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8])
        if _dict.get(entity.last_login_info) is None:
            _dict[entity.last_login_info] = list()
        _dict[entity.last_login_info].append(entity)
    return _dict
def select_by_RemarkList(remark_list,order_by = ' order by sys_user_id desc'):
    _dict = {}
    sql = "select sys_user_id, user_name, pwd, last_login_time, last_active_time, create_time, update_time, last_login_info, remark from v_sys_user" \
          " where remark in (%(remark_list)s)" + order_by
    rts = exesql(sql, {'remark_list':remark_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = SysUserEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8])
        if _dict.get(entity.remark) is None:
            _dict[entity.remark] = list()
        _dict[entity.remark].append(entity)
    return _dict

