import os
import click
from flask import Flask, render_template

from hylog.models import Admin, Category
from hylog.blueprints.admin import admin_bp
from hylog.blueprints.auth import auth_bp
from hylog.blueprints.blog import blog_bp
from hylog.settings import config
from hylog.extensions import bootstrap, db, moment, ckeditor, mail

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('hylog')
    app.config.from_object(config[config_name])

    register_logging(app)           # 注册日志处理器
    register_extensions(app)        # 注册扩展（扩展初始化）
    register_blueprints(app)        # 注册蓝本
    register_commands(app)          # 注册自定义shell命令
    register_errors(app)            # 注册错误处理函数
    register_shell_context(app)     # 注册shell上下文处理函数
    register_template_context(app)  # 注册模板上下文处理函数
    return app


def register_logging(app):
    pass


def register_extensions(app):
    """扩展的实例化放在extensions.py中"""
    bootstrap.init_app(app)
    db.init_app(app)
    moment.init_app(app)
    ckeditor.init_app(app)
    mail.init_app(app)


def register_blueprints(app):
    app.register_blueprint(blog_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db)


def register_template_context(app):
    @app.context_processor
    def make_template_context():
        admin = Admin.query.first()
        categories = Category.query.order_by(Category.name).all()
        return dict(admin=admin, categories=categories)


def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500


def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='先删除后创建')
    def initdb(drop):
        """初始化数据库"""
        if drop:
            click.confirm('此操作会删除现有数据库，是否继续?', abort=True)
            db.drop_all()
            click.echo('删除表.')
        db.create_all()
        click.echo('数据库初始化成功')

    @app.cli.command()
    @click.option('--category', default=10, help='分类目录个数，默认为10个.')
    @click.option('--post', default=50, help='日志篇数，默认为50篇.')
    @click.option('--comment', default=300, help='留言评论数，默认为300条.')
    def forge(category, post, comment):
        """创建测试数据"""
        from hylog.fakes import fake_admin, fake_categories, fake_posts, fake_comments, fake_links

        db.drop_all()
        db.create_all()

        click.echo('创建管理员...')
        fake_admin()

        click.echo(f'创建{category}个分类目录...')
        fake_categories(category)

        click.echo(f'创建{post}篇日志...')
        fake_posts(post)

        click.echo(f'创建{comment}条留言...')
        fake_comments(comment)

        click.echo('生成链接...')
        fake_links()

        click.echo('测试数据生成完成.')
