from sysdw import exesql
from utils import IDUtil
from domain.sysdomain.entity.SysMenuAuthEntity import SysMenuAuthEntity

from domain.sysdomain.entity.SysMenuEntity import SysMenuEntity
from domain.sysdomain.entity.SysRoleEntity import SysRoleEntity
from domain.sysdomain.entity.SysUserEntity import SysUserEntity
from domain.sysdomain.entity.SysOrgEntity import SysOrgEntity
from domain.sysdomain.entity.OrgDutyEntity import OrgDutyEntity

# sys_menu_auth_id, sys_menu_id, sys_user_id, sys_role_id, sys_org_id, org_duty_id, remark
# tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6]

def insert(entity):
    sql = "insert into phy_sys_menu_auth(sys_menu_auth_id, sys_menu_id, sys_user_id, sys_role_id, sys_org_id, org_duty_id, remark,ver_id) values"
    exesql(sql, [(entity.sys_menu_auth_id ,entity.sys_menu_id ,entity.sys_user_id ,entity.sys_role_id ,entity.sys_org_id ,entity.org_duty_id ,entity.remark ,IDUtil.get_long())])
    return entity

def delete_by_id(sys_menu_auth_id):
    sql = """insert into phy_sys_menu_auth(sys_menu_auth_id, sys_menu_id, sys_user_id, sys_role_id, sys_org_id, org_duty_id, remark,deleted,ver_id) 
        select sys_menu_auth_id, sys_menu_id, sys_user_id, sys_role_id, sys_org_id, org_duty_id, remark,1,%d from v_sys_menu_auth 
        where sys_menu_auth_id = %d"""%(IDUtil.get_long(),sys_menu_auth_id)
    exesql(sql)

def delete(entity):
    delete_by_id(entity.sys_menu_auth_id)

def update(entity):
    return insert(entity)

def update_by_id(sys_menu_auth_id,update_params):
    _entity = select_by_id(sys_menu_auth_id)
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

def full_search(search_str,row_cnt = 50000, row_begin=0, order_by = " order by sys_menu_auth_id desc"):
    if search_str is None or search_str.strip() == '' :
        return None
    _where = "where"
    _limit = " limit %s,%s"%(row_begin,row_cnt)
    attrs = ['sys_menu_auth_id','sys_menu_id','sys_user_id','sys_role_id','sys_org_id','org_duty_id','remark']
    for attr in attrs:
        _where += " toString(%s) like '%%%s%%' or"%(attr,search_str)
    _where += " %s like '%%%s%%' or"%("ref_SysMenuId_SysMenu.2", search_str)
    _where += " %s like '%%%s%%' or"%("ref_SysRoleId_SysRole.2", search_str)
    _where += " %s like '%%%s%%' or"%("ref_SysUserId_SysUser.2", search_str)
    _where += " %s like '%%%s%%' or"%("ref_SysOrgId_SysOrg.2", search_str)
    _where += " %s like '%%%s%%' or"%("ref_OrgDutyId_OrgDuty.3", search_str)
    _where = _where + ' 1!=1'
    _myref_str = ','+SysMenuAuthEntity.get_myref_tables_str() if SysMenuAuthEntity.get_myref_tables_str() != '' else ''
    attrstr = 'sys_menu_auth_id, sys_menu_id, sys_user_id, sys_role_id, sys_org_id, org_duty_id, remark' +_myref_str
    sql = "select %s from vs_sys_menu_auth "%attrstr + _where + \
          order_by + _limit
    sql_count = "select count(*) from vs_sys_menu_auth " + _where
    entities = []
    rts = exesql(sql)
    rtscnt = exesql(sql_count)
    total_cnt = int(rtscnt[0][0])
    for tup in rts:
        i = 0
        e = SysMenuAuthEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6])
        i += len(SysMenuAuthEntity.get_attrcodes())
        stup1 = tup[i];i += 1
        if stup1[0] != 0:
            e.ref_SysMenuId_SysMenu = SysMenuEntity.create_by_tuple(stup1)
        stup1 = tup[i];i += 1
        if stup1[0] != 0:
            e.ref_SysRoleId_SysRole = SysRoleEntity.create_by_tuple(stup1)
        stup1 = tup[i];i += 1
        if stup1[0] != 0:
            e.ref_SysUserId_SysUser = SysUserEntity.create_by_tuple(stup1)
        stup1 = tup[i];i += 1
        if stup1[0] != 0:
            e.ref_SysOrgId_SysOrg = SysOrgEntity.create_by_tuple(stup1)
        stup1 = tup[i];i += 1
        if stup1[0] != 0:
            e.ref_OrgDutyId_OrgDuty = OrgDutyEntity.create_by_tuple(stup1)
        entities.append(e)
    return entities,total_cnt

