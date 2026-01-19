from sysdw import exesql
from utils import IDUtil
from domain.sysdomain.entity.UserUseLogEntity import UserUseLogEntity

from domain.sysdomain.entity.SysUserEntity import SysUserEntity

# user_use_log_id, sys_user_id, ip_addr, local_ip, api_url, gpu_info, remark, create_time
# tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7]

def insert(entity):
    sql = "insert into phy_user_use_log(user_use_log_id, sys_user_id, ip_addr, local_ip, api_url, gpu_info, remark, create_time,ver_id) values"
    exesql(sql, [(entity.user_use_log_id ,entity.sys_user_id ,entity.ip_addr ,entity.local_ip ,entity.api_url ,entity.gpu_info ,entity.remark ,entity.create_time ,IDUtil.get_long())])
    return entity

def delete_by_id(user_use_log_id):
    sql = """insert into phy_user_use_log(user_use_log_id, sys_user_id, ip_addr, local_ip, api_url, gpu_info, remark, create_time,deleted,ver_id) 
        select user_use_log_id, sys_user_id, ip_addr, local_ip, api_url, gpu_info, remark, create_time,1,%d from v_user_use_log 
        where user_use_log_id = %d"""%(IDUtil.get_long(),user_use_log_id)
    exesql(sql)

def delete(entity):
    delete_by_id(entity.user_use_log_id)

def update(entity):
    return insert(entity)

def update_by_id(user_use_log_id,update_params):
    _entity = select_by_id(user_use_log_id)
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

def full_search(search_str,row_cnt = 50000, row_begin=0, order_by = " order by user_use_log_id desc"):
    if search_str is None or search_str.strip() == '' :
        return None
    _where = "where"
    _limit = " limit %s,%s"%(row_begin,row_cnt)
    attrs = ['user_use_log_id','sys_user_id','ip_addr','local_ip','api_url','gpu_info','remark','create_time']
    for attr in attrs:
        _where += " toString(%s) like '%%%s%%' or"%(attr,search_str)
    _where += " %s like '%%%s%%' or"%("ref_SysUserId_SysUser.2", search_str)
    _where = _where + ' 1!=1'
    _myref_str = ','+UserUseLogEntity.get_myref_tables_str() if UserUseLogEntity.get_myref_tables_str() != '' else ''
    attrstr = 'user_use_log_id, sys_user_id, ip_addr, local_ip, api_url, gpu_info, remark, create_time' +_myref_str
    sql = "select %s from vs_user_use_log "%attrstr + _where + \
          order_by + _limit
    sql_count = "select count(*) from vs_user_use_log " + _where
    entities = []
    rts = exesql(sql)
    rtscnt = exesql(sql_count)
    total_cnt = int(rtscnt[0][0])
    for tup in rts:
        i = 0
        e = UserUseLogEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7])
        i += len(UserUseLogEntity.get_attrcodes())
        stup1 = tup[i];i += 1
        if stup1[0] != 0:
            e.ref_SysUserId_SysUser = SysUserEntity.create_by_tuple(stup1)
        entities.append(e)
    return entities,total_cnt

def select_all(order_by = " order by user_use_log_id desc"):
    entities = []
    sql = "select user_use_log_id, sys_user_id, ip_addr, local_ip, api_url, gpu_info, remark, create_time from v_user_use_log" + order_by
    rts = exesql(sql)
    for tup in rts:
        entities.append(UserUseLogEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7]))
    return entities

def select_count():
    sql = "select count(*) from v_user_use_log"
    rts = exesql(sql)
    return int(rts[0][0])

#获取一页数据的同时也返回本表外键的数据
def select_vspage(row_cnt, row_begin, search_params,order_by = " order by user_use_log_id desc"):
    _where = "where"
    attrs = ['user_use_log_id','sys_user_id','ip_addr','local_ip','api_url','gpu_info','remark','create_time']
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
    _myref_str = ','+UserUseLogEntity.get_myref_tables_str() if UserUseLogEntity.get_myref_tables_str() != '' else ''
    attrstr = 'user_use_log_id, sys_user_id, ip_addr, local_ip, api_url, gpu_info, remark, create_time' +_myref_str
    sql = "select %s from vs_user_use_log "%attrstr + _where + \
          order_by + " limit %(row_begin)s,%(row_cnt)s"
    sql_count = "select count(*) from v_user_use_log " + _where
    entities = []
    rts = exesql(sql,{'row_cnt':row_cnt,'row_begin':row_begin})
    rtscnt = exesql(sql_count)
    total_cnt = int(rtscnt[0][0])
    for tup in rts:
        i = 0
        e = UserUseLogEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7])
        i += len(UserUseLogEntity.get_attrcodes())
        stup1 = tup[i];i += 1
        if stup1[0] != 0:
            e.ref_SysUserId_SysUser = SysUserEntity.create_by_tuple(stup1)
        entities.append(e)
    return entities,total_cnt

