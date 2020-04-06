# -*- coding: UTF-8 -*-
"""
  _author: Simon Qu
  _date: 202000406
  _version: 1.0.0
  _description: 路由模块，用于网站页面跳转
"""

from app import app
from flask import render_template, url_for, redirect, flash
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Simon'}
    title = 'Home page'
    return render_template('index.html', title=title, user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('The user {} login to TingxiangBlog and remember {}'.format(form.username.data,form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html',title='Sign In', form=form)

