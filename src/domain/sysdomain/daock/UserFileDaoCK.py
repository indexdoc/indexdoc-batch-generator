from sysdw import exesql
from utils import IDUtil
from domain.sysdomain.entity.UserFileEntity import UserFileEntity

from domain.sysdomain.entity.SysUserEntity import SysUserEntity

# user_file_id, file_uuid, upload_user_id, file_name, file_type, content_type, file_storage, cdn_url, file_suffix, file_content, file_preview, file_summary, upload_time
# tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9], tup[10], tup[11], tup[12]

def insert(entity):
    sql = "insert into phy_user_file(user_file_id, file_uuid, upload_user_id, file_name, file_type, content_type, file_storage, cdn_url, file_suffix, file_content, file_preview, file_summary, upload_time,ver_id) values"
    exesql(sql, [(entity.user_file_id ,entity.file_uuid ,entity.upload_user_id ,entity.file_name ,entity.file_type ,entity.content_type ,entity.file_storage ,entity.cdn_url ,entity.file_suffix ,entity.file_content ,entity.file_preview ,entity.file_summary ,entity.upload_time ,IDUtil.get_long())])
    return entity

def delete_by_id(user_file_id):
    sql = """insert into phy_user_file(user_file_id, file_uuid, upload_user_id, file_name, file_type, content_type, file_storage, cdn_url, file_suffix, file_content, file_preview, file_summary, upload_time,deleted,ver_id) 
        select user_file_id, file_uuid, upload_user_id, file_name, file_type, content_type, file_storage, cdn_url, file_suffix, file_content, file_preview, file_summary, upload_time,1,%d from v_user_file 
        where user_file_id = %d"""%(IDUtil.get_long(),user_file_id)
    exesql(sql)

def delete(entity):
    delete_by_id(entity.user_file_id)

def update(entity):
    return insert(entity)

def update_by_id(user_file_id,update_params):
    _entity = select_by_id(user_file_id)
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

def full_search(search_str,row_cnt = 50000, row_begin=0, order_by = " order by user_file_id desc"):
    if search_str is None or search_str.strip() == '' :
        return None
    _where = "where"
    _limit = " limit %s,%s"%(row_begin,row_cnt)
    attrs = ['user_file_id','file_uuid','upload_user_id','file_name','file_type','content_type','file_storage','cdn_url','file_suffix','file_content','file_preview','file_summary','upload_time']
    for attr in attrs:
        _where += " toString(%s) like '%%%s%%' or"%(attr,search_str)
    _where += " %s like '%%%s%%' or"%("ref_UploadUserId_SysUser.2", search_str)
    _where = _where + ' 1!=1'
    _myref_str = ','+UserFileEntity.get_myref_tables_str() if UserFileEntity.get_myref_tables_str() != '' else ''
    attrstr = 'user_file_id, file_uuid, upload_user_id, file_name, file_type, content_type, file_storage, cdn_url, file_suffix, file_content, file_preview, file_summary, upload_time' +_myref_str
    sql = "select %s from vs_user_file "%attrstr + _where + \
          order_by + _limit
    sql_count = "select count(*) from vs_user_file " + _where
    entities = []
    rts = exesql(sql)
    rtscnt = exesql(sql_count)
    total_cnt = int(rtscnt[0][0])
    for tup in rts:
        i = 0
        e = UserFileEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9], tup[10], tup[11], tup[12])
        i += len(UserFileEntity.get_attrcodes())
        stup1 = tup[i];i += 1
        if stup1[0] != 0:
            e.ref_UploadUserId_SysUser = SysUserEntity.create_by_tuple(stup1)
        entities.append(e)
    return entities,total_cnt

def select_all(order_by = " order by user_file_id desc"):
    entities = []
    sql = "select user_file_id, file_uuid, upload_user_id, file_name, file_type, content_type, file_storage, cdn_url, file_suffix, file_content, file_preview, file_summary, upload_time from v_user_file" + order_by
    rts = exesql(sql)
    for tup in rts:
        entities.append(UserFileEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9], tup[10], tup[11], tup[12]))
    return entities

def select_count():
    sql = "select count(*) from v_user_file"
    rts = exesql(sql)
    return int(rts[0][0])

