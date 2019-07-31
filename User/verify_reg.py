import re

from flask import session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError
from User.models import User


class RegisterForm(FlaskForm):
    username = StringField('用户名:', validators=[DataRequired('请输入用户名:'), Length(min=3, max=12, message='用户名长度在3~12位之间')],
                           render_kw={'placeholder': '请输入用户名'})
    passsword = PasswordField('密码:', validators=[DataRequired('请输入密码:'), Length(min=3, max=12, message='密码长度在3~12位之间')],
                              render_kw={'placeholder': '请输入密码'})
    confirm_password = PasswordField('确认密码:', validators=[DataRequired('确认密码'), EqualTo('passsword', '两次密码输入不一致')],
                                     render_kw={'placeholder': '请确认密码'})
    email = StringField('邮箱:', validators=[DataRequired('请输入邮箱地址：'), Email(message='请输入正确的邮箱')],
                        render_kw={'placeholder': '请输入邮箱'})
    submit = SubmitField('注册')

    # 自定义验证规则：validate_验证字段(self,字段值对象)
    def validate_password(self, field):
        if re.match(r'\d+$', field.data):
            raise ValidationError('密码不能是纯数字')

    # 验证用户名是否重复
    def validate_username(self, field):
        res = User.query.filter(User.username == field.data).first()
        if res:
            raise ValidationError('用户名已存在！')

class UeditorForm(FlaskForm):
    pass