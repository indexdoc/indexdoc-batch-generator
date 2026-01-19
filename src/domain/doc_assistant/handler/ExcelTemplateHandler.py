from domain.doc_assistant.serv import ExcelTemplateServ
from domain.doc_assistant.entity.ExcelTemplateEntity import ExcelTemplateEntity
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
        _entities,_cnt = ExcelTemplateServ.get_vspage(_limit, (_page - 1) * _limit, _search_params)
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
        _entities,_cnt = ExcelTemplateServ.full_search(_limit, (_page - 1) * _limit, _search_str)
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
        _entities,_cnt = ExcelTemplateServ.get_page(_limit, (_page - 1) * _limit, _search_params)
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
        _user_file_id=str_to_int(self.get_arg('user_file_id'))
        _create_time=str_to_datetime(self.get_arg('create_time'))
        _entity = ExcelTemplateServ.create(_user_file_id,_create_time)
        self.clear()
        _rtn = {'success': True,
                'msg': 'success',
                'obj': _entity.to_dict(),
                }
        self.write(_rtn)
        return

class ApiDeleteHandler(BaseApiHandler):
    def myget(self):
        _excel_template_id = int(self.get_arg('excel_template_id'))
        ExcelTemplateServ.delete(_excel_template_id)
        _rtn = {'success': True,
                'msg': 'success',
                'obj': _excel_template_id,
                }
        self.write(_rtn)
        return


class ApiUpdateHandler(BaseApiHandler):
    def mypost(self):
        _excel_template_id=str_to_int(self.get_arg('excel_template_id'))
        _user_file_id=str_to_int(self.get_arg('user_file_id'))
        _create_time=str_to_datetime(self.get_arg('create_time'))
        _entity = ExcelTemplateServ.update(_excel_template_id ,_user_file_id ,_create_time )
        _rtn = {'success': True,
                'msg': 'success',
                'obj': _entity.to_dict(),
                }
        self.clear()
        self.write(_rtn)

# /api/doc_assistant/ExcelTemplate/updateById?id=123456&update_params={"column_code1":"value1","column_code2":"value2"}
class ApiUpdateByIdHandler(BaseApiHandler):
    def myget(self):
        _excel_template_id = self.get_arg('id')
        _update_params = self.get_arg('update_params') #JSON格式传数据
        if _excel_template_id is None or _excel_template_id.strip() == '' \
           or _update_params is None or _update_params.strip()=='':
            self.write({
                'success':False,
                'msg':'参数错误',
            })
            return
        _update_params = json.loads(_update_params)
#将参数转换为python对象
        if _update_params.get('excel_template_id') is not None:
            _update_params['excel_template_id'] = str_to_int(_update_params.get('excel_template_id'))
        if _update_params.get('user_file_id') is not None:
            _update_params['user_file_id'] = str_to_int(_update_params.get('user_file_id'))
        if _update_params.get('create_time') is not None:
            _update_params['create_time'] = str_to_datetime(_update_params.get('create_time'))
        _entity = ExcelTemplateServ.update_by_id(_excel_template_id,_update_params)
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
    ('/api/doc_assistant/ExcelTemplate/list',ApiListHandler),
    ('/api/doc_assistant/ExcelTemplate/vslist',ApiVsListHandler),
    ('/api/doc_assistant/ExcelTemplate/add', ApiAddHandler),
    ('/api/doc_assistant/ExcelTemplate/delete', ApiDeleteHandler),
    ('/api/doc_assistant/ExcelTemplate/update', ApiUpdateHandler),
    ('/api/doc_assistant/ExcelTemplate/fullSearch', ApiVsFullSearchHandler),
    ('/api/doc_assistant/ExcelTemplate/updateById', ApiUpdateByIdHandler),
    ]
