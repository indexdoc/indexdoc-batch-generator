import copy
import datetime
import jwt
from captcha.image import ImageCaptcha
from random import randint
from io import BytesIO
import base64

from domain.sysdomain.entity.SysUserEntity import SysUserEntity
# from config import token_iss_user,token_secret_key
import config
from domain.sysdomain.serv import SysUserRoleServ

# payload = {
#     'iss': token_iss_user,  # 签名
#     'user': {  # 内容，一般存放该用户id和开始时间
#         'sys_user_id': user.sys_user_id,
#         'user_namae': user.user_name,
#         'exp_time': datetime.datetime.now() + datetime.timedelta(days=7)
#        },
#  }
from utils import IDUtil


def token_new(user: SysUserEntity):
    _payload = {
        'iss': config.token_iss_user,  # 签名
        'user': {  # 内容，一般存放该用户id和开始时间
            'sys_user_id': user.sys_user_id,
            'user_name': user.user_name,
            'last_login_time': datetime.datetime.now(),
            'last_active_time': datetime.datetime.now(),
            'last_login_info': user.last_login_info,
        },
    }
    return token_encode(_payload)


token_algorithm = 'EdDSA'
private_key_pem = b'-----BEGIN EC PRIVATE KEY-----\nMHcCAQEEINyIzr6nX/qCmHM1fZE/tVSN9A8i3IFCpnCl4iZCGxdcoAoGCCqGSM49\nAwEHoUQDQgAE3e08myx4+uLlBPKgcPYXNCbzrhn7N3WUNDp7wdVfmxzUp3YV5p3P\nSioqII0TEo82oWYsW+vgPGUqiXimp9/qsQ==\n-----END EC PRIVATE KEY-----\n'
public_key_pem = b'-----BEGIN PUBLIC KEY-----\nMFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE3e08myx4+uLlBPKgcPYXNCbzrhn7\nN3WUNDp7wdVfmxzUp3YV5p3PSioqII0TEo82oWYsW+vgPGUqiXimp9/qsQ==\n-----END PUBLIC KEY-----\n'


def token_encode(payload: dict):
    _payload = copy.deepcopy(payload)
    _last_login_time: datetime = _payload['user']['last_login_time']
    _last_login_time_int = int(_last_login_time.timestamp())
    _payload['user']['last_login_time'] = _last_login_time_int
    _last_active_time: datetime = _payload['user']['last_active_time']
    _last_active_time_int = int(_last_active_time.timestamp())
    _payload['user']['last_login_time'] = _last_login_time_int
    _payload['user']['last_active_time'] = _last_active_time_int
    # token = jwt.encode(_payload, config.token_secret_key, algorithm='HS256')
    # token = jwt.encode({'token':token}, private_key_pem, algorithm="ES256K")

    token = jwt.encode(_payload, private_key_pem, algorithm="ES256K")

    return token


def token_decode(token: str):
    # _payload = jwt.decode(token, public_key_pem, algorithms=["ES256K"])
    # _payload = jwt.decode(_payload['token'], config.token_secret_key, issuer=config.token_iss_user, algorithms=['HS256'])
    _payload = jwt.decode(token, public_key_pem, algorithms=["ES256K"])
    _payload['user']['last_login_time'] = datetime.datetime.fromtimestamp(_payload['user']['last_login_time'])
    _payload['user']['last_active_time'] = datetime.datetime.fromtimestamp(_payload['user']['last_active_time'])
    return _payload


# IMG_CHAR_OPT = ['2', '3', '4', '5', '6', '7', '8', '9',
#         'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'm', 'n', 'p', 'q', 'r', 's', 't', 'u', 'w', 'x', 'y', 'z',
#         'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T',  'W', 'X', 'Y', 'Z']

IMG_CHAR_OPT = ['2', '3', '4', '5', '6', '7', '8', '9',
                'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'W', 'X',
                'Y', 'Z']

__img_dict = {}

IMG_MAX_VALID_SECONDS = 60 * 10  # 默认3分钟


def gen_imgcode():
    img_chars = ''
    for i in range(4):
        img_chars += IMG_CHAR_OPT[randint(0, len(IMG_CHAR_OPT) - 1)]
    image = ImageCaptcha().generate_image(img_chars)
    buffered = BytesIO()
    image.save(buffered, format='JPEG')
    img_base64 = str(base64.b64encode(buffered.getvalue()), 'utf-8')
    img_id = IDUtil.get_long()
    img_datetime = datetime.datetime.now()
    __img_dict[img_id] = (img_id, img_datetime, img_chars)
    # print(img_chars)
    return img_id, img_base64


def delete_outdate_imgs():
    _outdate_imgs = []
    for tup in __img_dict.values():
        _img_id = tup[0]
        _img_datetime = tup[1]
        _img_chars = tup[2]
        if datetime.datetime.now() - _img_datetime > datetime.timedelta(seconds=IMG_MAX_VALID_SECONDS):
            _outdate_imgs.append(_img_id)
    for _img_id in _outdate_imgs:
        __img_dict.pop(_img_id)


def check_imgcode(img_id: int, img_chars: str):
    delete_outdate_imgs()
    _tup = __img_dict.get(img_id)
    if _tup is None:
        return False, "验证码过期！"
    _img_datetime = _tup[1]
    _img_chars = _tup[2]
    if datetime.datetime.now() - _img_datetime > datetime.timedelta(seconds=IMG_MAX_VALID_SECONDS):
        return False, "验证码过期！"
    if _img_chars.lower() != img_chars.lower():
        return False, "验证码错误！"
    return True, "验证成功！"


import hashlib
import hmac


def encode_pwd(pwd: str, user_id: int):
    pwdcode = hashlib.blake2b(pwd.encode('utf-8'), digest_size=8, key=b"", salt=b"",
                              person=str(user_id).encode('utf-8')).hexdigest()
    return pwdcode


def check_pwd(pwd: str, user_id: int, pwdcode: str):
    pwdcode1 = hashlib.blake2b(pwd.encode('utf-8'), digest_size=8, key=b"", salt=b"",
                               person=str(user_id).encode('utf-8')).hexdigest()
    return hmac.compare_digest(pwdcode1, pwdcode)
