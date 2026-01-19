from sysdw import exesql
from utils import IDUtil
from domain.doc_assistant.entity.ExcelTemplateEntity import ExcelTemplateEntity

from domain.sysdomain.entity.UserFileEntity import UserFileEntity

# excel_template_id, user_file_id, create_time
# tup[0], tup[1], tup[2]

def insert(entity):
    sql = "insert into phy_excel_template(excel_template_id, user_file_id, create_time,ver_id) values"
    exesql(sql, [(entity.excel_template_id ,entity.user_file_id ,entity.create_time ,IDUtil.get_long())])
    return entity

def delete_by_id(excel_template_id):
    sql = """insert into phy_excel_template(excel_template_id, user_file_id, create_time,deleted,ver_id) 
        select excel_template_id, user_file_id, create_time,1,%d from v_excel_template 
        where excel_template_id = %d"""%(IDUtil.get_long(),excel_template_id)
    exesql(sql)

def delete(entity):
    delete_by_id(entity.excel_template_id)

def update(entity):
    return insert(entity)

def update_by_id(excel_template_id,update_params):
    _entity = select_by_id(excel_template_id)
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

def full_search(search_str,row_cnt = 50000, row_begin=0, order_by = " order by excel_template_id desc"):
    if search_str is None or search_str.strip() == '' :
        return None
    _where = "where"
    _limit = " limit %s,%s"%(row_begin,row_cnt)
    attrs = ['excel_template_id','user_file_id','create_time']
    for attr in attrs:
        _where += " toString(%s) like '%%%s%%' or"%(attr,search_str)
    _where += " %s like '%%%s%%' or"%("ref_UserFileId_UserFile.4", search_str)
    _where = _where + ' 1!=1'
    _myref_str = ','+ExcelTemplateEntity.get_myref_tables_str() if ExcelTemplateEntity.get_myref_tables_str() != '' else ''
    attrstr = 'excel_template_id, user_file_id, create_time' +_myref_str
    sql = "select %s from vs_excel_template "%attrstr + _where + \
          order_by + _limit
    sql_count = "select count(*) from vs_excel_template " + _where
    entities = []
    rts = exesql(sql)
    rtscnt = exesql(sql_count)
    total_cnt = int(rtscnt[0][0])
    for tup in rts:
        i = 0
        e = ExcelTemplateEntity(tup[0], tup[1], tup[2])
        i += len(ExcelTemplateEntity.get_attrcodes())
        stup1 = tup[i];i += 1
        if stup1[0] != 0:
            e.ref_UserFileId_UserFile = UserFileEntity.create_by_tuple(stup1)
        entities.append(e)
    return entities,total_cnt

def select_all(order_by = " order by excel_template_id desc"):
    entities = []
    sql = "select excel_template_id, user_file_id, create_time from v_excel_template" + order_by
    rts = exesql(sql)
    for tup in rts:
        entities.append(ExcelTemplateEntity(tup[0], tup[1], tup[2]))
    return entities

def select_count():
    sql = "select count(*) from v_excel_template"
    rts = exesql(sql)
    return int(rts[0][0])

#获取一页数据的同时也返回本表外键的数据
def select_vspage(row_cnt, row_begin, search_params,order_by = " order by excel_template_id desc"):
    _where = "where"
    attrs = ['excel_template_id','user_file_id','create_time']
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
    _myref_str = ','+ExcelTemplateEntity.get_myref_tables_str() if ExcelTemplateEntity.get_myref_tables_str() != '' else ''
    attrstr = 'excel_template_id, user_file_id, create_time' +_myref_str
    sql = "select %s from vs_excel_template "%attrstr + _where + \
          order_by + " limit %(row_begin)s,%(row_cnt)s"
    sql_count = "select count(*) from v_excel_template " + _where
    entities = []
    rts = exesql(sql,{'row_cnt':row_cnt,'row_begin':row_begin})
    rtscnt = exesql(sql_count)
    total_cnt = int(rtscnt[0][0])
    for tup in rts:
        i = 0
        e = ExcelTemplateEntity(tup[0], tup[1], tup[2])
        i += len(ExcelTemplateEntity.get_attrcodes())
        stup1 = tup[i];i += 1
        if stup1[0] != 0:
            e.ref_UserFileId_UserFile = UserFileEntity.create_by_tuple(stup1)
        entities.append(e)
    return entities,total_cnt

