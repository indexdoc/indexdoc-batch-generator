import datetime
import json
import random
import ssl
import urllib

import cachetools as cachetools

import SysCache
import SysServ
from BaseHandler import BaseApiHandler
import logging
import traceback

from domain.sysdomain.daock import SysUserDaoCK, SysRoleDaoCK
from domain.sysdomain.entity.SysUserEntity import SysUserEntity
from domain.sysdomain.serv import UserUseLogServ, SysUserServ, SysRoleServ, SysUserRoleServ
from utils import CodeUtil


class ApiRefreshAuth(BaseApiHandler):
    need_login = False

    def myget(self):
        try:
            SysCache.refreshAuth()
            self.clear()
            _rtn = {'success': True,
                    'msg': '更新菜单对应的页面及API权限成功！',
                    'obj': None,
                    }
            self.write(_rtn)
            return
        except Exception as e:
            _rtn = {'success': False,
                    'msg': '系统错误：' + e.__str__(),
                    'obj': None,
                    }
            self.write(_rtn)
            logging.error(e.__str__())
            logging.error(traceback.format_exc())
            return


class ApiDefaultToken(BaseApiHandler):
    need_login = False

    def myget(self):
        try:
            if self.current_user is not None and self.current_user['user_name'] != 'free':
                return
            # user_name = 'e-admin'
            user_name = 'free'
            # pwd = '74f0ee0fd1e364cb04b51d3a5d018214518fa594'
            pwd = '74f0ee0fd1e364cb04b51d3a5d018214518fa594'
            # UserUseLogServ.create(self.current_user['sys_user_id'],self.request.headers.get('X-Real-IP'),self.request.path,datetime.datetime.now())
            tup = SysServ.check_user_pwd(user_name, pwd)
            if tup[0] is False:
                self.clear()
                return self.write({
                    'success': False,
                    'msg': tup[1]
                })
            user: SysUserEntity = tup[1]
            user.last_login_info = json.dumps({
                'remote_ip': self.request.remote_ip,
                'X-Real-IP': self.request.headers.get("X-Real-IP"),
                'X-Forwarded-For': self.request.headers.get("X-Forwarded-For"),
                'user-agent': self.request.headers.get("User-Agent"),
            })
            token = CodeUtil.token_new(user)
            self.current_user = {  # 内容，一般存放该用户id和开始时间
                'sys_user_id': user.sys_user_id,
                'user_name': user.user_name,
                'last_login_time': datetime.datetime.now(),
                'last_active_time': datetime.datetime.now(),
            }
            self.user = self.current_user
            self.clear()
            self.set_secure_cookie('token', token)
            # 限制用户只能在一个地方登录
            # SysCache.user_token[user.sys_user_id]= [token]
            # 用户可以在多个地方登陆
            if SysCache.user_token.get(user.sys_user_id) is None:
                SysCache.user_token[user.sys_user_id] = [token]
            else:
                SysCache.user_token[user.sys_user_id].append(token)
            self.write({
                'success': True,
                'msg': '',
            })
            # self.finish()
            SysUserDaoCK.update(user)
            return
        except Exception as e:
            _rtn = {'success': False,
                    'msg': '系统错误：' + e.__str__(),
                    'obj': None,
                    }
            self.write(_rtn)
            logging.error(e.__str__())
            logging.error(traceback.format_exc())
            return


cache = cachetools.TTLCache(maxsize=100, ttl=300)


class ApiSendCode(BaseApiHandler):
    need_login = False

    def myget(self):
        _phone_no = self.get_arg('phone_no')
        # 生成6位随机验证码
        random_number = random.randint(100000, 999999)

        # 设置阿里云API基本信息
        host = 'https://zwp.market.alicloudapi.com'
        path = '/sms/sendv2'
        method = 'GET'
        appcode = '04b01aa4cc244257a37b374c1cc00eac'  # 注意：敏感信息建议使用环境变量

        # 短信内容和手机号
        content = f'【AiTuple】您的验证码是{random_number}。如非本人操作，请忽略本短信。'

        # 对内容和手机号进行 URL 编码，确保 UTF-8 编码
        querys = f'mobile={urllib.parse.quote(_phone_no)}&content={urllib.parse.quote(content, encoding="utf-8")}'

        # 构建请求URL
        url = f'{host}{path}?{querys}'

        try:
            # 构建请求对象
            request = urllib.request.Request(url)
            request.add_header('Authorization', 'APPCODE ' + appcode)

            # 创建SSL上下文，忽略证书验证
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE

            # 发送请求
            response = urllib.request.urlopen(request, context=ctx)
            content = response.read().decode('utf-8')

            # 输出响应内容
            print("Response: ", content)
            self.write({
                'success': True,
                'msg': '验证码发送成功，请注意查收',
            })
            cache[_phone_no] = random_number
            return

        except Exception as e:
            # 处理可能的异常
            print(f"Error occurred: {e}")
            self.write({
                'success': False,
                'msg': json.loads(content)['reason'],
            })
            return None


class ApiLoginPhone(BaseApiHandler):
    need_login = False

    def mypost(self, *args, **kwargs):
        argdict = self.get_dictarg()
        _phone_no = argdict.get('phone_no')
        _code = argdict.get('code')
        cached_code = cache.get(_phone_no)
        if cached_code is not None and cached_code == int(_code):
        # if int(_code) == 123:
            _sys_user_eneity = SysUserDaoCK.select_by_UserName(_phone_no)
            if _sys_user_eneity is None:
                _sys_user = SysUserServ.create(_phone_no, None, None, None, datetime.datetime.now(), None, None, None)
                _sysRole = SysRoleDaoCK.select_by_RoleName('免费使用用户')
                SysUserRoleServ.create(_sys_user.sys_user_id, _sysRole[0].sys_role_id)
                SysCache.refreshAuth()

            tup = SysServ.check_user(_phone_no)
            if tup[0] is False:
                self.clear()
                return self.write({
                    'success': False,
                    'msg': tup[1]
                })
            user: SysUserEntity = tup[1]
            user.last_login_info = json.dumps({
                'remote_ip': self.request.remote_ip,
                'X-Real-IP': self.request.headers.get("X-Real-IP"),
                'X-Forwarded-For': self.request.headers.get("X-Forwarded-For"),
                'user-agent': self.request.headers.get("User-Agent"),
            })
            token = CodeUtil.token_new(user)
            self.current_user = {  # 内容，一般存放该用户id和开始时间
                'sys_user_id': user.sys_user_id,
                'user_name': user.user_name,
                'last_login_time': datetime.datetime.now(),
                'last_active_time': datetime.datetime.now(),
            }
            self.user = self.current_user
            self.clear()
            self.set_secure_cookie('token', token)
            # 限制用户只能在一个地方登录
            # SysCache.user_token[user.sys_user_id]= [token]
            # 用户可以在多个地方登陆
            if SysCache.user_token.get(user.sys_user_id) is None:
                SysCache.user_token[user.sys_user_id] = [token]
            else:
                SysCache.user_token[user.sys_user_id].append(token)
            # self.finish()
            SysUserDaoCK.update(user)
            self.write({
                'success': True,
                'msg': '登录成功',
                'obj': {'token': token,
                        'sys_user_id': user.sys_user_id,
                        'user_name': user.user_name,
                        }
            })
            return
        else:
            self.write({
                'success': False,
                'msg': '验证码过期',
            })
        return


urls = [
    ('/api/refreshAuth', ApiRefreshAuth),
    ('/api/default', ApiDefaultToken),
    ('/api/sendCode', ApiSendCode),
    ('/api/loginPhone', ApiLoginPhone),
]
