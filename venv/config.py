# -*- coding: UTF-8 -*-
"""
  _author: Simon Qu
  _date: 20200406
  _version: 1.0.0
  _description: 用于配置环境变量或指定对应配置参数
"""
import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'xiang&&ting'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'mysql+pymysql://mysql:wuliao#24@192.168.118.129:3306/tingxiangblog'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMMIT_ON_TEARDOWN = True



