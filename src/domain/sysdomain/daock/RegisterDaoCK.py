from sysdw import exesql
from utils import IDUtil
from domain.sysdomain.entity.RegisterEntity import RegisterEntity

from domain.sysdomain.entity.SysUserEntity import SysUserEntity


# register_id, sys_user_id, phone_no, name, user_name, company_name, pwd, status, create_time, update_time, remark
# tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9], tup[10]

def insert(entity):
    sql = "insert into phy_register(register_id, sys_user_id, phone_no, name, user_name, company_name, pwd, status, create_time, update_time, remark,ver_id) values"
    exesql(sql, [(entity.register_id, entity.sys_user_id, entity.phone_no, entity.name, entity.user_name,
                  entity.company_name, entity.pwd, entity.status, entity.create_time, entity.update_time, entity.remark,
                  IDUtil.get_long())])
    return entity


def delete_by_id(register_id):
    sql = """insert into phy_register(register_id, sys_user_id, phone_no, name, user_name, company_name, pwd, status, create_time, update_time, remark,deleted,ver_id) 
        select register_id, sys_user_id, phone_no, name, user_name, company_name, pwd, status, create_time, update_time, remark,1,%d from v_register 
        where register_id = %d""" % (IDUtil.get_long(), register_id)
    exesql(sql)


def delete(entity):
    delete_by_id(entity.register_id)


def update(entity):
    return insert(entity)


def update_by_id(register_id, update_params):
    _entity = select_by_id(register_id)
    if _entity is None:
        return None
    if update_params is None:
        return _entity
    if len(update_params) == 0:
        return _entity
    for param in update_params.keys():
        if hasattr(_entity, param):
            _value = update_params[param]
            setattr(_entity, param, _value)
    return update(_entity)


def full_search(search_str, row_cnt=50000, row_begin=0, order_by=" order by register_id desc"):
    if search_str is None or search_str.strip() == '':
        return None
    _where = "where"
    _limit = " limit %s,%s" % (row_begin, row_cnt)
    attrs = ['register_id', 'sys_user_id', 'phone_no', 'name', 'user_name', 'company_name', 'pwd', 'status',
             'create_time', 'update_time', 'remark']
    for attr in attrs:
        _where += " toString(%s) like '%%%s%%' or" % (attr, search_str)
    _where += " %s like '%%%s%%' or" % ("ref_SysUserId_SysUser.2", search_str)
    _where = _where + ' 1!=1'
    _myref_str = ',' + RegisterEntity.get_myref_tables_str() if RegisterEntity.get_myref_tables_str() != '' else ''
    attrstr = 'register_id, sys_user_id, phone_no, name, user_name, company_name, pwd, status, create_time, update_time, remark' + _myref_str
    sql = "select %s from vs_register " % attrstr + _where + \
          order_by + _limit
    sql_count = "select count(*) from vs_register " + _where
    entities = []
    rts = exesql(sql)
    rtscnt = exesql(sql_count)
    total_cnt = int(rtscnt[0][0])
    for tup in rts:
        i = 0
        e = RegisterEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9], tup[10])
        i += len(RegisterEntity.get_attrcodes())
        stup1 = tup[i];
        i += 1
        if stup1[0] != 0:
            e.ref_SysUserId_SysUser = SysUserEntity.create_by_tuple(stup1)
        entities.append(e)
    return entities, total_cnt


def select_all(order_by=" order by register_id desc"):
    entities = []
    sql = "select register_id, sys_user_id, phone_no, name, user_name, company_name, pwd, status, create_time, update_time, remark from v_register" + order_by
    rts = exesql(sql)
    for tup in rts:
        entities.append(
            RegisterEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9], tup[10]))
    return entities


def select_count():
    sql = "select count(*) from v_register"
    rts = exesql(sql)
    return int(rts[0][0])