def select_all(order_by = " order by sys_menu_auth_id desc"):
    entities = []
    sql = "select sys_menu_auth_id, sys_menu_id, sys_user_id, sys_role_id, sys_org_id, org_duty_id, remark from v_sys_menu_auth" + order_by
    rts = exesql(sql)
    for tup in rts:
        entities.append(SysMenuAuthEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6]))
    return entities

def select_count():
    sql = "select count(*) from v_sys_menu_auth"
    rts = exesql(sql)
    return int(rts[0][0])

#获取一页数据的同时也返回本表外键的数据
def select_vspage(row_cnt, row_begin, search_params,order_by = " order by sys_menu_auth_id desc"):
    _where = "where"
    attrs = ['sys_menu_auth_id','sys_menu_id','sys_user_id','sys_role_id','sys_org_id','org_duty_id','remark']
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
    _myref_str = ','+SysMenuAuthEntity.get_myref_tables_str() if SysMenuAuthEntity.get_myref_tables_str() != '' else ''
    attrstr = 'sys_menu_auth_id, sys_menu_id, sys_user_id, sys_role_id, sys_org_id, org_duty_id, remark' +_myref_str
    sql = "select %s from vs_sys_menu_auth "%attrstr + _where + \
          order_by + " limit %(row_begin)s,%(row_cnt)s"
    sql_count = "select count(*) from v_sys_menu_auth " + _where
    entities = []
    rts = exesql(sql,{'row_cnt':row_cnt,'row_begin':row_begin})
    rtscnt = exesql(sql_count)
    total_cnt = int(rtscnt[0][0])
    for tup in rts:
        i = 0
        e = SysMenuAuthEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6])
        i += len(SysMenuAuthEntity.get_attrcodes())
        stup1 = tup[i];i += 1
        if stup1[0] != 0:
            e.ref_SysMenuId_SysMenu = SysMenuEntity.create_by_tuple(stup1)
        stup1 = tup[i];i += 1
        if stup1[0] != 0:
            e.ref_SysRoleId_SysRole = SysRoleEntity.create_by_tuple(stup1)
        stup1 = tup[i];i += 1
        if stup1[0] != 0:
            e.ref_SysUserId_SysUser = SysUserEntity.create_by_tuple(stup1)
        stup1 = tup[i];i += 1
        if stup1[0] != 0:
            e.ref_SysOrgId_SysOrg = SysOrgEntity.create_by_tuple(stup1)
        stup1 = tup[i];i += 1
        if stup1[0] != 0:
            e.ref_OrgDutyId_OrgDuty = OrgDutyEntity.create_by_tuple(stup1)
        entities.append(e)
    return entities,total_cnt

def select_page(row_cnt, row_begin, search_params,order_by = " order by sys_menu_auth_id desc"):
    _where = "where"
    attrs = ['sys_menu_auth_id','sys_menu_id','sys_user_id','sys_role_id','sys_org_id','org_duty_id','remark']
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
    sql = "select sys_menu_auth_id, sys_menu_id, sys_user_id, sys_role_id, sys_org_id, org_duty_id, remark from v_sys_menu_auth " + _where + \
          order_by + " limit %(row_begin)s,%(row_cnt)s"
    sql_count = "select count(*) from v_sys_menu_auth " + _where
    entities = []
    rts = exesql(sql,{'row_cnt':row_cnt,'row_begin':row_begin})
    rtscnt = exesql(sql_count)
    total_cnt = int(rtscnt[0][0])
    for tup in rts:
        entities.append(SysMenuAuthEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6]))
    return entities,total_cnt

