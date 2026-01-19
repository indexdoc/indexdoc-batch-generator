
urls =  []

#sysdomain
from domain.sysdomain.handler import SysUserHandler
urls += SysUserHandler.urls
from domain.sysdomain.handler import SysDictHandler
urls += SysDictHandler.urls
from domain.sysdomain.handler import SysRoleHandler
urls += SysRoleHandler.urls
from domain.sysdomain.handler import SysUserRoleHandler
urls += SysUserRoleHandler.urls
from domain.sysdomain.handler import SysDbLogHandler
urls += SysDbLogHandler.urls
from domain.sysdomain.handler import SysOrgHandler
urls += SysOrgHandler.urls
from domain.sysdomain.handler import SysUserOrgHandler
urls += SysUserOrgHandler.urls
from domain.sysdomain.handler import SysMenuAuthHandler
urls += SysMenuAuthHandler.urls
from domain.sysdomain.handler import SysMenuHandler
urls += SysMenuHandler.urls
from domain.sysdomain.handler import SysUserAttrHandler
urls += SysUserAttrHandler.urls
from domain.sysdomain.handler import SysApiAuthHandler
urls += SysApiAuthHandler.urls
from domain.sysdomain.handler import UserFileHandler
urls += UserFileHandler.urls
from domain.sysdomain.handler import OrgDutyHandler
urls += OrgDutyHandler.urls
from domain.sysdomain.handler import SysPageAuthHandler
urls += SysPageAuthHandler.urls
from domain.sysdomain.handler import RegisterHandler
urls += RegisterHandler.urls

from domain.sysdomain.view import ViewUserMenuHandler
urls += ViewUserMenuHandler.urls
from domain.sysdomain.view import ViewUserApiHandler
urls += ViewUserApiHandler.urls
from domain.sysdomain.view import ViewUserPageHandler
urls += ViewUserPageHandler.urls


#doc_assistant
from domain.doc_assistant.handler import WordTemplateHandler
urls += WordTemplateHandler.urls
from domain.doc_assistant.handler import ExcelTemplateHandler
urls += ExcelTemplateHandler.urls
from domain.doc_assistant.handler import GenerateFilesHandler
urls += GenerateFilesHandler.urls
from domain.doc_assistant import DocAssistantHandler
urls += DocAssistantHandler.urls

import SysHandler
urls += SysHandler.urls