# 获取一页数据的同时也返回本表外键的数据
def select_vspage(row_cnt, row_begin, search_params, order_by=" order by register_id desc"):
    _where = "where"
    attrs = ['register_id', 'sys_user_id', 'phone_no', 'name', 'user_name', 'company_name', 'pwd', 'status',
             'create_time', 'update_time', 'remark']
    if search_params is not None:
        for param in search_params.keys():
            if param in attrs:
                _value = str(search_params[param]).strip()
                if _value != "":
                    _value_splits = _value.split(' - ')
                    if len(_value_splits) == 2:
                        _where += " %s between '%s' and '%s' and" % (param, _value_splits[0], _value_splits[1])
                    else:
                        _where += " %s = '%s' and" % (param, _value)
    _where = _where + ' 1=1'
    _myref_str = ',' + RegisterEntity.get_myref_tables_str() if RegisterEntity.get_myref_tables_str() != '' else ''
    attrstr = 'register_id, sys_user_id, phone_no, name, user_name, company_name, pwd, status, create_time, update_time, remark' + _myref_str
    sql = "select %s from vs_register " % attrstr + _where + \
          order_by + " limit %(row_begin)s,%(row_cnt)s"
    sql_count = "select count(*) from v_register " + _where
    entities = []
    rts = exesql(sql, {'row_cnt': row_cnt, 'row_begin': row_begin})
    rtscnt = exesql(sql_count)
    total_cnt = int(rtscnt[0][0])
    for tup in rts:
        i = 0
        e = RegisterEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9], tup[10])
        i += len(RegisterEntity.get_attrcodes())
        stup1 = tup[i];
        i += 1
        if stup1[0] != 0:
            e.ref_SysUserId_SysUser = SysUserEntity.create_by_tuple(stup1)
        entities.append(e)
    return entities, total_cnt


def select_page(row_cnt, row_begin, search_params, order_by=" order by register_id desc"):
    _where = "where"
    attrs = ['register_id', 'sys_user_id', 'phone_no', 'name', 'user_name', 'company_name', 'pwd', 'status',
             'create_time', 'update_time', 'remark']
    if search_params is not None:
        for param in search_params.keys():
            if param in attrs:
                _value = str(search_params[param]).strip()
                if _value != "":
                    _value_splits = _value.split(' - ')
                    if len(_value_splits) == 2:
                        _where += " %s between '%s' and '%s' and" % (param, _value_splits[0], _value_splits[1])
                    else:
                        _where += " %s = '%s' and" % (param, _value)
    _where = _where + ' 1=1'
    sql = "select register_id, sys_user_id, phone_no, name, user_name, company_name, pwd, status, create_time, update_time, remark from v_register " + _where + \
          order_by + " limit %(row_begin)s,%(row_cnt)s"
    sql_count = "select count(*) from v_register " + _where
    entities = []
    rts = exesql(sql, {'row_cnt': row_cnt, 'row_begin': row_begin})
    rtscnt = exesql(sql_count)
    total_cnt = int(rtscnt[0][0])
    for tup in rts:
        entities.append(
            RegisterEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9], tup[10]))
    return entities, total_cnt


def select_by_id(register_id):
    sql = "select register_id, sys_user_id, phone_no, name, user_name, company_name, pwd, status, create_time, update_time, remark from  v_register where register_id = %(register_id)s"
    rts = exesql(sql, {'register_id': register_id})
    if rts is None or len(rts) == 0:
        return None
    tup = rts[0]
    return RegisterEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9], tup[10])


def select_by_RegisterId(register_id, order_by=' order by register_id desc'):
    entities = []
    sql = "select register_id, sys_user_id, phone_no, name, user_name, company_name, pwd, status, create_time, update_time, remark from v_register " \
          "where register_id = %(register_id)s" + order_by
    rts = exesql(sql, {'register_id': register_id})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(
            RegisterEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9], tup[10]))
    return entities


def select_by_SysUserId(sys_user_id, order_by=' order by register_id desc'):
    entities = []
    sql = "select register_id, sys_user_id, phone_no, name, user_name, company_name, pwd, status, create_time, update_time, remark from v_register " \
          "where sys_user_id = %(sys_user_id)s" + order_by
    rts = exesql(sql, {'sys_user_id': sys_user_id})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(
            RegisterEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9], tup[10]))
    return entities


def select_by_PhoneNo(phone_no, order_by=' order by register_id desc'):
    entities = []
    sql = "select register_id, sys_user_id, phone_no, name, user_name, company_name, pwd, status, create_time, update_time, remark from v_register " \
          "where phone_no = %(phone_no)s" + order_by
    rts = exesql(sql, {'phone_no': phone_no})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(
            RegisterEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9], tup[10]))
    return entities


def select_by_Name(name, order_by=' order by register_id desc'):
    entities = []
    sql = "select register_id, sys_user_id, phone_no, name, user_name, company_name, pwd, status, create_time, update_time, remark from v_register " \
          "where name = %(name)s" + order_by
    rts = exesql(sql, {'name': name})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(
            RegisterEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9], tup[10]))
    return entities


