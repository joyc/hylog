from flask import Blueprint

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login')
def login():
    return '登陆页面'


@auth_bp.route('/logout')
def logout():
    return '登出页面'
