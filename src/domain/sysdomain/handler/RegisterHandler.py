import hashlib

from domain.sysdomain.daock import SysUserDaoCK
from domain.sysdomain.handler import SysUserHandler
from domain.sysdomain.serv import RegisterServ, SysUserServ
from domain.sysdomain.entity.RegisterEntity import RegisterEntity
from BaseHandler import BaseApiHandler
from tornado.web import authenticated
from utils import PageUtil, CodeUtil
from utils import IDUtil
from utils.TypeCvt import *
import logging
import traceback
import json


class ApiVsListHandler(BaseApiHandler):
    def myget(self):
        _limit = self.get_arg('limit')
        _page = self.get_arg('page')
        _search_params = self.get_arg('searchParams')  # JSON格式传数据
        _limit = 50000 if _limit is None else int(_limit)
        _page = 1 if _page is None else int(_page)
        if _search_params is not None:
            _search_params = json.loads(_search_params)
        _entities, _cnt = RegisterServ.get_vspage(_limit, (_page - 1) * _limit, _search_params)
        self.write({
            'success': True,
            'code': 0,
            'msg': None,
            'count': _cnt,
            'data': _entities
        })
        return


class ApiVsFullSearchHandler(BaseApiHandler):
    def myget(self):
        _limit = self.get_arg('limit')
        _page = self.get_arg('page')
        _search_str = self.get_arg('searchString')
        _limit = 50000 if _limit is None else int(_limit)
        _page = 1 if _page is None else int(_page)
        if _search_str is None or _search_str.strip() == '':
            self.write({
                'success': False,
                'msg': '搜索的字符串为空',
            })
            return
        _entities, _cnt = RegisterServ.full_search(_limit, (_page - 1) * _limit, _search_str)
        self.write({
            'success': True,
            'code': 0,
            'msg': None,
            'count': _cnt,
            'data': _entities
        })


class ApiListHandler(BaseApiHandler):
    def myget(self):
        _limit = self.get_arg('limit')
        _page = self.get_arg('page')
        _search_params = self.get_arg('searchParams')  # JSON格式传数据
        _limit = 50000 if _limit is None else int(_limit)
        _page = 1 if _page is None else int(_page)
        if _search_params is not None:
            _search_params = json.loads(_search_params)
        _entities, _cnt = RegisterServ.get_page(_limit, (_page - 1) * _limit, _search_params)
        self.write({
            'success': True,
            'code': 0,
            'msg': None,
            'count': _cnt,
            'data': _entities
        })
        return


class ApiAddHandler(BaseApiHandler):
    def mypost(self):
        _sys_user_id = str_to_int(self.get_arg('sys_user_id'))
        _phone_no = object_to_str(self.get_arg('phone_no'))
        _name = object_to_str(self.get_arg('name'))
        _user_name = object_to_str(self.get_arg('user_name'))
        _company_name = object_to_str(self.get_arg('company_name'))
        _pwd = object_to_str(self.get_arg('pwd'))
        _status = object_to_str(self.get_arg('status'))
        _create_time = str_to_datetime(self.get_arg('create_time'))
        _update_time = str_to_datetime(self.get_arg('update_time'))
        _remark = object_to_str(self.get_arg('remark'))
        _entity = RegisterServ.create(_sys_user_id, _phone_no, _name, _user_name, _company_name, _pwd, _status,
                                      _create_time, _update_time, _remark)
        self.clear()
        _rtn = {'success': True,
                'msg': 'success',
                'obj': _entity.to_dict(),
                }
        self.write(_rtn)
        return


class ApiDeleteHandler(BaseApiHandler):
    def myget(self):
        _register_id = int(self.get_arg('register_id'))
        RegisterServ.delete(_register_id)
        _rtn = {'success': True,
                'msg': 'success',
                'obj': _register_id,
                }
        self.write(_rtn)
        return


class ApiUpdateHandler(BaseApiHandler):
    def mypost(self):
        _register_id = str_to_int(self.get_arg('register_id'))
        _sys_user_id = str_to_int(self.get_arg('sys_user_id'))
        _phone_no = object_to_str(self.get_arg('phone_no'))
        _name = object_to_str(self.get_arg('name'))
        _user_name = object_to_str(self.get_arg('user_name'))
        _company_name = object_to_str(self.get_arg('company_name'))
        _pwd = object_to_str(self.get_arg('pwd'))
        _status = object_to_str(self.get_arg('status'))
        _create_time = str_to_datetime(self.get_arg('create_time'))
        _update_time = str_to_datetime(self.get_arg('update_time'))
        _remark = object_to_str(self.get_arg('remark'))
        _entity = RegisterServ.update(_register_id, _sys_user_id, _phone_no, _name, _user_name, _company_name, _pwd,
                                      _status, _create_time, datetime.datetime.now(), _remark)
        _rtn = {'success': True,
                'msg': 'success',
                'obj': _entity.to_dict(),
                }
        self.clear()
        self.write(_rtn)


