from sysdw import exesql


def select_count():
    sql = "select count(*) from view_user_use_num"
    rts = exesql(sql)
    return int(rts[0][0])


def select_all(order_by=""):
    sql = "select ip_addr, local_ip, gpu_info from view_user_use_num" + order_by
    rts = exesql(sql)
    rts_list = []
    for tup in rts:
        _dic = {'ip_addr': tup[0], 'local_ip': tup[1], 'gpu_info': tup[2]}
        rts_list.append(_dic)
    return rts_list


def select_all_num(ip_addr, gpu_info, order_by=""):
    sql = f"select ip_addr, gpu_info from view_user_use_num where ip_addr = '{ip_addr}' and gpu_info = '{gpu_info}'" + order_by
    rts = exesql(sql)
    rts_list = []
    for tup in rts:
        _dic = {'ip_addr': tup[0], 'gpu_info': tup[1]}
        rts_list.append(_dic)
    return rts_list


def full_search(search_str, row_cnt=50000, row_begin=0, order_by=""):
    if search_str is None or search_str.strip() == '':
        return None
    _where = "where"
    _limit = " limit %s,%s" % (row_begin, row_cnt)
    attrs = ['ip_addr', 'local_ip', 'gpu_info']
    for attr in attrs:
        _where += " toString(%s) like '%%%s%%' or" % (attr, search_str)
    _where = _where + ' 1!=1'
    attrstr = 'ip_addr, local_ip, gpu_info'
    sql = "select %s from view_user_use_num " % attrstr + _where + \
          order_by + _limit
    sql_count = "select count(*) from view_user_use_num " + _where
    _dict_list = []
    rts = exesql(sql)
    rtscnt = exesql(sql_count)
    total_cnt = int(rtscnt[0][0])
    for tup in rts:
        _dic = {'ip_addr': tup[0], 'local_ip': tup[1], 'gpu_info': tup[2]}
        _dict_list.append(_dic)
    return _dict_list, total_cnt


def select_page(row_cnt, row_begin, search_params, order_by=""):
    _where = "where"
    attrs = ['ip_addr', 'local_ip', 'gpu_info']
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
    sql = "select ip_addr, local_ip, gpu_info from view_user_use_num " + _where + \
          order_by + " limit %(row_begin)s,%(row_cnt)s"
    sql_count = "select count(*) from view_user_use_num " + _where
    _dict_list = []
    rts = exesql(sql, {'row_cnt': row_cnt, 'row_begin': row_begin})
    rtscnt = exesql(sql_count)
    total_cnt = int(rtscnt[0][0])
    for tup in rts:
        _dic = {'ip_addr': tup[0], 'local_ip': tup[1], 'gpu_info': tup[2]}
        _dict_list.append(_dic)
    return _dict_list, total_cnt


def select_by(column_name, search_value, order_by='', row_begin=0, row_cnt=5000):
    _where = "where"
    attrs = ['ip_addr', 'local_ip', 'gpu_info']
    if column_name in attrs:
        _value = str(search_value).strip()
        if _value != "":
            _value_splits = _value.split(' - ')
            if len(_value_splits) == 2:
                _where += " %s between '%s' and '%s' and" % (column_name, _value_splits[0], _value_splits[1])
            else:
                _where += " %s = '%s' and" % (column_name, _value)
    _where = _where + ' 1=1'
    sql = "select ip_addr, local_ip, gpu_info from view_user_use_num " + _where + \
          order_by + " limit %(row_begin)s,%(row_cnt)s"
    sql_count = "select count(*) from view_user_menu " + _where
    _dict_list = []
    rts = exesql(sql, {'row_cnt': row_cnt, 'row_begin': row_begin})
    rtscnt = exesql(sql_count)
    total_cnt = int(rtscnt[0][0])
    for tup in rts:
        _dic = {'ip_addr': tup[0], 'local_ip': tup[1], 'gpu_info': tup[2]}
        _dict_list.append(_dic)
    return _dict_list, total_cnt