def select_page(row_cnt, row_begin, search_params,order_by = " order by user_use_log_id desc"):
    _where = "where"
    attrs = ['user_use_log_id','sys_user_id','ip_addr','local_ip','api_url','gpu_info','remark','create_time']
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
    sql = "select user_use_log_id, sys_user_id, ip_addr, local_ip, api_url, gpu_info, remark, create_time from v_user_use_log " + _where + \
          order_by + " limit %(row_begin)s,%(row_cnt)s"
    sql_count = "select count(*) from v_user_use_log " + _where
    entities = []
    rts = exesql(sql,{'row_cnt':row_cnt,'row_begin':row_begin})
    rtscnt = exesql(sql_count)
    total_cnt = int(rtscnt[0][0])
    for tup in rts:
        entities.append(UserUseLogEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7]))
    return entities,total_cnt

def select_by_id(user_use_log_id):
    sql = "select user_use_log_id, sys_user_id, ip_addr, local_ip, api_url, gpu_info, remark, create_time from  v_user_use_log where user_use_log_id = %(user_use_log_id)s"
    rts = exesql(sql, {'user_use_log_id':user_use_log_id})
    if rts is None or len(rts) == 0:
        return None
    tup = rts[0]
    return UserUseLogEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7])

def select_by_UserUseLogId(user_use_log_id, order_by = ' order by user_use_log_id desc'):
    entities = []
    sql = "select user_use_log_id, sys_user_id, ip_addr, local_ip, api_url, gpu_info, remark, create_time from v_user_use_log " \
          "where user_use_log_id = %(user_use_log_id)s" + order_by
    rts = exesql(sql, {'user_use_log_id':user_use_log_id})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(UserUseLogEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7]))
    return entities
def select_by_SysUserId(sys_user_id, order_by = ' order by user_use_log_id desc'):
    entities = []
    sql = "select user_use_log_id, sys_user_id, ip_addr, local_ip, api_url, gpu_info, remark, create_time from v_user_use_log " \
          "where sys_user_id = %(sys_user_id)s" + order_by
    rts = exesql(sql, {'sys_user_id':sys_user_id})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(UserUseLogEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7]))
    return entities
def select_by_IpAddr(ip_addr, order_by = ' order by user_use_log_id desc'):
    entities = []
    sql = "select user_use_log_id, sys_user_id, ip_addr, local_ip, api_url, gpu_info, remark, create_time from v_user_use_log " \
          "where ip_addr = %(ip_addr)s" + order_by
    rts = exesql(sql, {'ip_addr':ip_addr})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(UserUseLogEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7]))
    return entities
def select_by_LocalIp(local_ip, order_by = ' order by user_use_log_id desc'):
    entities = []
    sql = "select user_use_log_id, sys_user_id, ip_addr, local_ip, api_url, gpu_info, remark, create_time from v_user_use_log " \
          "where local_ip = %(local_ip)s" + order_by
    rts = exesql(sql, {'local_ip':local_ip})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(UserUseLogEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7]))
    return entities
def select_by_ApiUrl(api_url, order_by = ' order by user_use_log_id desc'):
    entities = []
    sql = "select user_use_log_id, sys_user_id, ip_addr, local_ip, api_url, gpu_info, remark, create_time from v_user_use_log " \
          "where api_url = %(api_url)s" + order_by
    rts = exesql(sql, {'api_url':api_url})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(UserUseLogEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7]))
    return entities
def select_by_GpuInfo(gpu_info, order_by = ' order by user_use_log_id desc'):
    entities = []
    sql = "select user_use_log_id, sys_user_id, ip_addr, local_ip, api_url, gpu_info, remark, create_time from v_user_use_log " \
          "where gpu_info = %(gpu_info)s" + order_by
    rts = exesql(sql, {'gpu_info':gpu_info})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(UserUseLogEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7]))
    return entities
def select_by_Remark(remark, order_by = ' order by user_use_log_id desc'):
    entities = []
    sql = "select user_use_log_id, sys_user_id, ip_addr, local_ip, api_url, gpu_info, remark, create_time from v_user_use_log " \
          "where remark = %(remark)s" + order_by
    rts = exesql(sql, {'remark':remark})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(UserUseLogEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7]))
    return entities
def select_by_CreateTime(create_time, order_by = ' order by user_use_log_id desc'):
    entities = []
    sql = "select user_use_log_id, sys_user_id, ip_addr, local_ip, api_url, gpu_info, remark, create_time from v_user_use_log " \
          "where create_time = %(create_time)s" + order_by
    rts = exesql(sql, {'create_time':create_time})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(UserUseLogEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7]))
    return entities

