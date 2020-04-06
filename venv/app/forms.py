# -*- coding: UTF-8 -*-
"""
  _author: Simon Qu
  _date: 20200406
  _version: 1.0.0
  _description: 此模块用于创建表单，用于与前端交互数据
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')



