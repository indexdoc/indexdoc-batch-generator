from domain.sysdomain.serv import SysOrgServ
from domain.sysdomain.entity.SysOrgEntity import SysOrgEntity
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
        _entities,_cnt = SysOrgServ.get_vspage(_limit, (_page - 1) * _limit, _search_params)
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
        _entities,_cnt = SysOrgServ.full_search(_limit, (_page - 1) * _limit, _search_str)
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
        _entities,_cnt = SysOrgServ.get_page(_limit, (_page - 1) * _limit, _search_params)
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
        _org_name=object_to_str(self.get_arg('org_name'))
        _upper_id=str_to_int(self.get_arg('upper_id'))
        _sort_no=str_to_int(self.get_arg('sort_no'))
        _create_time=str_to_datetime(self.get_arg('create_time'))
        _update_time=str_to_datetime(self.get_arg('update_time'))
        _entity = SysOrgServ.create(_org_name,_upper_id,_sort_no,_create_time,_update_time)
        self.clear()
        _rtn = {'success': True,
                'msg': 'success',
                'obj': _entity.to_dict(),
                }
        self.write(_rtn)
        return

class ApiDeleteHandler(BaseApiHandler):
    def myget(self):
        _sys_org_id = int(self.get_arg('sys_org_id'))
        SysOrgServ.delete(_sys_org_id)
        _rtn = {'success': True,
                'msg': 'success',
                'obj': _sys_org_id,
                }
        self.write(_rtn)
        return


class ApiUpdateHandler(BaseApiHandler):
    def mypost(self):
        _sys_org_id=str_to_int(self.get_arg('sys_org_id'))
        _org_name=object_to_str(self.get_arg('org_name'))
        _upper_id=str_to_int(self.get_arg('upper_id'))
        _sort_no=str_to_int(self.get_arg('sort_no'))
        _create_time=str_to_datetime(self.get_arg('create_time'))
        _update_time=str_to_datetime(self.get_arg('update_time'))
        _entity = SysOrgServ.update(_sys_org_id ,_org_name ,_upper_id ,_sort_no ,_create_time ,_update_time )
        _rtn = {'success': True,
                'msg': 'success',
                'obj': _entity.to_dict(),
                }
        self.clear()
        self.write(_rtn)

# /api/sysdomain/SysOrg/updateById?id=123456&update_params={"column_code1":"value1","column_code2":"value2"}
class ApiUpdateByIdHandler(BaseApiHandler):
    def myget(self):
        _sys_org_id = self.get_arg('id')
        _update_params = self.get_arg('update_params') #JSON格式传数据
        if _sys_org_id is None or _sys_org_id.strip() == '' \
           or _update_params is None or _update_params.strip()=='':
            self.write({
                'success':False,
                'msg':'参数错误',
            })
            return
        _update_params = json.loads(_update_params)
#将参数转换为python对象
        if _update_params.get('sys_org_id') is not None:
            _update_params['sys_org_id'] = str_to_int(_update_params.get('sys_org_id'))
        if _update_params.get('org_name') is not None:
            _update_params['org_name'] = object_to_str(_update_params.get('org_name'))
        if _update_params.get('upper_id') is not None:
            _update_params['upper_id'] = str_to_int(_update_params.get('upper_id'))
        if _update_params.get('sort_no') is not None:
            _update_params['sort_no'] = str_to_int(_update_params.get('sort_no'))
        if _update_params.get('create_time') is not None:
            _update_params['create_time'] = str_to_datetime(_update_params.get('create_time'))
        if _update_params.get('update_time') is not None:
            _update_params['update_time'] = str_to_datetime(_update_params.get('update_time'))
        _entity = SysOrgServ.update_by_id(_sys_org_id,_update_params)
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
    ('/api/sysdomain/SysOrg/list',ApiListHandler),
    ('/api/sysdomain/SysOrg/vslist',ApiVsListHandler),
    ('/api/sysdomain/SysOrg/add', ApiAddHandler),
    ('/api/sysdomain/SysOrg/delete', ApiDeleteHandler),
    ('/api/sysdomain/SysOrg/update', ApiUpdateHandler),
    ('/api/sysdomain/SysOrg/fullSearch', ApiVsFullSearchHandler),
    ('/api/sysdomain/SysOrg/updateById', ApiUpdateByIdHandler),
    ]