def select_page(row_cnt, row_begin, search_params,order_by = " order by excel_template_id desc"):
    _where = "where"
    attrs = ['excel_template_id','user_file_id','create_time']
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
    sql = "select excel_template_id, user_file_id, create_time from v_excel_template " + _where + \
          order_by + " limit %(row_begin)s,%(row_cnt)s"
    sql_count = "select count(*) from v_excel_template " + _where
    entities = []
    rts = exesql(sql,{'row_cnt':row_cnt,'row_begin':row_begin})
    rtscnt = exesql(sql_count)
    total_cnt = int(rtscnt[0][0])
    for tup in rts:
        entities.append(ExcelTemplateEntity(tup[0], tup[1], tup[2]))
    return entities,total_cnt

def select_by_id(excel_template_id):
    sql = "select excel_template_id, user_file_id, create_time from  v_excel_template where excel_template_id = %(excel_template_id)s"
    rts = exesql(sql, {'excel_template_id':excel_template_id})
    if rts is None or len(rts) == 0:
        return None
    tup = rts[0]
    return ExcelTemplateEntity(tup[0], tup[1], tup[2])

def select_by_ExcelTemplateId(excel_template_id, order_by = ' order by excel_template_id desc'):
    entities = []
    sql = "select excel_template_id, user_file_id, create_time from v_excel_template " \
          "where excel_template_id = %(excel_template_id)s" + order_by
    rts = exesql(sql, {'excel_template_id':excel_template_id})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(ExcelTemplateEntity(tup[0], tup[1], tup[2]))
    return entities
def select_by_UserFileId(user_file_id, order_by = ' order by excel_template_id desc'):
    entities = []
    sql = "select excel_template_id, user_file_id, create_time from v_excel_template " \
          "where user_file_id = %(user_file_id)s" + order_by
    rts = exesql(sql, {'user_file_id':user_file_id})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(ExcelTemplateEntity(tup[0], tup[1], tup[2]))
    return entities
def select_by_CreateTime(create_time, order_by = ' order by excel_template_id desc'):
    entities = []
    sql = "select excel_template_id, user_file_id, create_time from v_excel_template " \
          "where create_time = %(create_time)s" + order_by
    rts = exesql(sql, {'create_time':create_time})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(ExcelTemplateEntity(tup[0], tup[1], tup[2]))
    return entities

def select_by_ExcelTemplateIdList(excel_template_id_list,order_by = ' order by excel_template_id desc'):
    _dict = {}
    sql = "select excel_template_id, user_file_id, create_time from v_excel_template" \
          " where excel_template_id in (%(excel_template_id_list)s)" + order_by
    rts = exesql(sql, {'excel_template_id_list':excel_template_id_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = ExcelTemplateEntity(tup[0], tup[1], tup[2])
        if _dict.get(entity.excel_template_id) is None:
            _dict[entity.excel_template_id] = list()
        _dict[entity.excel_template_id].append(entity)
    return _dict
def select_by_UserFileIdList(user_file_id_list,order_by = ' order by excel_template_id desc'):
    _dict = {}
    sql = "select excel_template_id, user_file_id, create_time from v_excel_template" \
          " where user_file_id in (%(user_file_id_list)s)" + order_by
    rts = exesql(sql, {'user_file_id_list':user_file_id_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = ExcelTemplateEntity(tup[0], tup[1], tup[2])
        if _dict.get(entity.user_file_id) is None:
            _dict[entity.user_file_id] = list()
        _dict[entity.user_file_id].append(entity)
    return _dict
def select_by_CreateTimeList(create_time_list,order_by = ' order by excel_template_id desc'):
    _dict = {}
    sql = "select excel_template_id, user_file_id, create_time from v_excel_template" \
          " where create_time in (%(create_time_list)s)" + order_by
    rts = exesql(sql, {'create_time_list':create_time_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = ExcelTemplateEntity(tup[0], tup[1], tup[2])
        if _dict.get(entity.create_time) is None:
            _dict[entity.create_time] = list()
        _dict[entity.create_time].append(entity)
    return _dict

