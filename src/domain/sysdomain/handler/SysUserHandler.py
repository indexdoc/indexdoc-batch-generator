from domain.sysdomain.serv import SysUserServ
from domain.sysdomain.entity.SysUserEntity import SysUserEntity
from BaseHandler import BaseApiHandler
from tornado.web import authenticated
from utils import PageUtil
from utils import IDUtil
from utils.TypeCvt import *
import logging
import traceback
import json

class ApiVsListHandler(BaseApiHandler):
    def myget(self):
        _limit = self.get_arg('limit')
        _page = self.get_arg('page')
        # _real_ip = self.request.headers.get('X-Real-IP')
        _search_params = self.get_arg('searchParams') #JSON格式传数据
        _limit = 50000 if _limit is None else int(_limit)
        _page = 1 if _page is None else int(_page)
        if _search_params is not None:
            _search_params = json.loads(_search_params)
        _entities,_cnt = SysUserServ.get_vspage(_limit, (_page - 1) * _limit, _search_params)
        self.write({
            'success':True,
            'code':0,
            'msg':None,
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
                'success':False,
                'msg':'搜索的字符串为空',
            })
            return
        _entities,_cnt = SysUserServ.full_search(_limit, (_page - 1) * _limit, _search_str)
        self.write({
            'success':True,
            'code':0,
            'msg':None,
            'count': _cnt,
            'data': _entities
        })


class ApiListHandler(BaseApiHandler):
    def myget(self):
        _limit = self.get_arg('limit')
        _page = self.get_arg('page')
        _search_params = self.get_arg('searchParams') #JSON格式传数据
        _limit = 50000 if _limit is None else int(_limit)
        _page = 1 if _page is None else int(_page)
        if _search_params is not None:
            _search_params = json.loads(_search_params)
        _entities,_cnt = SysUserServ.get_page(_limit, (_page - 1) * _limit, _search_params)
        self.write({
            'success':True,
            'code':0,
            'msg':None,
            'count': _cnt,
            'data': _entities
        })
        return


class ApiAddHandler(BaseApiHandler):
    def mypost(self):
        _user_name=object_to_str(self.get_arg('user_name'))
        _pwd=object_to_str(self.get_arg('pwd'))
        _last_login_time=str_to_datetime(self.get_arg('last_login_time'))
        _last_active_time=str_to_datetime(self.get_arg('last_active_time'))
        _create_time=str_to_datetime(self.get_arg('create_time'))
        _update_time=str_to_datetime(self.get_arg('update_time'))
        _last_login_info=object_to_str(self.get_arg('last_login_info'))
        _remark=object_to_str(self.get_arg('remark'))
        _entity = SysUserServ.create(_user_name,_pwd,_last_login_time,_last_active_time,_create_time,_update_time,_last_login_info,_remark)
        self.clear()
        _rtn = {'success': True,
                'msg': 'success',
                'obj': _entity.to_dict(),
                }
        self.write(_rtn)
        return

class ApiDeleteHandler(BaseApiHandler):
    def myget(self):
        _sys_user_id = int(self.get_arg('sys_user_id'))
        SysUserServ.delete(_sys_user_id)
        _rtn = {'success': True,
                'msg': 'success',
                'obj': _sys_user_id,
                }
        self.write(_rtn)
        return


class ApiUpdateHandler(BaseApiHandler):
    def mypost(self):
        _sys_user_id=str_to_int(self.get_arg('sys_user_id'))
        _user_name=object_to_str(self.get_arg('user_name'))
        _pwd=object_to_str(self.get_arg('pwd'))
        _last_login_time=str_to_datetime(self.get_arg('last_login_time'))
        _last_active_time=str_to_datetime(self.get_arg('last_active_time'))
        _create_time=str_to_datetime(self.get_arg('create_time'))
        _update_time=str_to_datetime(self.get_arg('update_time'))
        _last_login_info=object_to_str(self.get_arg('last_login_info'))
        _remark=object_to_str(self.get_arg('remark'))
        _entity = SysUserServ.update(_sys_user_id ,_user_name ,_pwd ,_last_login_time ,_last_active_time ,_create_time ,_update_time ,_last_login_info ,_remark )
        _rtn = {'success': True,
                'msg': 'success',
                'obj': _entity.to_dict(),
                }
        self.clear()
        self.write(_rtn)

# /api/sysdomain/SysUser/updateById?id=123456&update_params={"column_code1":"value1","column_code2":"value2"}
class ApiUpdateByIdHandler(BaseApiHandler):
    def myget(self):
        _sys_user_id = self.get_arg('id')
        _update_params = self.get_arg('update_params') #JSON格式传数据
        if _sys_user_id is None or _sys_user_id.strip() == '' \
           or _update_params is None or _update_params.strip()=='':
            self.write({
                'success':False,
                'msg':'参数错误',
            })
            return
        _update_params = json.loads(_update_params)
#将参数转换为python对象
        if _update_params.get('sys_user_id') is not None:
            _update_params['sys_user_id'] = str_to_int(_update_params.get('sys_user_id'))
        if _update_params.get('user_name') is not None:
            _update_params['user_name'] = object_to_str(_update_params.get('user_name'))
        if _update_params.get('pwd') is not None:
            _update_params['pwd'] = object_to_str(_update_params.get('pwd'))
        if _update_params.get('last_login_time') is not None:
            _update_params['last_login_time'] = str_to_datetime(_update_params.get('last_login_time'))
        if _update_params.get('last_active_time') is not None:
            _update_params['last_active_time'] = str_to_datetime(_update_params.get('last_active_time'))
        if _update_params.get('create_time') is not None:
            _update_params['create_time'] = str_to_datetime(_update_params.get('create_time'))
        if _update_params.get('update_time') is not None:
            _update_params['update_time'] = str_to_datetime(_update_params.get('update_time'))
        if _update_params.get('last_login_info') is not None:
            _update_params['last_login_info'] = object_to_str(_update_params.get('last_login_info'))
        if _update_params.get('remark') is not None:
            _update_params['remark'] = object_to_str(_update_params.get('remark'))
        _entity = SysUserServ.update_by_id(_sys_user_id,_update_params)
        if _entity is None:
            self.write({
                'success':False,
                'msg':'ID不存在',
            })
            return
        _rtn = {'success': True,
                'msg': 'success',
                'obj': _entity.to_dict(),
                }
        self.clear()
        self.write(_rtn)

urls =[
    ('/api/sysdomain/SysUser/list',ApiListHandler),
    ('/api/sysdomain/SysUser/vslist',ApiVsListHandler),
    ('/api/sysdomain/SysUser/add', ApiAddHandler),
    ('/api/sysdomain/SysUser/delete', ApiDeleteHandler),
    ('/api/sysdomain/SysUser/update', ApiUpdateHandler),
    ('/api/sysdomain/SysUser/fullSearch', ApiVsFullSearchHandler),
    ('/api/sysdomain/SysUser/updateById', ApiUpdateByIdHandler),
    ]
