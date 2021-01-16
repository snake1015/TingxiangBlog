# -*- coding: UTF-8 -*-
"""
  _author: Simon Qu
  _date: 20200101
  _version: 1.0.0
  _description:  错误处理模块
"""

from flask import render_template
from app import app, db

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internel_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