def select_by_UserUseLogIdList(user_use_log_id_list,order_by = ' order by user_use_log_id desc'):
    _dict = {}
    sql = "select user_use_log_id, sys_user_id, ip_addr, local_ip, api_url, gpu_info, remark, create_time from v_user_use_log" \
          " where user_use_log_id in (%(user_use_log_id_list)s)" + order_by
    rts = exesql(sql, {'user_use_log_id_list':user_use_log_id_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = UserUseLogEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7])
        if _dict.get(entity.user_use_log_id) is None:
            _dict[entity.user_use_log_id] = list()
        _dict[entity.user_use_log_id].append(entity)
    return _dict
def select_by_SysUserIdList(sys_user_id_list,order_by = ' order by user_use_log_id desc'):
    _dict = {}
    sql = "select user_use_log_id, sys_user_id, ip_addr, local_ip, api_url, gpu_info, remark, create_time from v_user_use_log" \
          " where sys_user_id in (%(sys_user_id_list)s)" + order_by
    rts = exesql(sql, {'sys_user_id_list':sys_user_id_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = UserUseLogEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7])
        if _dict.get(entity.sys_user_id) is None:
            _dict[entity.sys_user_id] = list()
        _dict[entity.sys_user_id].append(entity)
    return _dict
def select_by_IpAddrList(ip_addr_list,order_by = ' order by user_use_log_id desc'):
    _dict = {}
    sql = "select user_use_log_id, sys_user_id, ip_addr, local_ip, api_url, gpu_info, remark, create_time from v_user_use_log" \
          " where ip_addr in (%(ip_addr_list)s)" + order_by
    rts = exesql(sql, {'ip_addr_list':ip_addr_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = UserUseLogEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7])
        if _dict.get(entity.ip_addr) is None:
            _dict[entity.ip_addr] = list()
        _dict[entity.ip_addr].append(entity)
    return _dict
def select_by_LocalIpList(local_ip_list,order_by = ' order by user_use_log_id desc'):
    _dict = {}
    sql = "select user_use_log_id, sys_user_id, ip_addr, local_ip, api_url, gpu_info, remark, create_time from v_user_use_log" \
          " where local_ip in (%(local_ip_list)s)" + order_by
    rts = exesql(sql, {'local_ip_list':local_ip_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = UserUseLogEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7])
        if _dict.get(entity.local_ip) is None:
            _dict[entity.local_ip] = list()
        _dict[entity.local_ip].append(entity)
    return _dict
def select_by_ApiUrlList(api_url_list,order_by = ' order by user_use_log_id desc'):
    _dict = {}
    sql = "select user_use_log_id, sys_user_id, ip_addr, local_ip, api_url, gpu_info, remark, create_time from v_user_use_log" \
          " where api_url in (%(api_url_list)s)" + order_by
    rts = exesql(sql, {'api_url_list':api_url_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = UserUseLogEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7])
        if _dict.get(entity.api_url) is None:
            _dict[entity.api_url] = list()
        _dict[entity.api_url].append(entity)
    return _dict
def select_by_GpuInfoList(gpu_info_list,order_by = ' order by user_use_log_id desc'):
    _dict = {}
    sql = "select user_use_log_id, sys_user_id, ip_addr, local_ip, api_url, gpu_info, remark, create_time from v_user_use_log" \
          " where gpu_info in (%(gpu_info_list)s)" + order_by
    rts = exesql(sql, {'gpu_info_list':gpu_info_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = UserUseLogEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7])
        if _dict.get(entity.gpu_info) is None:
            _dict[entity.gpu_info] = list()
        _dict[entity.gpu_info].append(entity)
    return _dict
def select_by_RemarkList(remark_list,order_by = ' order by user_use_log_id desc'):
    _dict = {}
    sql = "select user_use_log_id, sys_user_id, ip_addr, local_ip, api_url, gpu_info, remark, create_time from v_user_use_log" \
          " where remark in (%(remark_list)s)" + order_by
    rts = exesql(sql, {'remark_list':remark_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = UserUseLogEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7])
        if _dict.get(entity.remark) is None:
            _dict[entity.remark] = list()
        _dict[entity.remark].append(entity)
    return _dict
def select_by_CreateTimeList(create_time_list,order_by = ' order by user_use_log_id desc'):
    _dict = {}
    sql = "select user_use_log_id, sys_user_id, ip_addr, local_ip, api_url, gpu_info, remark, create_time from v_user_use_log" \
          " where create_time in (%(create_time_list)s)" + order_by
    rts = exesql(sql, {'create_time_list':create_time_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = UserUseLogEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7])
        if _dict.get(entity.create_time) is None:
            _dict[entity.create_time] = list()
        _dict[entity.create_time].append(entity)
    return _dict