def select_by_id(sys_menu_auth_id):
    sql = "select sys_menu_auth_id, sys_menu_id, sys_user_id, sys_role_id, sys_org_id, org_duty_id, remark from  v_sys_menu_auth where sys_menu_auth_id = %(sys_menu_auth_id)s"
    rts = exesql(sql, {'sys_menu_auth_id':sys_menu_auth_id})
    if rts is None or len(rts) == 0:
        return None
    tup = rts[0]
    return SysMenuAuthEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6])

def select_by_SysMenuAuthId(sys_menu_auth_id, order_by = ' order by sys_menu_auth_id desc'):
    entities = []
    sql = "select sys_menu_auth_id, sys_menu_id, sys_user_id, sys_role_id, sys_org_id, org_duty_id, remark from v_sys_menu_auth " \
          "where sys_menu_auth_id = %(sys_menu_auth_id)s" + order_by
    rts = exesql(sql, {'sys_menu_auth_id':sys_menu_auth_id})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(SysMenuAuthEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6]))
    return entities
def select_by_SysMenuId(sys_menu_id, order_by = ' order by sys_menu_auth_id desc'):
    entities = []
    sql = "select sys_menu_auth_id, sys_menu_id, sys_user_id, sys_role_id, sys_org_id, org_duty_id, remark from v_sys_menu_auth " \
          "where sys_menu_id = %(sys_menu_id)s" + order_by
    rts = exesql(sql, {'sys_menu_id':sys_menu_id})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(SysMenuAuthEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6]))
    return entities
def select_by_SysUserId(sys_user_id, order_by = ' order by sys_menu_auth_id desc'):
    entities = []
    sql = "select sys_menu_auth_id, sys_menu_id, sys_user_id, sys_role_id, sys_org_id, org_duty_id, remark from v_sys_menu_auth " \
          "where sys_user_id = %(sys_user_id)s" + order_by
    rts = exesql(sql, {'sys_user_id':sys_user_id})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(SysMenuAuthEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6]))
    return entities
def select_by_SysRoleId(sys_role_id, order_by = ' order by sys_menu_auth_id desc'):
    entities = []
    sql = "select sys_menu_auth_id, sys_menu_id, sys_user_id, sys_role_id, sys_org_id, org_duty_id, remark from v_sys_menu_auth " \
          "where sys_role_id = %(sys_role_id)s" + order_by
    rts = exesql(sql, {'sys_role_id':sys_role_id})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(SysMenuAuthEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6]))
    return entities
def select_by_SysOrgId(sys_org_id, order_by = ' order by sys_menu_auth_id desc'):
    entities = []
    sql = "select sys_menu_auth_id, sys_menu_id, sys_user_id, sys_role_id, sys_org_id, org_duty_id, remark from v_sys_menu_auth " \
          "where sys_org_id = %(sys_org_id)s" + order_by
    rts = exesql(sql, {'sys_org_id':sys_org_id})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(SysMenuAuthEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6]))
    return entities
def select_by_OrgDutyId(org_duty_id, order_by = ' order by sys_menu_auth_id desc'):
    entities = []
    sql = "select sys_menu_auth_id, sys_menu_id, sys_user_id, sys_role_id, sys_org_id, org_duty_id, remark from v_sys_menu_auth " \
          "where org_duty_id = %(org_duty_id)s" + order_by
    rts = exesql(sql, {'org_duty_id':org_duty_id})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(SysMenuAuthEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6]))
    return entities
def select_by_Remark(remark, order_by = ' order by sys_menu_auth_id desc'):
    entities = []
    sql = "select sys_menu_auth_id, sys_menu_id, sys_user_id, sys_role_id, sys_org_id, org_duty_id, remark from v_sys_menu_auth " \
          "where remark = %(remark)s" + order_by
    rts = exesql(sql, {'remark':remark})
    if rts is None or len(rts) == 0:
        return None
    for tup in rts:
        entities.append(SysMenuAuthEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6]))
    return entities

def select_by_SysMenuAuthIdList(sys_menu_auth_id_list,order_by = ' order by sys_menu_auth_id desc'):
    _dict = {}
    sql = "select sys_menu_auth_id, sys_menu_id, sys_user_id, sys_role_id, sys_org_id, org_duty_id, remark from v_sys_menu_auth" \
          " where sys_menu_auth_id in (%(sys_menu_auth_id_list)s)" + order_by
    rts = exesql(sql, {'sys_menu_auth_id_list':sys_menu_auth_id_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = SysMenuAuthEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6])
        if _dict.get(entity.sys_menu_auth_id) is None:
            _dict[entity.sys_menu_auth_id] = list()
        _dict[entity.sys_menu_auth_id].append(entity)
    return _dict