#获取一页数据的同时也返回本表外键的数据
def select_vspage(row_cnt, row_begin, search_params,order_by = " order by user_file_id desc"):
    _where = "where"
    attrs = ['user_file_id','file_uuid','upload_user_id','file_name','file_type','content_type','file_storage','cdn_url','file_suffix','file_content','file_preview','file_summary','upload_time']
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
    _myref_str = ','+UserFileEntity.get_myref_tables_str() if UserFileEntity.get_myref_tables_str() != '' else ''
    attrstr = 'user_file_id, file_uuid, upload_user_id, file_name, file_type, content_type, file_storage, cdn_url, file_suffix, file_content, file_preview, file_summary, upload_time' +_myref_str
    sql = "select %s from vs_user_file "%attrstr + _where + \
          order_by + " limit %(row_begin)s,%(row_cnt)s"
    sql_count = "select count(*) from v_user_file " + _where
    entities = []
    rts = exesql(sql,{'row_cnt':row_cnt,'row_begin':row_begin})
    rtscnt = exesql(sql_count)
    total_cnt = int(rtscnt[0][0])
    for tup in rts:
        i = 0
        e = UserFileEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9], tup[10], tup[11], tup[12])
        i += len(UserFileEntity.get_attrcodes())
        stup1 = tup[i];i += 1
        if stup1[0] != 0:
            e.ref_UploadUserId_SysUser = SysUserEntity.create_by_tuple(stup1)
        entities.append(e)
    return entities,total_cnt

def select_page(row_cnt, row_begin, search_params,order_by = " order by user_file_id desc"):
    _where = "where"
    attrs = ['user_file_id','file_uuid','upload_user_id','file_name','file_type','content_type','file_storage','cdn_url','file_suffix','file_content','file_preview','file_summary','upload_time']
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
    sql = "select user_file_id, file_uuid, upload_user_id, file_name, file_type, content_type, file_storage, cdn_url, file_suffix, file_content, file_preview, file_summary, upload_time from v_user_file " + _where + \
          order_by + " limit %(row_begin)s,%(row_cnt)s"
    sql_count = "select count(*) from v_user_file " + _where
    entities = []
    rts = exesql(sql,{'row_cnt':row_cnt,'row_begin':row_begin})
    rtscnt = exesql(sql_count)
    total_cnt = int(rtscnt[0][0])
    for tup in rts:
        entities.append(UserFileEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9], tup[10], tup[11], tup[12]))
    return entities,total_cnt

def select_by_id(user_file_id):
    sql = "select user_file_id, file_uuid, upload_user_id, file_name, file_type, content_type, file_storage, cdn_url, file_suffix, file_content, file_preview, file_summary, upload_time from  v_user_file where user_file_id = %(user_file_id)s"
    rts = exesql(sql, {'user_file_id':user_file_id})
    if rts is None or len(rts) == 0:
        return None
    tup = rts[0]
    return UserFileEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9], tup[10], tup[11], tup[12])

def select_by_UserFileId(user_file_id, order_by = ' order by user_file_id desc'):
    entities = []
    sql = "select user_file_id, file_uuid, upload_user_id, file_name, file_type, content_type, file_storage, cdn_url, file_suffix, file_content, file_preview, file_summary, upload_time from v_user_file " \
          "where user_file_id = %(user_file_id)s" + order_by
    rts = exesql(sql, {'user_file_id':user_file_id})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(UserFileEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9], tup[10], tup[11], tup[12]))
    return entities
def select_by_FileUuid(file_uuid, order_by = ' order by user_file_id desc'):
    entities = []
    sql = "select user_file_id, file_uuid, upload_user_id, file_name, file_type, content_type, file_storage, cdn_url, file_suffix, file_content, file_preview, file_summary, upload_time from v_user_file " \
          "where file_uuid = %(file_uuid)s" + order_by
    rts = exesql(sql, {'file_uuid':file_uuid})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(UserFileEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9], tup[10], tup[11], tup[12]))
    return entities
def select_by_UploadUserId(upload_user_id, order_by = ' order by user_file_id desc'):
    entities = []
    sql = "select user_file_id, file_uuid, upload_user_id, file_name, file_type, content_type, file_storage, cdn_url, file_suffix, file_content, file_preview, file_summary, upload_time from v_user_file " \
          "where upload_user_id = %(upload_user_id)s" + order_by
    rts = exesql(sql, {'upload_user_id':upload_user_id})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(UserFileEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9], tup[10], tup[11], tup[12]))
    return entities
def select_by_FileName(file_name, order_by = ' order by user_file_id desc'):
    entities = []
    sql = "select user_file_id, file_uuid, upload_user_id, file_name, file_type, content_type, file_storage, cdn_url, file_suffix, file_content, file_preview, file_summary, upload_time from v_user_file " \
          "where file_name = %(file_name)s" + order_by
    rts = exesql(sql, {'file_name':file_name})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(UserFileEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9], tup[10], tup[11], tup[12]))
    return entities
