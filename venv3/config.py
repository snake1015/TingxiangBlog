# -*- coding: UTF-8 -*-
"""
  _author: Simon Qu
  _date: 20200406
  _version: 1.0.0
  _description: 用于配置环境变量或指定对应配置参数
"""
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'xiang&&ting'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'app.db')
                              # 'mysql+pymysql://mysql:wuliao#24@192.168.118.131:3306/tingxiangblog'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMMIT_ON_TEARDOWN = True
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'localhost'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 8025)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USER = os.environ.get('MAIL_USER')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['qjxking@126.com']
    POSTS_PER_PAGE = 2
    LANGUAGES = ['zh', 'en']




