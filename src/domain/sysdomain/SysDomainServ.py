import os
import re

import config
from domain.sysdomain.entity.SysMenuEntity import SysMenuEntity
from domain.sysdomain.entity.SysMenuAuthEntity import SysMenuAuthEntity
from domain.sysdomain.serv import SysMenuAuthServ, SysPageAuthServ ,SysApiAuthServ,SysMenuServ
from domain.sysdomain.daock import SysMenuAuthDaoCK,SysPageAuthDaoCK,SysApiAuthDaoCK
from domain.sysdomain.view import ViewUserApiDaoCK,ViewUserPageDaoCK

def getAllApiAuth():
    _dicts = ViewUserApiDaoCK.select_all()
    auth_dict = dict()
    for api_dict in _dicts:
        auth_dict[( api_dict['api_url'],api_dict['sys_user_id'])] = api_dict['auth_flag']
    return auth_dict

def getAllPageAuth():
    _dicts = ViewUserPageDaoCK.select_all()
    auth_dict = dict()
    for page_dict in _dicts:
        auth_dict[(page_dict['page_path'],page_dict['sys_user_id'])] = page_dict['auth_flag']
    return auth_dict

def refreshAllMenuSubAuth():
    #删除sys_page_auth和sys_api_auth中所有gen_type为“系统后台自动更新”的数据
    for pageauth in SysPageAuthServ.get_all():
        if pageauth.update_type == '系统后台自动更新':
            SysPageAuthServ.delete(pageauth.sys_page_auth_id)
    for apiauth in SysApiAuthServ.get_all():
        if apiauth.update_type == '系统后台自动更新':
            SysApiAuthServ.delete(apiauth.sys_api_auth_id)
    #遍历SysMenuAuth，对每个菜单对应的page及api重新赋权
    for menuauth in SysMenuAuthServ.get_all():
        refreshMenuSubAuth(menuauth)

def refreshMenuSubAuth(menuauth:SysMenuAuthEntity):
    #得到当前菜单对应的页面
    menu = SysMenuServ.get_entity_by_id(menuauth.sys_menu_id)
    page_path = menu.menu_url
    if page_path is not None:
        _updatePageAuth(page_path, menuauth,menu)

def _updatePageAuth(page_path:str, menuauth:SysMenuAuthEntity,menu:SysMenuEntity):
    #判断当前页面是否在Sys_page_auth表中进行了定义且update_type=='手工更新'，则不进行更新
    pageauths = SysPageAuthDaoCK.select_by_SysMenuAuthId(menuauth.sys_menu_auth_id)
    need_update = True
    if pageauths is not None:
        for pageauth in pageauths:
            if pageauth.page_path == page_path:
                need_update = False
    if need_update:
        _page_path_base = page_path.split('?')[0]
        SysPageAuthServ.create(menu.menu_name,_page_path_base,
                               menuauth.sys_user_id,menuauth.sys_role_id,menuauth.sys_org_id,menuauth.org_duty_id,
                               '允许',menuauth.sys_menu_auth_id,'系统后台自动更新',None
                               )
    #获取子页面及API并进行更新
    if page_path is None or page_path == '':
        return
    subpages = _get_subpage(page_path)
    for _page_path in subpages:
        _page_path_base = _page_path.split('?')[0]
        _updatePageAuth(_page_path_base, menuauth,menu)
    subapis = _get_subapi(page_path)
    for _api_path in subapis:
        _api_path_bash = _api_path.split('?')[0]
        _updateApiAuth(_api_path_bash,menuauth,menu)

def _updateApiAuth(api_path,menuauth,menu):
    #判断当前页面是否在Sys_page_auth表中进行了定义且update_type=='手工更新'，则不进行更新
    apiauths = SysApiAuthDaoCK.select_by_SysMenuAuthId(menuauth.sys_menu_auth_id)
    need_update = True
    if apiauths is not None:
        for apiauth in apiauths:
            if apiauth.api_url == api_path:
                need_update = False
    if need_update:
        SysApiAuthServ.create(menu.menu_name,api_path,
                               menuauth.sys_user_id,menuauth.sys_role_id,menuauth.sys_org_id,menuauth.org_duty_id,
                               '允许',menuauth.sys_menu_auth_id,'系统后台自动更新',None
                               )


def _get_subpage(pagepath:str):
    pattern_html = r"content\s*:\s*['\"]([^'\"]+\.html(?:\?[^'\"\n]*)?)['\"]"
    file_path = config.html_path + pagepath.split('?')[0]
    with open(file_path,'r') as fp:
        file_content = fp.read()
    html_files = re.findall(pattern_html, file_content)
    dir_path = os.path.dirname(pagepath)
    _paths = list()
    for _path in html_files:
        _path = os.path.join(dir_path,_path)
        _path = os.path.normpath(_path)
        _paths.append(_path)
    return _paths

def _get_subapi(pagepath:str):
    pattern_api = r'["\'](/api/.*?)["\']'
    file_path = config.html_path  + pagepath.split('?')[0]
    with open(file_path,'r') as fp:
        file_content = fp.read()
    api_paths = re.findall(pattern_api, file_content)
    return api_paths

#_get_subapi('/pc/syspage/sysdomain/SysUser/vslist.html')