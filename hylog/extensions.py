# -*- coding: utf-8 -*-
"""
存储扩展实例化
"""
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_ckeditor import CKEditor
from flask_moment import Moment
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from flask_migrate import Migrate


bootstrap = Bootstrap()
db = SQLAlchemy()
moment = Moment()
ckeditor = CKEditor()
mail = Mail()
login_manager = LoginManager()
csrf = CSRFProtect()
migrate = Migrate()

# 获取当前用户的代理函数用的用户加载函数
@login_manager.user_loader
def load_user(user_id):
    from hylog.models import Admin
    user = Admin.query.get(int(user_id))
    return user


login_manager.login_view = 'auth.login'
login_manager.login_message = u'请先登陆！'  # 更改默认提示语句
login_manager.login_message_category = 'warning'