def select_by_FileType(file_type, order_by = ' order by user_file_id desc'):
    entities = []
    sql = "select user_file_id, file_uuid, upload_user_id, file_name, file_type, content_type, file_storage, cdn_url, file_suffix, file_content, file_preview, file_summary, upload_time from v_user_file " \
          "where file_type = %(file_type)s" + order_by
    rts = exesql(sql, {'file_type':file_type})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(UserFileEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9], tup[10], tup[11], tup[12]))
    return entities
def select_by_ContentType(content_type, order_by = ' order by user_file_id desc'):
    entities = []
    sql = "select user_file_id, file_uuid, upload_user_id, file_name, file_type, content_type, file_storage, cdn_url, file_suffix, file_content, file_preview, file_summary, upload_time from v_user_file " \
          "where content_type = %(content_type)s" + order_by
    rts = exesql(sql, {'content_type':content_type})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(UserFileEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9], tup[10], tup[11], tup[12]))
    return entities
def select_by_FileStorage(file_storage, order_by = ' order by user_file_id desc'):
    entities = []
    sql = "select user_file_id, file_uuid, upload_user_id, file_name, file_type, content_type, file_storage, cdn_url, file_suffix, file_content, file_preview, file_summary, upload_time from v_user_file " \
          "where file_storage = %(file_storage)s" + order_by
    rts = exesql(sql, {'file_storage':file_storage})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(UserFileEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9], tup[10], tup[11], tup[12]))
    return entities
def select_by_CdnUrl(cdn_url, order_by = ' order by user_file_id desc'):
    entities = []
    sql = "select user_file_id, file_uuid, upload_user_id, file_name, file_type, content_type, file_storage, cdn_url, file_suffix, file_content, file_preview, file_summary, upload_time from v_user_file " \
          "where cdn_url = %(cdn_url)s" + order_by
    rts = exesql(sql, {'cdn_url':cdn_url})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(UserFileEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9], tup[10], tup[11], tup[12]))
    return entities
def select_by_FileSuffix(file_suffix, order_by = ' order by user_file_id desc'):
    entities = []
    sql = "select user_file_id, file_uuid, upload_user_id, file_name, file_type, content_type, file_storage, cdn_url, file_suffix, file_content, file_preview, file_summary, upload_time from v_user_file " \
          "where file_suffix = %(file_suffix)s" + order_by
    rts = exesql(sql, {'file_suffix':file_suffix})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(UserFileEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9], tup[10], tup[11], tup[12]))
    return entities
def select_by_FileContent(file_content, order_by = ' order by user_file_id desc'):
    entities = []
    sql = "select user_file_id, file_uuid, upload_user_id, file_name, file_type, content_type, file_storage, cdn_url, file_suffix, file_content, file_preview, file_summary, upload_time from v_user_file " \
          "where file_content = %(file_content)s" + order_by
    rts = exesql(sql, {'file_content':file_content})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(UserFileEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9], tup[10], tup[11], tup[12]))
    return entities
def select_by_FilePreview(file_preview, order_by = ' order by user_file_id desc'):
    entities = []
    sql = "select user_file_id, file_uuid, upload_user_id, file_name, file_type, content_type, file_storage, cdn_url, file_suffix, file_content, file_preview, file_summary, upload_time from v_user_file " \
          "where file_preview = %(file_preview)s" + order_by
    rts = exesql(sql, {'file_preview':file_preview})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(UserFileEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9], tup[10], tup[11], tup[12]))
    return entities
def select_by_FileSummary(file_summary, order_by = ' order by user_file_id desc'):
    entities = []
    sql = "select user_file_id, file_uuid, upload_user_id, file_name, file_type, content_type, file_storage, cdn_url, file_suffix, file_content, file_preview, file_summary, upload_time from v_user_file " \
          "where file_summary = %(file_summary)s" + order_by
    rts = exesql(sql, {'file_summary':file_summary})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(UserFileEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9], tup[10], tup[11], tup[12]))
    return entities
def select_by_UploadTime(upload_time, order_by = ' order by user_file_id desc'):
    entities = []
    sql = "select user_file_id, file_uuid, upload_user_id, file_name, file_type, content_type, file_storage, cdn_url, file_suffix, file_content, file_preview, file_summary, upload_time from v_user_file " \
          "where upload_time = %(upload_time)s" + order_by
    rts = exesql(sql, {'upload_time':upload_time})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(UserFileEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9], tup[10], tup[11], tup[12]))
    return entities