# /api/sysdomain/Register/updateById?id=123456&update_params={"column_code1":"value1","column_code2":"value2"}
class ApiUpdateByIdHandler2(BaseApiHandler):
    def myget(self):
        _register_id = self.get_arg('id')
        _update_params = self.get_arg('update_params')  # JSON格式传数据
        if _register_id is None or _register_id.strip() == '' \
                or _update_params is None or _update_params.strip() == '':
            self.write({
                'success': False,
                'msg': '参数错误',
            })
            return
        _update_params = json.loads(_update_params)
        # 将参数转换为python对象
        if _update_params.get('register_id') is not None:
            _update_params['register_id'] = str_to_int(_update_params.get('register_id'))
        if _update_params.get('sys_user_id') is not None:
            _update_params['sys_user_id'] = str_to_int(_update_params.get('sys_user_id'))
        if _update_params.get('phone_no') is not None:
            _update_params['phone_no'] = object_to_str(_update_params.get('phone_no'))
        if _update_params.get('name') is not None:
            _update_params['name'] = object_to_str(_update_params.get('name'))
        if _update_params.get('user_name') is not None:
            _update_params['user_name'] = object_to_str(_update_params.get('user_name'))
        if _update_params.get('company_name') is not None:
            _update_params['company_name'] = object_to_str(_update_params.get('company_name'))
        if _update_params.get('pwd') is not None:
            _update_params['pwd'] = object_to_str(_update_params.get('pwd'))
        if _update_params.get('status') is not None:
            _update_params['status'] = object_to_str(_update_params.get('status'))
        if _update_params.get('create_time') is not None:
            _update_params['create_time'] = str_to_datetime(_update_params.get('create_time'))
        if _update_params.get('update_time') is not None:
            # _update_params['update_time'] = str_to_datetime(_update_params.get('update_time'))
            _update_params['update_time'] = datetime.datetime.now()
        if _update_params.get('remark') is not None:
            _update_params['remark'] = object_to_str(_update_params.get('remark'))
        _entity = RegisterServ.update_by_id(_register_id, _update_params)
        if _entity is None:
            self.write({
                'success': False,
                'msg': 'ID不存在',
            })
            return
        if _update_params['status'] == '通过':
            if _entity.sys_user_id is None:
                _SysUserEntity = SysUserServ.create(_entity.user_name, _entity.pwd, None, None, datetime.datetime.now(),
                                                    None,
                                                    None, None)
            else:
                _SysUserEntity = SysUserServ.get_entity_by_id(_entity.sys_user_id)
                # 注册审核通过后用户被删除
                if _SysUserEntity is None:
                    _SysUserEntity = SysUserServ.create(_entity.user_name, _entity.pwd, None, None,
                                                        datetime.datetime.now(), None,
                                                        None, None)
            # 更新密码
            pwdsha1 = hashlib.sha1(_SysUserEntity.pwd.encode('utf-8')).hexdigest()
            pwdcode = CodeUtil.encode_pwd(pwdsha1, _SysUserEntity.sys_user_id)
            _SysUserEntity.pwd = pwdcode
            SysUserDaoCK.update(_SysUserEntity)
            # 更新用户id
            _params = {'sys_user_id': _SysUserEntity.sys_user_id}
            RegisterServ.update_by_id(_register_id, _params)

        _rtn = {'success': True,
                'msg': 'success',
                'obj': _entity.to_dict(),
                }
        self.clear()
        self.write(_rtn)


urls = [
    ('/api/sysdomain/Register/list', ApiListHandler),
    ('/api/sysdomain/Register/vslist', ApiVsListHandler),
    ('/api/sysdomain/Register/add', ApiAddHandler),
    ('/api/sysdomain/Register/delete', ApiDeleteHandler),
    ('/api/sysdomain/Register/update', ApiUpdateHandler),
    ('/api/sysdomain/Register/fullSearch', ApiVsFullSearchHandler),
    ('/api/sysdomain/Register/updateById', ApiUpdateByIdHandler2),
]
