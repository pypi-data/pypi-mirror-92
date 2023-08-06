#改模块配置了django的环境，必须比models先引用
from django_to_sqlserver_description import update_MS_Description

from . import models
#真实执行
update_MS_Description(models)