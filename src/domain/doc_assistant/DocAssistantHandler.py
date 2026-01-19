import os
import re
import shutil
import zipfile

import docx

import config
from BaseHandler import BaseApiHandler

from domain.sysdomain.daock import UserFileDaoCK
from domain.sysdomain.serv import UserFileServ
from utils import IDUtil
from utils.FileUtil import get_file_suffix
from utils.IDUtil import get_uuid
from utils.ToPdfUtil import convert_file_to_pdf
from utils.TypeCvt import *
import logging
import traceback
import json


class ApiGetbatchFileHandler(BaseApiHandler):
    # todo 以下代码并没有进行过测试！
    need_login = False

    def mypost(self):
        # Excel文件选中行数据
        _checkdata = json.loads(self.get_arg('checkdata'))
        if len(_checkdata) == 1:
            for item in _checkdata:
                if 'generateword' in item:
                    _file_name = item['generateword']
                    if '/' in _file_name:
                        _generate_file_storage = item['rowid'] + '/' + _file_name
                        _generate_file_name = os.path.splitext(_file_name)[0] + '.zip'
                    else:
                        _generate_file_storage = item['rowid'] + '.docx'
                        _generate_file_name = _file_name
            _rtn = {'success': True,
                    'msg': '下载成功！',
                    'status': '200',
                    'generate_file_storage': _generate_file_storage,
                    'generate_file_name': _generate_file_name,
                    }
            self.write(_rtn)
            return
        if len(_checkdata) > 1:
            file_paths = []
            name_mapping = dict()
            for item in _checkdata:
                if 'generateword' in item:
                    _file_name = item['generateword']
                    if '/' in _file_name:
                        file_uuid = item['rowid']
                        directory_to_zip = config.user_file_path + '/output/' + file_uuid
                        zip_file_name = config.user_file_path + '/output/' + file_uuid + '.zip'
                        zip_directory(directory_to_zip, zip_file_name)
                        file_paths.append(zip_file_name)
                        name_mapping[zip_file_name] = _file_name
                    else:
                        _file_storage = config.user_file_path + '/output/' + item['rowid'] + '.docx'
                        file_paths.append(_file_storage)
                        name_mapping[_file_storage] = _file_name

            # 获取当前时间
            now = datetime.datetime.now()
            # 格式化时间为字符串
            timestamp = now.strftime('%Y%m%d_%H%M%S')
            zip_file_name = 'output' + timestamp + '.zip'
            output_dir = config.user_file_path + '/output/'
            filepath = output_dir + zip_file_name
            # 调用函数
            zip_files(file_paths, zip_file_name, output_dir, name_mapping)
            _rtn = {'success': True,
                    'msg': '下载成功！',
                    'status': '200',
                    'generate_file_storage': zip_file_name,
                    'generate_file_name': zip_file_name,
                    }
            self.write(_rtn)
            return


class ApiGetoneFileHandler(BaseApiHandler):
    # todo 以下代码并没有进行过测试！
    need_login = False

    def myget(self, *args, **kwargs):
        user = self.current_user
        _file_name = args[0]
        if get_file_suffix(_file_name) == '.zip':
            zip_file_name = config.user_file_path + '/output/' + _file_name
            self.set_header('Content-Type', 'application/zip')
            self.set_header('Content-Disposition', 'attachment;')
            self.set_header('Content-Length', os.path.getsize(zip_file_name))
            with open(zip_file_name, 'rb') as f:
                while True:
                    data = f.read(4096)
                    if not data:
                        break
                    self.write(data)
        else:
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
            if _fileentity.file_uuid + '/' in _file_name:
                file_uuid = _fileentity.file_uuid
                directory_to_zip = config.user_file_path + '/output/' + file_uuid
                zip_file_name = config.user_file_path + '/output/' + file_uuid + '.zip'
                zip_directory(directory_to_zip, zip_file_name)
                filepath = zip_file_name
                self.set_header('Content-Type', 'application/zip')
                self.set_header('Content-Disposition', 'attachment;')
                self.set_header('Content-Length', os.path.getsize(filepath))
                with open(filepath, 'rb') as f:
                    while True:
                        data = f.read(4096)
                        if not data:
                            break
                        self.write(data)
            else:
                filepath = config.user_file_path + '/output/' + _file_name
                self.set_header('Content-Type', 'application/octet-stream')
                with open(filepath, 'rb') as f:
                    while True:
                        data = f.read(4096)
                        if not data:
                            break
                        self.write(data)
                        # self.flush()  # 此处可能会报错
        return


