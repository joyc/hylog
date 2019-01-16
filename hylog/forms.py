from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, ValidationError, HiddenField
from wtforms.validators import DataRequired, Length, Email, Optional, URL
from flask_ckeditor import CKEditorField

from hylog.models import Category


class LoginForm(FlaskForm):
    """登陆表单"""
    username = StringField('姓名', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('密码', validators=[DataRequired(), Length(8, 128)])
    remember = BooleanField('保存')
    submit = SubmitField('登陆')


class SettingForm(FlaskForm):
    """设定表单"""
    name = StringField('姓名', validators=[DataRequired(), Length(1, 70)])
    blog_title = StringField('博客标题', validators=[DataRequired(), Length(1, 60)])
    blog_sub_title = StringField('博客副标题', validators=[DataRequired(), Length(1, 100)])
    about = CKEditorField('About Page', validators=[DataRequired()])
    submit= SubmitField()


class PostForm(FlaskForm):
    """文章表单"""
    title = StringField('标题', validators=[DataRequired(), Length(1, 60)])
    category = SelectField('目录', coerce=int, default=1)
    body = CKEditorField('内容', validators=[DataRequired()])
    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name)
                                 for category in Category.query.order_by(category.name).all()]


class CategoryForm(FlaskForm):
    """分类目录表单"""
    name = StringField('分类名', validators=[DataRequired(), Length(1, 30)])
    submit = SubmitField()

    def validate_name(self, field):
        if Category.query.filter_by(name=field.data).first():
            raise ValidationError('该分类名已被使用，请换一个试试。')


class CommentForm(FlaskForm):
    """评论表单"""
    author = StringField('姓名', validators=[DataRequired(), Length(1, 30)])
    email = StringField('邮件', validators=[DataRequired(), Email(), Length(1, 254)])
    site = StringField('网站', validators=[Optional(), URL(), Length(0, 255)])
    body = TextAreaField('内容', validators=[DataRequired()])
    submit = SubmitField()


class AdminCommentForm(CommentForm):
    """管理员用留言表单"""
    author = HiddenField()
    email = HiddenField()
    site = HiddenField()


class LinkForm(FlaskForm):
    """链接表单"""
    name = StringField('名称', validators=[DataRequired(), Length(1, 30)])
    url = StringField('URL', validators=[DataRequired(), URL(), Length(1, 255)])
    submit = SubmitField()
