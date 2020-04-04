# -*- coding: UTF-8 -*-
"""
  _author: Simon Qu
  _date: 20200101
  _version: 1.0.0
  _description: 
"""

from app import app

@app.route('/')
def index():
    return('Welcome to TingxiangBlog!')

