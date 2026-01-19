from domain.sysdomain.view import ViewUserUseNumDaoCK
from BaseHandler import BaseApiHandler
from tornado.web import authenticated
from utils import PageUtil
import logging
import traceback
import json


class ApiListHandler(BaseApiHandler):
    def myget(self):
        _limit = self.get_arg('limit')
        _page = self.get_arg('page')
        _search_params = self.get_arg('searchParams') #JSON格式传数据
        _limit = 50000 if _limit is None else int(_limit)
        _page = 1 if _page is None else int(_page)
        if _search_params is not None:
            _search_params = json.loads(_search_params)
        _dict_list,_cnt = ViewUserUseNumDaoCK.select_page(int(_limit), (int(_page) - 1) * int(_limit),_search_params)
        self.write({
            'success':True,
            'code':0,
            'msg':None,
            'count': _cnt,
            'data': _dict_list
        })

class ApiFullSearchHandler(BaseApiHandler):
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
        _dict_list,_cnt = ViewUserUseNumDaoCK.full_search(_search_str, _limit, (_page - 1) * _limit)
        self.write({
            'success':True,
            'code':0,
            'msg':None,
            'count': _cnt,
            'data': _dict_list
        })
        return


urls =[
    ('/api/sysdomain/ViewUserUseNum/list',ApiListHandler),
    ('/api/sysdomain/ViewUserUseNum/fullSearch', ApiFullSearchHandler),
    ]