# 批量文档助手文件上传
class ApiUploadFileHandler(BaseApiHandler):
    need_login = False  # 登录后才能调用

    def mypost(self):
        _gpuInfo = self.get_arg('gpuInfo')
        _local_ip = self.get_arg('local_ip')
        upload_path = config.user_file_path + '/upload/'  # 文件的暂存路径
        if not os.path.exists(upload_path):
            os.makedirs(upload_path)
        file_metas = self.request.files.get('file', None)  # 提取表单中‘name’为‘file’的文件元数据
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.set_header('Access-Control-Allow-Headers',
                        'DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range')

        if not file_metas:
            _rtn = {'success': False,
                    'msg': '文件为空！',
                    'obj': None,
                    }
            self.write(_rtn)
            return
        if len(file_metas) == 0:
            _rtn = {'success': False,
                    'msg': '文件为空！',
                    'obj': None,
                    }
            self.write(_rtn)
            return
        file_meta = file_metas[0]

        try:
            # _file_uuid = self.get_argument('uuid')
            _file_uuid = get_uuid()
            _file_suffix = '.' + self.get_argument('fileExt')
            _file_storage_name = _file_uuid + _file_suffix
            _file_path = upload_path + _file_storage_name
            _file_name = self.get_argument('fileName') + _file_suffix
            chunk = int(self.get_argument('page', 0))
            chunks = int(self.get_argument('totalPage', 0))
            if chunks == 1:
                with open(_file_path, 'wb') as upfile:
                    upfile.write(file_meta['body'])
                    upfile.close()
            else:
                with open(_file_path, 'ab') as upfile:
                    # upfile.seek(chunk*self.options.chunk_size)
                    upfile.write(file_meta['body'])
                    upfile.close()
                    if chunk == chunks:
                        os.rename(_file_path, upload_path + _file_storage_name)
            # todo,需要修改为新的文件字段
            _entity = UserFileServ.create(_file_uuid, None, _file_name
                                          , '其它文件', file_meta['content_type'], _file_storage_name
                                          , None, _file_suffix, None, None, None
                                          , datetime.datetime.now()
                                          )
            finish = 1
            if chunk == chunks:
                finish = 2
                input_file_path = os.path.join(config.user_file_path + '/upload/', _file_storage_name)
                output_file_path = os.path.join(config.user_file_path + '/upload/', _file_uuid + '.pdf')
                convert_file_to_pdf(input_file_path, output_file_path)
                _pdfEntity = UserFileServ.create(_file_uuid, None, self.get_argument('fileName') + '.pdf'
                                                 , '其它文件', file_meta['content_type'], _file_uuid + '.pdf'
                                                 , None, '.pdf', None, None, None
                                                 , datetime.datetime.now()
                                                 )
            _rtn = {'success': True,
                    'msg': 'success！',
                    'finish': finish,
                    'status': '200',
                    'login': True,
                    'obj': _entity,
                    'fileurl': '/api/file/' + _file_storage_name
                    }
            self.write(_rtn)
            return
        except Exception as e:
            self.clear()
            _rtn = {'success': False,
                    'msg': '系统错误：' + e.__str__(),
                    'obj': None,
                    }
            self.write(_rtn)
            logging.error(e.__str__())
            logging.error(traceback.format_exc())
            return


# 上传文件uuid生成
class ApiGetUUid(BaseApiHandler):
    # @coroutine
    def post(self):
        _rtn = {'success': True,
                'msg': 'success！',
                'data': IDUtil.get_uuid(),
                'status': '200',
                }
        self.write(_rtn)


