from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length
from flask_ckeditor import CKEditorField

from hylog.models import Category


class LoginForm(FlaskForm):
    """登陆表单"""
    username = StringField('姓名', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('密码', validators=[DataRequired(), Length(8, 128)])
    remember = BooleanField('保存')
    submit = SubmitField('登陆')


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