def select_by_UserFileIdList(user_file_id_list,order_by = ' order by user_file_id desc'):
    _dict = {}
    sql = "select user_file_id, file_uuid, upload_user_id, file_name, file_type, content_type, file_storage, cdn_url, file_suffix, file_content, file_preview, file_summary, upload_time from v_user_file" \
          " where user_file_id in (%(user_file_id_list)s)" + order_by
    rts = exesql(sql, {'user_file_id_list':user_file_id_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = UserFileEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9], tup[10], tup[11], tup[12])
        if _dict.get(entity.user_file_id) is None:
            _dict[entity.user_file_id] = list()
        _dict[entity.user_file_id].append(entity)
    return _dict

def select_by_UserFileIdList2(user_file_id_list,order_by = ' order by user_file_id desc'):
    _dict = []
    sql = "select user_file_id, file_uuid, upload_user_id, file_name, file_type, content_type, file_storage, cdn_url, file_suffix, file_content, file_preview, file_summary, upload_time from v_user_file" \
          " where user_file_id in (%(user_file_id_list)s)" + order_by
    rts = exesql(sql, {'user_file_id_list':user_file_id_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = UserFileEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9], tup[10], tup[11], tup[12])
        _dict.append(entity)
    return _dict
def select_by_FileUuidList(file_uuid_list,order_by = ' order by user_file_id desc'):
    _dict = {}
    sql = "select user_file_id, file_uuid, upload_user_id, file_name, file_type, content_type, file_storage, cdn_url, file_suffix, file_content, file_preview, file_summary, upload_time from v_user_file" \
          " where file_uuid in (%(file_uuid_list)s)" + order_by
    rts = exesql(sql, {'file_uuid_list':file_uuid_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = UserFileEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9], tup[10], tup[11], tup[12])
        if _dict.get(entity.file_uuid) is None:
            _dict[entity.file_uuid] = list()
        _dict[entity.file_uuid].append(entity)
    return _dict
def select_by_UploadUserIdList(upload_user_id_list,order_by = ' order by user_file_id desc'):
    _dict = {}
    sql = "select user_file_id, file_uuid, upload_user_id, file_name, file_type, content_type, file_storage, cdn_url, file_suffix, file_content, file_preview, file_summary, upload_time from v_user_file" \
          " where upload_user_id in (%(upload_user_id_list)s)" + order_by
    rts = exesql(sql, {'upload_user_id_list':upload_user_id_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = UserFileEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9], tup[10], tup[11], tup[12])
        if _dict.get(entity.upload_user_id) is None:
            _dict[entity.upload_user_id] = list()
        _dict[entity.upload_user_id].append(entity)
    return _dict
def select_by_FileNameList(file_name_list,order_by = ' order by user_file_id desc'):
    _dict = {}
    sql = "select user_file_id, file_uuid, upload_user_id, file_name, file_type, content_type, file_storage, cdn_url, file_suffix, file_content, file_preview, file_summary, upload_time from v_user_file" \
          " where file_name in (%(file_name_list)s)" + order_by
    rts = exesql(sql, {'file_name_list':file_name_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = UserFileEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9], tup[10], tup[11], tup[12])
        if _dict.get(entity.file_name) is None:
            _dict[entity.file_name] = list()
        _dict[entity.file_name].append(entity)
    return _dict
def select_by_FileTypeList(file_type_list,order_by = ' order by user_file_id desc'):
    _dict = {}
    sql = "select user_file_id, file_uuid, upload_user_id, file_name, file_type, content_type, file_storage, cdn_url, file_suffix, file_content, file_preview, file_summary, upload_time from v_user_file" \
          " where file_type in (%(file_type_list)s)" + order_by
    rts = exesql(sql, {'file_type_list':file_type_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = UserFileEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9], tup[10], tup[11], tup[12])
        if _dict.get(entity.file_type) is None:
            _dict[entity.file_type] = list()
        _dict[entity.file_type].append(entity)
    return _dict
def select_by_ContentTypeList(content_type_list,order_by = ' order by user_file_id desc'):
    _dict = {}
    sql = "select user_file_id, file_uuid, upload_user_id, file_name, file_type, content_type, file_storage, cdn_url, file_suffix, file_content, file_preview, file_summary, upload_time from v_user_file" \
          " where content_type in (%(content_type_list)s)" + order_by
    rts = exesql(sql, {'content_type_list':content_type_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = UserFileEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9], tup[10], tup[11], tup[12])
        if _dict.get(entity.content_type) is None:
            _dict[entity.content_type] = list()
        _dict[entity.content_type].append(entity)
    return _dict
