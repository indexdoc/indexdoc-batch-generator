from sysdw import exesql

def select_count():
    sql = "select count(*) from view_user_api"
    rts = exesql(sql)
    return int(rts[0][0])

def select_all(order_by = ""):
    sql = "select sys_user_id, sys_api_auth_id, api_url, auth_flag, update_type from view_user_api" + order_by
    rts = exesql(sql)
    rts_list = []
    for tup in rts:
        _dic = {'sys_user_id':tup[0], 'sys_api_auth_id':tup[1], 'api_url':tup[2], 'auth_flag':tup[3], 'update_type':tup[4]}
        rts_list.append(_dic)
    return rts_list

def full_search(search_str, row_cnt = 50000, row_begin=0, order_by = ""):
    if search_str is None or search_str.strip() == '' :
        return None
    _where = "where"
    _limit = " limit %s,%s"%(row_begin,row_cnt)
    attrs = ['sys_user_id','sys_api_auth_id','api_url','auth_flag','update_type']
    for attr in attrs:
        _where += " toString(%s) like '%%%s%%' or"%(attr,search_str)
    _where = _where + ' 1!=1'
    attrstr = 'sys_user_id, sys_api_auth_id, api_url, auth_flag, update_type'
    sql = "select %s from view_user_api "%attrstr + _where + \
          order_by + _limit
    sql_count = "select count(*) from view_user_api " + _where
    _dict_list = []
    rts = exesql(sql)
    rtscnt = exesql(sql_count)
    total_cnt = int(rtscnt[0][0])
    for tup in rts:
        _dic = {'sys_user_id':tup[0], 'sys_api_auth_id':tup[1], 'api_url':tup[2], 'auth_flag':tup[3], 'update_type':tup[4]}
        _dict_list.append(_dic)
    return _dict_list,total_cnt

def select_page(row_cnt, row_begin, search_params,order_by = ""):
    _where = "where"
    attrs = ['sys_user_id','sys_api_auth_id','api_url','auth_flag','update_type']
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
    sql = "select sys_user_id, sys_api_auth_id, api_url, auth_flag, update_type from view_user_api " + _where + \
          order_by + " limit %(row_begin)s,%(row_cnt)s"
    sql_count = "select count(*) from view_user_api " + _where
    _dict_list = []
    rts = exesql(sql,{'row_cnt':row_cnt,'row_begin':row_begin})
    rtscnt = exesql(sql_count)
    total_cnt = int(rtscnt[0][0])
    for tup in rts:
        _dic = {'sys_user_id':tup[0], 'sys_api_auth_id':tup[1], 'api_url':tup[2], 'auth_flag':tup[3], 'update_type':tup[4]}
        _dict_list.append(_dic)
    return _dict_list,total_cnt

def select_by(column_name,search_value,order_by='',row_begin=0,row_cnt=5000):
    _where = "where"
    attrs = ['sys_user_id','sys_api_auth_id','api_url','auth_flag','update_type']
    if column_name in attrs:
        _value = str(search_value).strip()
        if _value != "":
             _value_splits = _value.split(' - ')
             if len(_value_splits) == 2:
                 _where += " %s between '%s' and '%s' and"%(column_name,_value_splits[0],_value_splits[1])
             else:
                 _where += " %s = '%s' and"%(column_name,_value)
    _where = _where + ' 1=1'
    sql = "select sys_user_id, sys_api_auth_id, api_url, auth_flag, update_type from view_user_api " + _where + \
          order_by + " limit %(row_begin)s,%(row_cnt)s"
    sql_count = "select count(*) from view_user_menu " + _where
    _dict_list = []
    rts = exesql(sql,{'row_cnt':row_cnt,'row_begin':row_begin})
    rtscnt = exesql(sql_count)
    total_cnt = int(rtscnt[0][0])
    for tup in rts:
        _dic = {'sys_user_id':tup[0], 'sys_api_auth_id':tup[1], 'api_url':tup[2], 'auth_flag':tup[3], 'update_type':tup[4]}
        _dict_list.append(_dic)
    return _dict_list,total_cnt
