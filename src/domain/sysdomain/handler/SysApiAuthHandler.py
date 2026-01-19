from domain.sysdomain.serv import SysApiAuthServ
from domain.sysdomain.entity.SysApiAuthEntity import SysApiAuthEntity
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
        _entities,_cnt = SysApiAuthServ.get_vspage(_limit, (_page - 1) * _limit, _search_params)
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
        _entities,_cnt = SysApiAuthServ.full_search(_limit, (_page - 1) * _limit, _search_str)
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
        _entities,_cnt = SysApiAuthServ.get_page(_limit, (_page - 1) * _limit, _search_params)
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
        _api_name=object_to_str(self.get_arg('api_name'))
        _api_url=object_to_str(self.get_arg('api_url'))
        _sys_user_id=str_to_int(self.get_arg('sys_user_id'))
        _sys_role_id=str_to_int(self.get_arg('sys_role_id'))
        _sys_org_id=str_to_int(self.get_arg('sys_org_id'))
        _org_duty_id=str_to_int(self.get_arg('org_duty_id'))
        _auth_flag=object_to_str(self.get_arg('auth_flag'))
        _sys_menu_auth_id=str_to_int(self.get_arg('sys_menu_auth_id'))
        _update_type=object_to_str(self.get_arg('update_type'))
        _remark=object_to_str(self.get_arg('remark'))
        _entity = SysApiAuthServ.create(_api_name,_api_url,_sys_user_id,_sys_role_id,_sys_org_id,_org_duty_id,_auth_flag,_sys_menu_auth_id,_update_type,_remark)
        self.clear()
        _rtn = {'success': True,
                'msg': 'success',
                'obj': _entity.to_dict(),
                }
        self.write(_rtn)
        return

class ApiDeleteHandler(BaseApiHandler):
    def myget(self):
        _sys_api_auth_id = int(self.get_arg('sys_api_auth_id'))
        SysApiAuthServ.delete(_sys_api_auth_id)
        _rtn = {'success': True,
                'msg': 'success',
                'obj': _sys_api_auth_id,
                }
        self.write(_rtn)
        return


class ApiUpdateHandler(BaseApiHandler):
    def mypost(self):
        _sys_api_auth_id=str_to_int(self.get_arg('sys_api_auth_id'))
        _api_name=object_to_str(self.get_arg('api_name'))
        _api_url=object_to_str(self.get_arg('api_url'))
        _sys_user_id=str_to_int(self.get_arg('sys_user_id'))
        _sys_role_id=str_to_int(self.get_arg('sys_role_id'))
        _sys_org_id=str_to_int(self.get_arg('sys_org_id'))
        _org_duty_id=str_to_int(self.get_arg('org_duty_id'))
        _auth_flag=object_to_str(self.get_arg('auth_flag'))
        _sys_menu_auth_id=str_to_int(self.get_arg('sys_menu_auth_id'))
        _update_type=object_to_str(self.get_arg('update_type'))
        _remark=object_to_str(self.get_arg('remark'))
        _entity = SysApiAuthServ.update(_sys_api_auth_id ,_api_name ,_api_url ,_sys_user_id ,_sys_role_id ,_sys_org_id ,_org_duty_id ,_auth_flag ,_sys_menu_auth_id ,_update_type ,_remark )
        _rtn = {'success': True,
                'msg': 'success',
                'obj': _entity.to_dict(),
                }
        self.clear()
        self.write(_rtn)

# /api/sysdomain/SysApiAuth/updateById?id=123456&update_params={"column_code1":"value1","column_code2":"value2"}
class ApiUpdateByIdHandler(BaseApiHandler):
    def myget(self):
        _sys_api_auth_id = self.get_arg('id')
        _update_params = self.get_arg('update_params') #JSON格式传数据
        if _sys_api_auth_id is None or _sys_api_auth_id.strip() == '' \
           or _update_params is None or _update_params.strip()=='':
            self.write({
                'success':False,
                'msg':'参数错误',
            })
            return
        _update_params = json.loads(_update_params)
#将参数转换为python对象
        if _update_params.get('sys_api_auth_id') is not None:
            _update_params['sys_api_auth_id'] = str_to_int(_update_params.get('sys_api_auth_id'))
        if _update_params.get('api_name') is not None:
            _update_params['api_name'] = object_to_str(_update_params.get('api_name'))
        if _update_params.get('api_url') is not None:
            _update_params['api_url'] = object_to_str(_update_params.get('api_url'))
        if _update_params.get('sys_user_id') is not None:
            _update_params['sys_user_id'] = str_to_int(_update_params.get('sys_user_id'))
        if _update_params.get('sys_role_id') is not None:
            _update_params['sys_role_id'] = str_to_int(_update_params.get('sys_role_id'))
        if _update_params.get('sys_org_id') is not None:
            _update_params['sys_org_id'] = str_to_int(_update_params.get('sys_org_id'))
        if _update_params.get('org_duty_id') is not None:
            _update_params['org_duty_id'] = str_to_int(_update_params.get('org_duty_id'))
        if _update_params.get('auth_flag') is not None:
            _update_params['auth_flag'] = object_to_str(_update_params.get('auth_flag'))
        if _update_params.get('sys_menu_auth_id') is not None:
            _update_params['sys_menu_auth_id'] = str_to_int(_update_params.get('sys_menu_auth_id'))
        if _update_params.get('update_type') is not None:
            _update_params['update_type'] = object_to_str(_update_params.get('update_type'))
        if _update_params.get('remark') is not None:
            _update_params['remark'] = object_to_str(_update_params.get('remark'))
        _entity = SysApiAuthServ.update_by_id(_sys_api_auth_id,_update_params)
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
    ('/api/sysdomain/SysApiAuth/list',ApiListHandler),
    ('/api/sysdomain/SysApiAuth/vslist',ApiVsListHandler),
    ('/api/sysdomain/SysApiAuth/add', ApiAddHandler),
    ('/api/sysdomain/SysApiAuth/delete', ApiDeleteHandler),
    ('/api/sysdomain/SysApiAuth/update', ApiUpdateHandler),
    ('/api/sysdomain/SysApiAuth/fullSearch', ApiVsFullSearchHandler),
    ('/api/sysdomain/SysApiAuth/updateById', ApiUpdateByIdHandler),
    ]
