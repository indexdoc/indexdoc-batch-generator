import threading
from tornado.web import RequestHandler

import SysCache

import config
import os

from domain.sysdomain.daock import UserFileDaoCK

from BaseHandler import  BaseApiHandler

class ApiGetTmpFileHandler(BaseApiHandler):
    need_login = False

    def myget(self, *args, **kwargs):
        _file_name = self.get_arg('file_name')
        filepath = config.tmp_path + '/' + _file_name
        # 获取文件扩展名
        file_extension = os.path.splitext(_file_name)[1].lower()

        # 设置默认的 Content-Type
        content_type = 'application/octet-stream'

        # 根据文件扩展名设置合适的 Content-Type
        if file_extension == '.xlsx':  # Excel 文件
            content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        elif file_extension == '.xls':  # Excel 97-2003 文件
            content_type = 'application/vnd.ms-excel'
        elif file_extension == '.docx':  # Word 文件
            content_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        elif file_extension == '.doc':  # Word 97-2003 文件
            content_type = 'application/msword'

        # 设置响应头
        self.set_header('Content-Type', content_type)
        self.set_header('Content-Disposition', f'attachment; filename={_file_name}')
        with open(filepath, 'rb') as f:
            while True:
                data = f.read(4096)
                if not data:
                    break
                self.write(data)
                # self.flush()  # 此处可能会报错
        return

class ApiGetFileHandler(BaseApiHandler):
    # todo 以下代码并没有进行过测试！
    need_login = False

    def myget(self, *args, **kwargs):
        user = self.current_user
        # if user is None:
        #     self.clear()
        #     _rtn = {'success': False,
        #             'msg': '文件不存在！',
        #             'obj': None,
        #             }
        #     self.write(_rtn)
        #     return
        _file_name = args[0]
        _entitylist = UserFileDaoCK.select_by_FileStorage(_file_name)
        if _entitylist is None or len(_entitylist) < 1:
            self.clear()
            _rtn = {'success': False,
                    'msg': '文件不存在！',
                    'obj': None,
                    }
            self.write(_rtn)
            return
        _fileentity = _entitylist[0]
        filepath = config.user_file_path + '/upload/' + _file_name
        self.set_header('Content-Type', _fileentity.content_type)
        with open(filepath, 'rb') as f:
            while True:
                data = f.read(4096)
                if not data:
                    break
                self.write(data)
                # self.flush()  # 此处可能会报错
        return



# 支持小于100M的文件上传
from utils import IDUtil, FileUtil


class ApiGetUUid(BaseApiHandler):
    # @coroutine
    def post(self):
        _rtn = {'success': True,
                'msg': 'success！',
                'data': IDUtil.get_uuid(),
                'status': '200',
                }
        self.write(_rtn)


urls = [
    ('/api/getUUid', ApiGetUUid),
	(r'/api/file/(.*)', ApiGetFileHandler),
    ('/api/tmpfile', ApiGetTmpFileHandler)
]
