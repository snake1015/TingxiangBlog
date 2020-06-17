# -*- coding: UTF-8 -*-
"""
  _author: Simon Qu
  _date: 20200406
  _version: 1.0.0
  _description: 此模块用于创建表单，用于与前端交互数据
"""

from flask_wtf import FlaskForm
from flask_babel import lazy_gettext as _l
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import User

class LoginForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if  user is not None:
            raise ValidationError('The user has exist,pls use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('The email has been use, pls use a different email.')

class EditProfileForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    about_me = TextAreaField('About Me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def _init_(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username')

class PostForm(FlaskForm):
    post = TextAreaField('说点什么',validators=[DataRequired(), Length(min=1, max=140)])
    submit = SubmitField()


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('注册邮箱', validators=[DataRequired(),Email()])
    submit = SubmitField('重置密码')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('输入密码:', validators=[DataRequired()])
    password2 = PasswordField('再次输入密码:', validators=[DataRequired(), EqualTo(password)])
    submit = SubmitField('提交')