# 文档生成
class ApiFileGenerateHandler(BaseApiHandler):
    need_login = False  # 登录后才能调用

    def mypost(self):
        _gpuInfo = self.get_arg('gpuInfo')
        _local_ip = self.get_arg('local_ip')
        rtn_list = []
        var1 = 0
        var2 = 0
        user = self.current_user
        # Excel文件选中行数据
        _checkdata = json.loads(self.get_arg('checkdata'))
        for item in _checkdata:
            if 'generateStatus' in item:
                del item['generateStatus']
        for item in _checkdata:
            if 'generateword' in item:
                del item['generateword']
        for item in _checkdata:
            if 'LAY_INDEX' in item:
                del item['LAY_INDEX']
        for item in _checkdata:
            if 'LAY_NUM' in item:
                del item['LAY_NUM']
        columns = list({key for d in _checkdata for key in d})
        # Word上传后的文件名
        _file_storage = object_to_str(self.get_arg('file_storage'))
        # word模板文件位置
        _word_file = config.user_file_path + '/upload/' + _file_storage
        # Word模板文件后缀名
        _fileExt = get_file_suffix(_word_file)
        if _fileExt == '.doc':
            _rtn = {'success': False,
                    'msg': '请上传后缀名.docx的Word模板文件！',
                    'obj': None,
                    }
            self.write(_rtn)
            return
        # 文件存储路径
        # task_id = IDUtil.get_uuid()
        _savepath = config.user_file_path + '/output/'  # 存储路径
        if not os.path.exists(_savepath):
            os.makedirs(_savepath)
        try:
            for _one_checkdata in _checkdata:
                file_uuid = _one_checkdata['rowid']
                filenamerule = _one_checkdata['文件名']
                newfilename = parsenewFileName(filenamerule, _one_checkdata)
                if '/' in newfilename:
                    newfilefullpath = os.path.join(_savepath + file_uuid + '/', newfilename + '.docx')
                    # 应对{组织机构全称}/申请表需要生成子目录的情况
                    directory_path = os.path.dirname(newfilefullpath)
                    if not os.path.exists(directory_path):
                        os.makedirs(directory_path)
                    # 构建替换字典
                    replacements = {f'{{{col}}}': _one_checkdata[col] for col in columns}
                    create_docx_report(_word_file, newfilefullpath, replacements)
                    if os.path.exists(newfilefullpath):
                        # todo,需要修改为新的文件字段
                        _file_storage_name = file_uuid + '/' + newfilename + '.docx'
                        _entity = UserFileServ.create(file_uuid, None, newfilename + '.docx'
                                                      , '其它文件', None, _file_storage_name
                                                      , None, '.docx', None, None, None
                                                      , datetime.datetime.now()
                                                      )
                        input_file_path = os.path.join(config.user_file_path + '/output/', _file_storage_name)
                        output_file_path = os.path.join(config.user_file_path + '/upload/', file_uuid + '.pdf')
                        convert_file_to_pdf(input_file_path, output_file_path)
                        _pdfEntity = UserFileServ.create(file_uuid, None,
                                                         newfilename + '.pdf'
                                                         , '其它文件', 'application/octet-stream', file_uuid + '.pdf'
                                                         , None, '.pdf', None, None, None
                                                         , datetime.datetime.now()
                                                         )
                        _rtn = {'success': True,
                                'msg': '文件' + newfilename + '.docx生成成功！',
                                'rowid': file_uuid,
                                'obj': _entity,
                                'fileurl': '/api/doc_assistant/getfile/' + _file_storage_name
                                }
                        var1 += 1
                        rtn_list.append(_rtn)
                    else:
                        _rtn = {'success': False,
                                'msg': '文件' + newfilename + '.docx生成失败！',
                                'rowid': file_uuid,
                                'obj': None,
                                'fileurl': None
                                }
                        var2 += 1
                        rtn_list.append(_rtn)
                else:
                    newfilefullpath = os.path.join(_savepath, file_uuid + '.docx')
                    # 构建替换字典
                    replacements = {f'{{{col}}}': _one_checkdata.get(col, '') for col in columns}
                    create_docx_report(_word_file, newfilefullpath, replacements)
                    if os.path.exists(newfilefullpath):
                        # todo,需要修改为新的文件字段
                        _file_storage_name = file_uuid + '.docx'
                        _entity = UserFileServ.create(file_uuid, None, newfilename + '.docx'
                                                      , '其它文件', None, _file_storage_name
                                                      , None, '.docx', None, None, None
                                                      , datetime.datetime.now()
                                                      )
                        input_file_path = os.path.join(config.user_file_path + '/output/', _file_storage_name)
                        output_file_path = os.path.join(config.user_file_path + '/upload/', file_uuid + '.pdf')
                        convert_file_to_pdf(input_file_path, output_file_path)
                        _pdfEntity = UserFileServ.create(file_uuid, None,
                                                         newfilename + '.pdf'
                                                         , '其它文件', 'application/octet-stream', file_uuid + '.pdf'
                                                         , None, '.pdf', None, None, None
                                                         , datetime.datetime.now()
                                                         )
                        _rtn = {'success': True,
                                'msg': '文件' + newfilename + '.docx生成成功！',
                                'rowid': file_uuid,
                                'obj': _entity,
                                'login': True,
                                'fileurl': '/api/doc_assistant/getfile/' + _file_storage_name
                                }
                        var1 += 1
                        rtn_list.append(_rtn)
                    else:
                        _rtn = {'success': False,
                                'msg': '文件' + newfilename + '.docx生成失败！',
                                'rowid': file_uuid,
                                'login': True,
                                'obj': None,
                                'fileurl': None
                                }
                        var2 += 1
                        rtn_list.append(_rtn)
            self.write({
                'success': True,
                'code': 0,
                'msg': '累计:' + str(var1) + '个生成成功，' + str(var2) + '个生成失败！',
                'count': var1 + var2,
                'login': True,
                'data': rtn_list,
            })
            return
        except Exception as e:
            self.clear()
            _rtn = {'success': False,
                    'msg': '系统错误：' + e.__str__(),
                    'obj': None,
                    }
            self.write(_rtn)
            logging.error(e.__str__())
            logging.error(traceback.format_exc())
            return


