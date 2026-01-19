from domain.sysdomain.serv import UserFileServ
from domain.sysdomain.entity.UserFileEntity import UserFileEntity
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
        _entities,_cnt = UserFileServ.get_vspage(_limit, (_page - 1) * _limit, _search_params)
        self.write({
            'success':True,
            'code':0,
            'msg':None,
            'count': _cnt,
            'data': _entities
        })
        return


class ApiVsListHandler2(BaseApiHandler):
    def myget(self):
        _user_file_id_list = json.loads(self.get_arg('user_file_id_list'))
        _entities = UserFileServ.get_vspage2(_user_file_id_list)
        self.write({
            'success':True,
            'code':0,
            'msg':None,
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
        _entities,_cnt = UserFileServ.full_search(_limit, (_page - 1) * _limit, _search_str)
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
        _entities,_cnt = UserFileServ.get_page(_limit, (_page - 1) * _limit, _search_params)
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
        _file_uuid=object_to_str(self.get_arg('file_uuid'))
        _upload_user_id=str_to_int(self.get_arg('upload_user_id'))
        _file_name=object_to_str(self.get_arg('file_name'))
        _file_type=object_to_str(self.get_arg('file_type'))
        _content_type=object_to_str(self.get_arg('content_type'))
        _file_storage=object_to_str(self.get_arg('file_storage'))
        _cdn_url=object_to_str(self.get_arg('cdn_url'))
        _file_suffix=object_to_str(self.get_arg('file_suffix'))
        _file_content=object_to_str(self.get_arg('file_content'))
        _file_preview=object_to_str(self.get_arg('file_preview'))
        _file_summary=object_to_str(self.get_arg('file_summary'))
        _upload_time=str_to_datetime(self.get_arg('upload_time'))
        _entity = UserFileServ.create(_file_uuid,_upload_user_id,_file_name,_file_type,_content_type,_file_storage,_cdn_url,_file_suffix,_file_content,_file_preview,_file_summary,_upload_time)
        self.clear()
        _rtn = {'success': True,
                'msg': 'success',
                'obj': _entity.to_dict(),
                }
        self.write(_rtn)
        return

class ApiDeleteHandler(BaseApiHandler):
    def myget(self):
        _user_file_id = int(self.get_arg('user_file_id'))
        UserFileServ.delete(_user_file_id)
        _rtn = {'success': True,
                'msg': 'success',
                'obj': _user_file_id,
                }
        self.write(_rtn)
        return


class ApiUpdateHandler(BaseApiHandler):
    def mypost(self):
        _user_file_id=str_to_int(self.get_arg('user_file_id'))
        _file_uuid=object_to_str(self.get_arg('file_uuid'))
        _upload_user_id=str_to_int(self.get_arg('upload_user_id'))
        _file_name=object_to_str(self.get_arg('file_name'))
        _file_type=object_to_str(self.get_arg('file_type'))
        _content_type=object_to_str(self.get_arg('content_type'))
        _file_storage=object_to_str(self.get_arg('file_storage'))
        _cdn_url=object_to_str(self.get_arg('cdn_url'))
        _file_suffix=object_to_str(self.get_arg('file_suffix'))
        _file_content=object_to_str(self.get_arg('file_content'))
        _file_preview=object_to_str(self.get_arg('file_preview'))
        _file_summary=object_to_str(self.get_arg('file_summary'))
        _upload_time=str_to_datetime(self.get_arg('upload_time'))
        _entity = UserFileServ.update(_user_file_id ,_file_uuid ,_upload_user_id ,_file_name ,_file_type ,_content_type ,_file_storage ,_cdn_url ,_file_suffix ,_file_content ,_file_preview ,_file_summary ,_upload_time )
        _rtn = {'success': True,
                'msg': 'success',
                'obj': _entity.to_dict(),
                }
        self.clear()
        self.write(_rtn)

# /api/sysdomain/UserFile/updateById?id=123456&update_params={"column_code1":"value1","column_code2":"value2"}
class ApiUpdateByIdHandler(BaseApiHandler):
    def myget(self):
        _user_file_id = self.get_arg('id')
        _update_params = self.get_arg('update_params') #JSON格式传数据
        if _user_file_id is None or _user_file_id.strip() == '' \
           or _update_params is None or _update_params.strip()=='':
            self.write({
                'success':False,
                'msg':'参数错误',
            })
            return
        _update_params = json.loads(_update_params)
#将参数转换为python对象
        if _update_params.get('user_file_id') is not None:
            _update_params['user_file_id'] = str_to_int(_update_params.get('user_file_id'))
        if _update_params.get('file_uuid') is not None:
            _update_params['file_uuid'] = object_to_str(_update_params.get('file_uuid'))
        if _update_params.get('upload_user_id') is not None:
            _update_params['upload_user_id'] = str_to_int(_update_params.get('upload_user_id'))
        if _update_params.get('file_name') is not None:
            _update_params['file_name'] = object_to_str(_update_params.get('file_name'))
        if _update_params.get('file_type') is not None:
            _update_params['file_type'] = object_to_str(_update_params.get('file_type'))
        if _update_params.get('content_type') is not None:
            _update_params['content_type'] = object_to_str(_update_params.get('content_type'))
        if _update_params.get('file_storage') is not None:
            _update_params['file_storage'] = object_to_str(_update_params.get('file_storage'))
        if _update_params.get('cdn_url') is not None:
            _update_params['cdn_url'] = object_to_str(_update_params.get('cdn_url'))
        if _update_params.get('file_suffix') is not None:
            _update_params['file_suffix'] = object_to_str(_update_params.get('file_suffix'))
        if _update_params.get('file_content') is not None:
            _update_params['file_content'] = object_to_str(_update_params.get('file_content'))
        if _update_params.get('file_preview') is not None:
            _update_params['file_preview'] = object_to_str(_update_params.get('file_preview'))
        if _update_params.get('file_summary') is not None:
            _update_params['file_summary'] = object_to_str(_update_params.get('file_summary'))
        if _update_params.get('upload_time') is not None:
            _update_params['upload_time'] = str_to_datetime(_update_params.get('upload_time'))
        _entity = UserFileServ.update_by_id(_user_file_id,_update_params)
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
    ('/api/sysdomain/UserFile/list',ApiListHandler),
    ('/api/sysdomain/UserFile/vslist',ApiVsListHandler),
    ('/api/sysdomain/UserFile/vslist2',ApiVsListHandler2),
    ('/api/sysdomain/UserFile/add', ApiAddHandler),
    ('/api/sysdomain/UserFile/delete', ApiDeleteHandler),
    ('/api/sysdomain/UserFile/update', ApiUpdateHandler),
    ('/api/sysdomain/UserFile/fullSearch', ApiVsFullSearchHandler),
    ('/api/sysdomain/UserFile/updateById', ApiUpdateByIdHandler),
    ]