def select_by_UserName(user_name, order_by=' order by register_id desc'):
    entities = []
    sql = "select register_id, sys_user_id, phone_no, name, user_name, company_name, pwd, status, create_time, update_time, remark from v_register " \
          "where user_name = %(user_name)s" + order_by
    rts = exesql(sql, {'user_name': user_name})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(
            RegisterEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9], tup[10]))
    return entities


def select_by_CompanyName(company_name, order_by=' order by register_id desc'):
    entities = []
    sql = "select register_id, sys_user_id, phone_no, name, user_name, company_name, pwd, status, create_time, update_time, remark from v_register " \
          "where company_name = %(company_name)s" + order_by
    rts = exesql(sql, {'company_name': company_name})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(
            RegisterEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9], tup[10]))
    return entities


def select_by_Pwd(pwd, order_by=' order by register_id desc'):
    entities = []
    sql = "select register_id, sys_user_id, phone_no, name, user_name, company_name, pwd, status, create_time, update_time, remark from v_register " \
          "where pwd = %(pwd)s" + order_by
    rts = exesql(sql, {'pwd': pwd})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(
            RegisterEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9], tup[10]))
    return entities


def select_by_Status(status, order_by=' order by register_id desc'):
    entities = []
    sql = "select register_id, sys_user_id, phone_no, name, user_name, company_name, pwd, status, create_time, update_time, remark from v_register " \
          "where status = %(status)s" + order_by
    rts = exesql(sql, {'status': status})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(
            RegisterEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9], tup[10]))
    return entities


def select_by_CreateTime(create_time, order_by=' order by register_id desc'):
    entities = []
    sql = "select register_id, sys_user_id, phone_no, name, user_name, company_name, pwd, status, create_time, update_time, remark from v_register " \
          "where create_time = %(create_time)s" + order_by
    rts = exesql(sql, {'create_time': create_time})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(
            RegisterEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9], tup[10]))
    return entities


def select_by_UpdateTime(update_time, order_by=' order by register_id desc'):
    entities = []
    sql = "select register_id, sys_user_id, phone_no, name, user_name, company_name, pwd, status, create_time, update_time, remark from v_register " \
          "where update_time = %(update_time)s" + order_by
    rts = exesql(sql, {'update_time': update_time})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(
            RegisterEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9], tup[10]))
    return entities


def select_by_Remark(remark, order_by=' order by register_id desc'):
    entities = []
    sql = "select register_id, sys_user_id, phone_no, name, user_name, company_name, pwd, status, create_time, update_time, remark from v_register " \
          "where remark = %(remark)s" + order_by
    rts = exesql(sql, {'remark': remark})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(
            RegisterEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9], tup[10]))
    return entities


def select_by_RegisterIdList(register_id_list, order_by=' order by register_id desc'):
    _dict = {}
    sql = "select register_id, sys_user_id, phone_no, name, user_name, company_name, pwd, status, create_time, update_time, remark from v_register" \
          " where register_id in (%(register_id_list)s)" + order_by
    rts = exesql(sql, {'register_id_list': register_id_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = RegisterEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9], tup[10])
        if _dict.get(entity.register_id) is None:
            _dict[entity.register_id] = list()
        _dict[entity.register_id].append(entity)
    return _dict


def select_by_SysUserIdList(sys_user_id_list, order_by=' order by register_id desc'):
    _dict = {}
    sql = "select register_id, sys_user_id, phone_no, name, user_name, company_name, pwd, status, create_time, update_time, remark from v_register" \
          " where sys_user_id in (%(sys_user_id_list)s)" + order_by
    rts = exesql(sql, {'sys_user_id_list': sys_user_id_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = RegisterEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9], tup[10])
        if _dict.get(entity.sys_user_id) is None:
            _dict[entity.sys_user_id] = list()
        _dict[entity.sys_user_id].append(entity)
    return _dict


def select_by_PhoneNoList(phone_no_list, order_by=' order by register_id desc'):
    _dict = {}
    sql = "select register_id, sys_user_id, phone_no, name, user_name, company_name, pwd, status, create_time, update_time, remark from v_register" \
          " where phone_no in (%(phone_no_list)s)" + order_by
    rts = exesql(sql, {'phone_no_list': phone_no_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = RegisterEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9], tup[10])
        if _dict.get(entity.phone_no) is None:
            _dict[entity.phone_no] = list()
        _dict[entity.phone_no].append(entity)
    return _dict