def create_docx_report(_word_file, newfilefullpath, replacements):
    # 复制模板文件作为新文件
    shutil.copy(_word_file, newfilefullpath)
    # 调用函数进行文本替换
    replace_text_in_docx(newfilefullpath, replacements)


# 根据文件名规则生成新的文件名
def parsenewFileName(filenamerule, one_checkdata: dict):
    # 使用正则表达式提取花括号中的内容
    pattern = r'\{(.*?)\}'
    matches = re.findall(pattern, filenamerule)[0]
    replacestr = one_checkdata[matches]
    findstr = '{' + matches + '}'
    newfilename = filenamerule.replace(findstr, replacestr)
    return newfilename


def get_file_suffix(file_url):
    return os.path.splitext(file_url)[-1].lower()


def replace_text_in_docx(file_path, replacements):
    # 加载 .docx 文件
    doc = docx.Document(file_path)
    # 遍历每一段文本进行替换
    for paragraph in doc.paragraphs:
        for key, value in replacements.items():
            if key in paragraph.text:
                paragraph.text = paragraph.text.replace(key, str(value))
    # 保存更改后的文档
    doc.save(file_path)


def zip_directory(directory, zip_file_name):
    # 打开一个 Zip 文件，准备写入压缩内容
    with zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # 遍历整个目录树
        for root, _, files in os.walk(directory):
            for file in files:
                # 构造文件的完整路径
                file_path = os.path.join(root, file)
                # 将文件添加到 Zip 文件中，使用相对路径存储
                zipf.write(file_path, os.path.relpath(file_path, directory))


def zip_files(file_paths, zip_file_name, output_dir, name_mapping):
    # 打开一个 Zip 文件，准备写入压缩内容
    with zipfile.ZipFile(os.path.join(output_dir, zip_file_name), 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in file_paths:
            # 获取文件的目标名称
            new_name = name_mapping.get(file_path, os.path.basename(file_path))
            # 将文件添加到 Zip 文件中，使用目标名称作为存储路径
            zipf.write(file_path, new_name)


urls = [
    ('/api/doc_assistant/uploadfile', ApiUploadFileHandler),  # 批量文档助手文件上传
    ('/api/doc_assistant/getUUid', ApiGetUUid),  # 上传文件uuid生成
    ('/api/doc_assistant/filegenerate', ApiFileGenerateHandler),  # 文档生成
    ('/api/doc_assistant/getbatchfile', ApiGetbatchFileHandler),
    (r'/api/doc_assistant/file/(.*)', ApiGetoneFileHandler),
]
