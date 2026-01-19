from domain.sysdomain.serv import SysRoleServ
from domain.sysdomain.entity.SysRoleEntity import SysRoleEntity
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
        _search_params = self.get_arg('searchParams') #JSON格式传数据
        _limit = 50000 if _limit is None else int(_limit)
        _page = 1 if _page is None else int(_page)
        if _search_params is not None:
            _search_params = json.loads(_search_params)
        _entities,_cnt = SysRoleServ.get_vspage(_limit, (_page - 1) * _limit, _search_params)
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
        _entities,_cnt = SysRoleServ.full_search(_limit, (_page - 1) * _limit, _search_str)
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
        _entities,_cnt = SysRoleServ.get_page(_limit, (_page - 1) * _limit, _search_params)
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
        _role_name=object_to_str(self.get_arg('role_name'))
        _entity = SysRoleServ.create(_role_name)
        self.clear()
        _rtn = {'success': True,
                'msg': 'success',
                'obj': _entity.to_dict(),
                }
        self.write(_rtn)
        return

class ApiDeleteHandler(BaseApiHandler):
    def myget(self):
        _sys_role_id = int(self.get_arg('sys_role_id'))
        SysRoleServ.delete(_sys_role_id)
        _rtn = {'success': True,
                'msg': 'success',
                'obj': _sys_role_id,
                }
        self.write(_rtn)
        return


class ApiUpdateHandler(BaseApiHandler):
    def mypost(self):
        _sys_role_id=str_to_int(self.get_arg('sys_role_id'))
        _role_name=object_to_str(self.get_arg('role_name'))
        _entity = SysRoleServ.update(_sys_role_id ,_role_name )
        _rtn = {'success': True,
                'msg': 'success',
                'obj': _entity.to_dict(),
                }
        self.clear()
        self.write(_rtn)

# /api/sysdomain/SysRole/updateById?id=123456&update_params={"column_code1":"value1","column_code2":"value2"}
class ApiUpdateByIdHandler(BaseApiHandler):
    def myget(self):
        _sys_role_id = self.get_arg('id')
        _update_params = self.get_arg('update_params') #JSON格式传数据
        if _sys_role_id is None or _sys_role_id.strip() == '' \
           or _update_params is None or _update_params.strip()=='':
            self.write({
                'success':False,
                'msg':'参数错误',
            })
            return
        _update_params = json.loads(_update_params)
#将参数转换为python对象
        if _update_params.get('sys_role_id') is not None:
            _update_params['sys_role_id'] = str_to_int(_update_params.get('sys_role_id'))
        if _update_params.get('role_name') is not None:
            _update_params['role_name'] = object_to_str(_update_params.get('role_name'))
        _entity = SysRoleServ.update_by_id(_sys_role_id,_update_params)
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
    ('/api/sysdomain/SysRole/list',ApiListHandler),
    ('/api/sysdomain/SysRole/vslist',ApiVsListHandler),
    ('/api/sysdomain/SysRole/add', ApiAddHandler),
    ('/api/sysdomain/SysRole/delete', ApiDeleteHandler),
    ('/api/sysdomain/SysRole/update', ApiUpdateHandler),
    ('/api/sysdomain/SysRole/fullSearch', ApiVsFullSearchHandler),
    ('/api/sysdomain/SysRole/updateById', ApiUpdateByIdHandler),
    ]
