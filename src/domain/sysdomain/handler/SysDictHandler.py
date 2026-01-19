from domain.sysdomain.serv import SysDictServ
from domain.sysdomain.entity.SysDictEntity import SysDictEntity
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
        _entities,_cnt = SysDictServ.get_vspage(_limit, (_page - 1) * _limit, _search_params)
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
        _entities,_cnt = SysDictServ.full_search(_limit, (_page - 1) * _limit, _search_str)
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
        _entities,_cnt = SysDictServ.get_page(_limit, (_page - 1) * _limit, _search_params)
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
        _module_name=object_to_str(self.get_arg('module_name'))
        _table_name=object_to_str(self.get_arg('table_name'))
        _column_name=object_to_str(self.get_arg('column_name'))
        _select_mode=object_to_str(self.get_arg('select_mode'))
        _data_value=object_to_str(self.get_arg('data_value'))
        _remark=object_to_str(self.get_arg('remark'))
        _entity = SysDictServ.create(_module_name,_table_name,_column_name,_select_mode,_data_value,_remark)
        self.clear()
        _rtn = {'success': True,
                'msg': 'success',
                'obj': _entity.to_dict(),
                }
        self.write(_rtn)
        return

class ApiDeleteHandler(BaseApiHandler):
    def myget(self):
        _sys_dict_id = int(self.get_arg('sys_dict_id'))
        SysDictServ.delete(_sys_dict_id)
        _rtn = {'success': True,
                'msg': 'success',
                'obj': _sys_dict_id,
                }
        self.write(_rtn)
        return


class ApiUpdateHandler(BaseApiHandler):
    def mypost(self):
        _sys_dict_id=str_to_int(self.get_arg('sys_dict_id'))
        _module_name=object_to_str(self.get_arg('module_name'))
        _table_name=object_to_str(self.get_arg('table_name'))
        _column_name=object_to_str(self.get_arg('column_name'))
        _select_mode=object_to_str(self.get_arg('select_mode'))
        _data_value=object_to_str(self.get_arg('data_value'))
        _remark=object_to_str(self.get_arg('remark'))
        _entity = SysDictServ.update(_sys_dict_id ,_module_name ,_table_name ,_column_name ,_select_mode ,_data_value ,_remark )
        _rtn = {'success': True,
                'msg': 'success',
                'obj': _entity.to_dict(),
                }
        self.clear()
        self.write(_rtn)

# /api/sysdomain/SysDict/updateById?id=123456&update_params={"column_code1":"value1","column_code2":"value2"}
class ApiUpdateByIdHandler(BaseApiHandler):
    def myget(self):
        _sys_dict_id = self.get_arg('id')
        _update_params = self.get_arg('update_params') #JSON格式传数据
        if _sys_dict_id is None or _sys_dict_id.strip() == '' \
           or _update_params is None or _update_params.strip()=='':
            self.write({
                'success':False,
                'msg':'参数错误',
            })
            return
        _update_params = json.loads(_update_params)
#将参数转换为python对象
        if _update_params.get('sys_dict_id') is not None:
            _update_params['sys_dict_id'] = str_to_int(_update_params.get('sys_dict_id'))
        if _update_params.get('module_name') is not None:
            _update_params['module_name'] = object_to_str(_update_params.get('module_name'))
        if _update_params.get('table_name') is not None:
            _update_params['table_name'] = object_to_str(_update_params.get('table_name'))
        if _update_params.get('column_name') is not None:
            _update_params['column_name'] = object_to_str(_update_params.get('column_name'))
        if _update_params.get('select_mode') is not None:
            _update_params['select_mode'] = object_to_str(_update_params.get('select_mode'))
        if _update_params.get('data_value') is not None:
            _update_params['data_value'] = object_to_str(_update_params.get('data_value'))
        if _update_params.get('remark') is not None:
            _update_params['remark'] = object_to_str(_update_params.get('remark'))
        _entity = SysDictServ.update_by_id(_sys_dict_id,_update_params)
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
    ('/api/sysdomain/SysDict/list',ApiListHandler),
    ('/api/sysdomain/SysDict/vslist',ApiVsListHandler),
    ('/api/sysdomain/SysDict/add', ApiAddHandler),
    ('/api/sysdomain/SysDict/delete', ApiDeleteHandler),
    ('/api/sysdomain/SysDict/update', ApiUpdateHandler),
    ('/api/sysdomain/SysDict/fullSearch', ApiVsFullSearchHandler),
    ('/api/sysdomain/SysDict/updateById', ApiUpdateByIdHandler),
    ]
