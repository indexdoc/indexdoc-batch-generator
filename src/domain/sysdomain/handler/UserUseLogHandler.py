from domain.sysdomain.serv import UserUseLogServ
from domain.sysdomain.entity.UserUseLogEntity import UserUseLogEntity
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
        _entities,_cnt = UserUseLogServ.get_vspage(_limit, (_page - 1) * _limit, _search_params)
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
        _entities,_cnt = UserUseLogServ.full_search(_limit, (_page - 1) * _limit, _search_str)
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
        _entities,_cnt = UserUseLogServ.get_page(_limit, (_page - 1) * _limit, _search_params)
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
        _ip_addr=object_to_str(self.get_arg('ip_addr'))
        _local_ip=object_to_str(self.get_arg('local_ip'))
        _api_url=object_to_str(self.get_arg('api_url'))
        _gpu_info=object_to_str(self.get_arg('gpu_info'))
        _remark=object_to_str(self.get_arg('remark'))
        _create_time=str_to_datetime(self.get_arg('create_time'))
        _entity = UserUseLogServ.create(_sys_user_id,_ip_addr,_local_ip,_api_url,_gpu_info,_remark,_create_time)
        self.clear()
        _rtn = {'success': True,
                'msg': 'success',
                'obj': _entity.to_dict(),
                }
        self.write(_rtn)
        return

class ApiDeleteHandler(BaseApiHandler):
    def myget(self):
        _user_use_log_id = int(self.get_arg('user_use_log_id'))
        UserUseLogServ.delete(_user_use_log_id)
        _rtn = {'success': True,
                'msg': 'success',
                'obj': _user_use_log_id,
                }
        self.write(_rtn)
        return


class ApiUpdateHandler(BaseApiHandler):
    def mypost(self):
        _user_use_log_id=str_to_int(self.get_arg('user_use_log_id'))
        _sys_user_id=str_to_int(self.get_arg('sys_user_id'))
        _ip_addr=object_to_str(self.get_arg('ip_addr'))
        _local_ip=object_to_str(self.get_arg('local_ip'))
        _api_url=object_to_str(self.get_arg('api_url'))
        _gpu_info=object_to_str(self.get_arg('gpu_info'))
        _remark=object_to_str(self.get_arg('remark'))
        _create_time=str_to_datetime(self.get_arg('create_time'))
        _entity = UserUseLogServ.update(_user_use_log_id ,_sys_user_id ,_ip_addr ,_local_ip ,_api_url ,_gpu_info ,_remark ,_create_time )
        _rtn = {'success': True,
                'msg': 'success',
                'obj': _entity.to_dict(),
                }
        self.clear()
        self.write(_rtn)

# /api/sysdomain/UserUseLog/updateById?id=123456&update_params={"column_code1":"value1","column_code2":"value2"}
class ApiUpdateByIdHandler(BaseApiHandler):
    def myget(self):
        _user_use_log_id = self.get_arg('id')
        _update_params = self.get_arg('update_params') #JSON格式传数据
        if _user_use_log_id is None or _user_use_log_id.strip() == '' \
           or _update_params is None or _update_params.strip()=='':
            self.write({
                'success':False,
                'msg':'参数错误',
            })
            return
        _update_params = json.loads(_update_params)
#将参数转换为python对象
        if _update_params.get('user_use_log_id') is not None:
            _update_params['user_use_log_id'] = str_to_int(_update_params.get('user_use_log_id'))
        if _update_params.get('sys_user_id') is not None:
            _update_params['sys_user_id'] = str_to_int(_update_params.get('sys_user_id'))
        if _update_params.get('ip_addr') is not None:
            _update_params['ip_addr'] = object_to_str(_update_params.get('ip_addr'))
        if _update_params.get('local_ip') is not None:
            _update_params['local_ip'] = object_to_str(_update_params.get('local_ip'))
        if _update_params.get('api_url') is not None:
            _update_params['api_url'] = object_to_str(_update_params.get('api_url'))
        if _update_params.get('gpu_info') is not None:
            _update_params['gpu_info'] = object_to_str(_update_params.get('gpu_info'))
        if _update_params.get('remark') is not None:
            _update_params['remark'] = object_to_str(_update_params.get('remark'))
        if _update_params.get('create_time') is not None:
            _update_params['create_time'] = str_to_datetime(_update_params.get('create_time'))
        _entity = UserUseLogServ.update_by_id(_user_use_log_id,_update_params)
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
    ('/api/sysdomain/UserUseLog/list',ApiListHandler),
    ('/api/sysdomain/UserUseLog/vslist',ApiVsListHandler),
    ('/api/sysdomain/UserUseLog/add', ApiAddHandler),
    ('/api/sysdomain/UserUseLog/delete', ApiDeleteHandler),
    ('/api/sysdomain/UserUseLog/update', ApiUpdateHandler),
    ('/api/sysdomain/UserUseLog/fullSearch', ApiVsFullSearchHandler),
    ('/api/sysdomain/UserUseLog/updateById', ApiUpdateByIdHandler),
    ]
