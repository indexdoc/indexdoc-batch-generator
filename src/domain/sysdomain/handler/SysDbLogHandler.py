from domain.sysdomain.serv import SysDbLogServ
from domain.sysdomain.entity.SysDbLogEntity import SysDbLogEntity
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
        _entities,_cnt = SysDbLogServ.get_vspage(_limit, (_page - 1) * _limit, _search_params)
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
        _entities,_cnt = SysDbLogServ.full_search(_limit, (_page - 1) * _limit, _search_str)
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
        _entities,_cnt = SysDbLogServ.get_page(_limit, (_page - 1) * _limit, _search_params)
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
        _sys_user_id=str_to_int(self.get_arg('sys_user_id'))
        _op_datetime=str_to_datetime(self.get_arg('op_datetime'))
        _op_duration=str_to_float(self.get_arg('op_duration'))
        _op_type=object_to_str(self.get_arg('op_type'))
        _table_code=object_to_str(self.get_arg('table_code'))
        _data_id=str_to_int(self.get_arg('data_id'))
        _sql_str=object_to_str(self.get_arg('sql_str'))
        _sql_param=object_to_str(self.get_arg('sql_param'))
        _sql_result=object_to_str(self.get_arg('sql_result'))
        _entity = SysDbLogServ.create(_sys_user_id,_op_datetime,_op_duration,_op_type,_table_code,_data_id,_sql_str,_sql_param,_sql_result)
        self.clear()
        _rtn = {'success': True,
                'msg': 'success',
                'obj': _entity.to_dict(),
                }
        self.write(_rtn)
        return

class ApiDeleteHandler(BaseApiHandler):
    def myget(self):
        _sys_db_log_id = int(self.get_arg('sys_db_log_id'))
        SysDbLogServ.delete(_sys_db_log_id)
        _rtn = {'success': True,
                'msg': 'success',
                'obj': _sys_db_log_id,
                }
        self.write(_rtn)
        return


class ApiUpdateHandler(BaseApiHandler):
    def mypost(self):
        _sys_db_log_id=str_to_int(self.get_arg('sys_db_log_id'))
        _sys_user_id=str_to_int(self.get_arg('sys_user_id'))
        _op_datetime=str_to_datetime(self.get_arg('op_datetime'))
        _op_duration=str_to_float(self.get_arg('op_duration'))
        _op_type=object_to_str(self.get_arg('op_type'))
        _table_code=object_to_str(self.get_arg('table_code'))
        _data_id=str_to_int(self.get_arg('data_id'))
        _sql_str=object_to_str(self.get_arg('sql_str'))
        _sql_param=object_to_str(self.get_arg('sql_param'))
        _sql_result=object_to_str(self.get_arg('sql_result'))
        _entity = SysDbLogServ.update(_sys_db_log_id ,_sys_user_id ,_op_datetime ,_op_duration ,_op_type ,_table_code ,_data_id ,_sql_str ,_sql_param ,_sql_result )
        _rtn = {'success': True,
                'msg': 'success',
                'obj': _entity.to_dict(),
                }
        self.clear()
        self.write(_rtn)

# /api/sysdomain/SysDbLog/updateById?id=123456&update_params={"column_code1":"value1","column_code2":"value2"}
class ApiUpdateByIdHandler(BaseApiHandler):
    def myget(self):
        _sys_db_log_id = self.get_arg('id')
        _update_params = self.get_arg('update_params') #JSON格式传数据
        if _sys_db_log_id is None or _sys_db_log_id.strip() == '' \
           or _update_params is None or _update_params.strip()=='':
            self.write({
                'success':False,
                'msg':'参数错误',
            })
            return
        _update_params = json.loads(_update_params)
#将参数转换为python对象
        if _update_params.get('sys_db_log_id') is not None:
            _update_params['sys_db_log_id'] = str_to_int(_update_params.get('sys_db_log_id'))
        if _update_params.get('sys_user_id') is not None:
            _update_params['sys_user_id'] = str_to_int(_update_params.get('sys_user_id'))
        if _update_params.get('op_datetime') is not None:
            _update_params['op_datetime'] = str_to_datetime(_update_params.get('op_datetime'))
        if _update_params.get('op_duration') is not None:
            _update_params['op_duration'] = str_to_float(_update_params.get('op_duration'))
        if _update_params.get('op_type') is not None:
            _update_params['op_type'] = object_to_str(_update_params.get('op_type'))
        if _update_params.get('table_code') is not None:
            _update_params['table_code'] = object_to_str(_update_params.get('table_code'))
        if _update_params.get('data_id') is not None:
            _update_params['data_id'] = str_to_int(_update_params.get('data_id'))
        if _update_params.get('sql_str') is not None:
            _update_params['sql_str'] = object_to_str(_update_params.get('sql_str'))
        if _update_params.get('sql_param') is not None:
            _update_params['sql_param'] = object_to_str(_update_params.get('sql_param'))
        if _update_params.get('sql_result') is not None:
            _update_params['sql_result'] = object_to_str(_update_params.get('sql_result'))
        _entity = SysDbLogServ.update_by_id(_sys_db_log_id,_update_params)
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
    ('/api/sysdomain/SysDbLog/list',ApiListHandler),
    ('/api/sysdomain/SysDbLog/vslist',ApiVsListHandler),
    ('/api/sysdomain/SysDbLog/add', ApiAddHandler),
    ('/api/sysdomain/SysDbLog/delete', ApiDeleteHandler),
    ('/api/sysdomain/SysDbLog/update', ApiUpdateHandler),
    ('/api/sysdomain/SysDbLog/fullSearch', ApiVsFullSearchHandler),
    ('/api/sysdomain/SysDbLog/updateById', ApiUpdateByIdHandler),
    ]
