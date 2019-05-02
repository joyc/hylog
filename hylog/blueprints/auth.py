# -*- coding: utf-8 -*-
"""
验证蓝图
"""
from flask import render_template, flash, redirect, url_for, Blueprint
from flask_login import login_user, logout_user, login_required, current_user

from hylog.forms import LoginForm
from hylog.models import Admin
from hylog.utils import redirect_back

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('blog.index'))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        admin = Admin.query.first()
        if admin:
            # 验证用户名及密码
            if username == admin.username and admin.validate_password(password):
                login_user(admin, remember)  # 登入用户
                flash(f'欢迎回来，{admin.username}', 'info')
                return redirect_back()  # 返回前一个页面
            flash('用户名或密码错误。', 'warning')
        else:
            flash('无此账户。', 'warning')
    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required    # 用于视图保护
def logout():
    logout_user()
    flash('退出成功。', 'info')
    return redirect_back()