def select_by_NameList(name_list, order_by=' order by register_id desc'):
    _dict = {}
    sql = "select register_id, sys_user_id, phone_no, name, user_name, company_name, pwd, status, create_time, update_time, remark from v_register" \
          " where name in (%(name_list)s)" + order_by
    rts = exesql(sql, {'name_list': name_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = RegisterEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9], tup[10])
        if _dict.get(entity.name) is None:
            _dict[entity.name] = list()
        _dict[entity.name].append(entity)
    return _dict


def select_by_UserNameList(user_name_list, order_by=' order by register_id desc'):
    _dict = {}
    sql = "select register_id, sys_user_id, phone_no, name, user_name, company_name, pwd, status, create_time, update_time, remark from v_register" \
          " where user_name in (%(user_name_list)s)" + order_by
    rts = exesql(sql, {'user_name_list': user_name_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = RegisterEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9], tup[10])
        if _dict.get(entity.user_name) is None:
            _dict[entity.user_name] = list()
        _dict[entity.user_name].append(entity)
    return _dict


def select_by_CompanyNameList(company_name_list, order_by=' order by register_id desc'):
    _dict = {}
    sql = "select register_id, sys_user_id, phone_no, name, user_name, company_name, pwd, status, create_time, update_time, remark from v_register" \
          " where company_name in (%(company_name_list)s)" + order_by
    rts = exesql(sql, {'company_name_list': company_name_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = RegisterEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9], tup[10])
        if _dict.get(entity.company_name) is None:
            _dict[entity.company_name] = list()
        _dict[entity.company_name].append(entity)
    return _dict


def select_by_PwdList(pwd_list, order_by=' order by register_id desc'):
    _dict = {}
    sql = "select register_id, sys_user_id, phone_no, name, user_name, company_name, pwd, status, create_time, update_time, remark from v_register" \
          " where pwd in (%(pwd_list)s)" + order_by
    rts = exesql(sql, {'pwd_list': pwd_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = RegisterEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9], tup[10])
        if _dict.get(entity.pwd) is None:
            _dict[entity.pwd] = list()
        _dict[entity.pwd].append(entity)
    return _dict


def select_by_StatusList(status_list, order_by=' order by register_id desc'):
    _dict = {}
    sql = "select register_id, sys_user_id, phone_no, name, user_name, company_name, pwd, status, create_time, update_time, remark from v_register" \
          " where status in (%(status_list)s)" + order_by
    rts = exesql(sql, {'status_list': status_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = RegisterEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9], tup[10])
        if _dict.get(entity.status) is None:
            _dict[entity.status] = list()
        _dict[entity.status].append(entity)
    return _dict


def select_by_CreateTimeList(create_time_list, order_by=' order by register_id desc'):
    _dict = {}
    sql = "select register_id, sys_user_id, phone_no, name, user_name, company_name, pwd, status, create_time, update_time, remark from v_register" \
          " where create_time in (%(create_time_list)s)" + order_by
    rts = exesql(sql, {'create_time_list': create_time_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = RegisterEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9], tup[10])
        if _dict.get(entity.create_time) is None:
            _dict[entity.create_time] = list()
        _dict[entity.create_time].append(entity)
    return _dict


def select_by_UpdateTimeList(update_time_list, order_by=' order by register_id desc'):
    _dict = {}
    sql = "select register_id, sys_user_id, phone_no, name, user_name, company_name, pwd, status, create_time, update_time, remark from v_register" \
          " where update_time in (%(update_time_list)s)" + order_by
    rts = exesql(sql, {'update_time_list': update_time_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = RegisterEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9], tup[10])
        if _dict.get(entity.update_time) is None:
            _dict[entity.update_time] = list()
        _dict[entity.update_time].append(entity)
    return _dict


def select_by_RemarkList(remark_list, order_by=' order by register_id desc'):
    _dict = {}
    sql = "select register_id, sys_user_id, phone_no, name, user_name, company_name, pwd, status, create_time, update_time, remark from v_register" \
          " where remark in (%(remark_list)s)" + order_by
    rts = exesql(sql, {'remark_list': remark_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = RegisterEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9], tup[10])
        if _dict.get(entity.remark) is None:
            _dict[entity.remark] = list()
        _dict[entity.remark].append(entity)
    return _dict