def select_by_SysMenuIdList(sys_menu_id_list,order_by = ' order by sys_menu_auth_id desc'):
    _dict = {}
    sql = "select sys_menu_auth_id, sys_menu_id, sys_user_id, sys_role_id, sys_org_id, org_duty_id, remark from v_sys_menu_auth" \
          " where sys_menu_id in (%(sys_menu_id_list)s)" + order_by
    rts = exesql(sql, {'sys_menu_id_list':sys_menu_id_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = SysMenuAuthEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6])
        if _dict.get(entity.sys_menu_id) is None:
            _dict[entity.sys_menu_id] = list()
        _dict[entity.sys_menu_id].append(entity)
    return _dict
def select_by_SysUserIdList(sys_user_id_list,order_by = ' order by sys_menu_auth_id desc'):
    _dict = {}
    sql = "select sys_menu_auth_id, sys_menu_id, sys_user_id, sys_role_id, sys_org_id, org_duty_id, remark from v_sys_menu_auth" \
          " where sys_user_id in (%(sys_user_id_list)s)" + order_by
    rts = exesql(sql, {'sys_user_id_list':sys_user_id_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = SysMenuAuthEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6])
        if _dict.get(entity.sys_user_id) is None:
            _dict[entity.sys_user_id] = list()
        _dict[entity.sys_user_id].append(entity)
    return _dict
def select_by_SysRoleIdList(sys_role_id_list,order_by = ' order by sys_menu_auth_id desc'):
    _dict = {}
    sql = "select sys_menu_auth_id, sys_menu_id, sys_user_id, sys_role_id, sys_org_id, org_duty_id, remark from v_sys_menu_auth" \
          " where sys_role_id in (%(sys_role_id_list)s)" + order_by
    rts = exesql(sql, {'sys_role_id_list':sys_role_id_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = SysMenuAuthEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6])
        if _dict.get(entity.sys_role_id) is None:
            _dict[entity.sys_role_id] = list()
        _dict[entity.sys_role_id].append(entity)
    return _dict
def select_by_SysOrgIdList(sys_org_id_list,order_by = ' order by sys_menu_auth_id desc'):
    _dict = {}
    sql = "select sys_menu_auth_id, sys_menu_id, sys_user_id, sys_role_id, sys_org_id, org_duty_id, remark from v_sys_menu_auth" \
          " where sys_org_id in (%(sys_org_id_list)s)" + order_by
    rts = exesql(sql, {'sys_org_id_list':sys_org_id_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = SysMenuAuthEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6])
        if _dict.get(entity.sys_org_id) is None:
            _dict[entity.sys_org_id] = list()
        _dict[entity.sys_org_id].append(entity)
    return _dict
def select_by_OrgDutyIdList(org_duty_id_list,order_by = ' order by sys_menu_auth_id desc'):
    _dict = {}
    sql = "select sys_menu_auth_id, sys_menu_id, sys_user_id, sys_role_id, sys_org_id, org_duty_id, remark from v_sys_menu_auth" \
          " where org_duty_id in (%(org_duty_id_list)s)" + order_by
    rts = exesql(sql, {'org_duty_id_list':org_duty_id_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = SysMenuAuthEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6])
        if _dict.get(entity.org_duty_id) is None:
            _dict[entity.org_duty_id] = list()
        _dict[entity.org_duty_id].append(entity)
    return _dict
def select_by_RemarkList(remark_list,order_by = ' order by sys_menu_auth_id desc'):
    _dict = {}
    sql = "select sys_menu_auth_id, sys_menu_id, sys_user_id, sys_role_id, sys_org_id, org_duty_id, remark from v_sys_menu_auth" \
          " where remark in (%(remark_list)s)" + order_by
    rts = exesql(sql, {'remark_list':remark_list})
    if rts is None or len(rts) == 0:
        return {}
    for tup in rts:
        entity = SysMenuAuthEntity(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6])
        if _dict.get(entity.remark) is None:
            _dict[entity.remark] = list()
        _dict[entity.remark].append(entity)
    return _dict