def select_by_FileStorageList(file_storage_list,order_by = ' order by user_file_id desc'):
    _dict = {}
    sql = "select user_file_id, file_uuid, upload_user_id, file_name, file_type, content_type, file_storage, cdn_url, file_suffix, file_content, file_preview, file_summary, upload_time from v_user_file" \
          " where file_storage in (%(file_storage_list)s)" + order_by
    rts = exesql(sql, {'file_storage_list':file_storage_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = UserFileEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9], tup[10], tup[11], tup[12])
        if _dict.get(entity.file_storage) is None:
            _dict[entity.file_storage] = list()
        _dict[entity.file_storage].append(entity)
    return _dict
def select_by_CdnUrlList(cdn_url_list,order_by = ' order by user_file_id desc'):
    _dict = {}
    sql = "select user_file_id, file_uuid, upload_user_id, file_name, file_type, content_type, file_storage, cdn_url, file_suffix, file_content, file_preview, file_summary, upload_time from v_user_file" \
          " where cdn_url in (%(cdn_url_list)s)" + order_by
    rts = exesql(sql, {'cdn_url_list':cdn_url_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = UserFileEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9], tup[10], tup[11], tup[12])
        if _dict.get(entity.cdn_url) is None:
            _dict[entity.cdn_url] = list()
        _dict[entity.cdn_url].append(entity)
    return _dict
def select_by_FileSuffixList(file_suffix_list,order_by = ' order by user_file_id desc'):
    _dict = {}
    sql = "select user_file_id, file_uuid, upload_user_id, file_name, file_type, content_type, file_storage, cdn_url, file_suffix, file_content, file_preview, file_summary, upload_time from v_user_file" \
          " where file_suffix in (%(file_suffix_list)s)" + order_by
    rts = exesql(sql, {'file_suffix_list':file_suffix_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = UserFileEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9], tup[10], tup[11], tup[12])
        if _dict.get(entity.file_suffix) is None:
            _dict[entity.file_suffix] = list()
        _dict[entity.file_suffix].append(entity)
    return _dict
def select_by_FileContentList(file_content_list,order_by = ' order by user_file_id desc'):
    _dict = {}
    sql = "select user_file_id, file_uuid, upload_user_id, file_name, file_type, content_type, file_storage, cdn_url, file_suffix, file_content, file_preview, file_summary, upload_time from v_user_file" \
          " where file_content in (%(file_content_list)s)" + order_by
    rts = exesql(sql, {'file_content_list':file_content_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = UserFileEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9], tup[10], tup[11], tup[12])
        if _dict.get(entity.file_content) is None:
            _dict[entity.file_content] = list()
        _dict[entity.file_content].append(entity)
    return _dict
def select_by_FilePreviewList(file_preview_list,order_by = ' order by user_file_id desc'):
    _dict = {}
    sql = "select user_file_id, file_uuid, upload_user_id, file_name, file_type, content_type, file_storage, cdn_url, file_suffix, file_content, file_preview, file_summary, upload_time from v_user_file" \
          " where file_preview in (%(file_preview_list)s)" + order_by
    rts = exesql(sql, {'file_preview_list':file_preview_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = UserFileEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9], tup[10], tup[11], tup[12])
        if _dict.get(entity.file_preview) is None:
            _dict[entity.file_preview] = list()
        _dict[entity.file_preview].append(entity)
    return _dict
def select_by_FileSummaryList(file_summary_list,order_by = ' order by user_file_id desc'):
    _dict = {}
    sql = "select user_file_id, file_uuid, upload_user_id, file_name, file_type, content_type, file_storage, cdn_url, file_suffix, file_content, file_preview, file_summary, upload_time from v_user_file" \
          " where file_summary in (%(file_summary_list)s)" + order_by
    rts = exesql(sql, {'file_summary_list':file_summary_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = UserFileEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9], tup[10], tup[11], tup[12])
        if _dict.get(entity.file_summary) is None:
            _dict[entity.file_summary] = list()
        _dict[entity.file_summary].append(entity)
    return _dict
def select_by_UploadTimeList(upload_time_list,order_by = ' order by user_file_id desc'):
    _dict = {}
    sql = "select user_file_id, file_uuid, upload_user_id, file_name, file_type, content_type, file_storage, cdn_url, file_suffix, file_content, file_preview, file_summary, upload_time from v_user_file" \
          " where upload_time in (%(upload_time_list)s)" + order_by
    rts = exesql(sql, {'upload_time_list':upload_time_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = UserFileEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9], tup[10], tup[11], tup[12])
        if _dict.get(entity.upload_time) is None:
            _dict[entity.upload_time] = list()
        _dict[entity.upload_time].append(entity)
    return _dict

