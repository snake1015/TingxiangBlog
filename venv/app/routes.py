# -*- coding: UTF-8 -*-
"""
  _author: Simon Qu
  _date: 20200101
  _version: 1.0.0
  _description: 
"""

from app import app
from flask import render_template, url_for

@app.route('/')
def index():
    user = {'username': 'Simon'}
    return render_template('index.html', user=user)

@app.route('/login',methods=['GET', 'POST'])
def login():
    return render_template('login.html')

