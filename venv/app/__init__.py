# -*- coding: UTF-8 -*-
"""
  _author: Simon Qu
  _date: 20200101
  _version: 1.0.0
  _description: 初始化一个Flask 对象
"""

from flask import Flask
from flask_login import LoginManager
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import pymysql
import os
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler

app = Flask(__name__)
app.config.from_object(Config)  # 获取配置的环境变量
db = SQLAlchemy(app) # 创建一个数据库对象
migrate = Migrate(app, db) # 创建一个数据迁移对象
login = LoginManager(app) # 初始化login对象
login.login_view = 'login' # 确认受保护的页面需要先登录才可以访问并转到login页面


from app import routes, models, errors

# 配置日志信息记录及邮件发送
if not app.debug:
    if app.config['MAIL_SERVER']:
        #将错误信息通过邮件
        auth = None
        if app.config['MAIL_USER'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USER'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'],app.config['MAIL_PORT']),
            fromaddr='no-reply@'+app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMIN'],
            subject='tingxiangblog error',
            credentials=auth,
            secure=secure)
        mail_handler.setLevel(logging.error)
        app.logger.addHandler(mail_handler)
        # 将日志记录在本地日志文件中
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/tingxiangblog.log', maxBytes=102400, backupCount=10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('tingxiangblog startup')




