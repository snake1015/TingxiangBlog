# -*- coding: UTF-8 -*-
"""
  _author: Simon Qu
  _date: 20200101
  _version: 1.0.0
  _description: 初始化一个Flask 对象
"""

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import pymysql

app = Flask(__name__)
app.config.from_object(Config)  # 获取配置的环境变量
db = SQLAlchemy(app) # 创建一个数据库对象
migrate = Migrate(app, db) # 创建一个数据迁移对象


from app import routes, models



