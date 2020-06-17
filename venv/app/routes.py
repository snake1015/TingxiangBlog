# -*- coding: UTF-8 -*-
"""
  _author: Simon Qu
  _date: 202000406
  _version: 1.0.0
  _description: 路由模块，用于网站页面跳转
"""

from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post
from app import app, db
from flask import render_template, url_for, redirect, flash, request
from werkzeug.urls import url_parse
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from app.forms import PostForm, ResetPasswordRequestForm, ResetPasswordForm
from app.email import send_password_reset_email
import json
from datetime import datetime

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

# 主页路由
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live')
        return redirect(url_for('index'))
    page = request.args.get('page', 1, type=int)
    pagination = current_user.followed_posts().paginate(page, app.config['POSTS_PER_PAGE'], False)
    posts = pagination.items
    next_url = url_for('index', page=pagination.next_num) if pagination.has_next else None
    prev_url = url_for('index', page=pagination.prev_num) if pagination.has_prev else None
    return render_template('index.html', title='Home page', form=form, posts=posts, pagination=pagination)

# 用户登录路由
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: # 判断当前用户是否已登录，已登录则返回主页面
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit(): # 如果点击了登录按钮则进行登录验证
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):  # 如果登录失败，则提示错误信息，重新登录
            flash('invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data) # 登录成功，并记录当前登录用户
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc !='':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html',title='Sign In', form=form)

# 用户注销路由
@app.route('/logout', methods=['GET','POST'])
def logout():
    logout_user()
    return redirect(url_for('index'))

# 用户注册路由
@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register Page', form=form)

# 访问个人主页路由
@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    pagination = user.posts.order_by(Post.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
    posts = pagination.items
    next_url = url_for('user', username=user.username, page=pagination.next_num) if pagination.has_next else None
    prev_url = url_for('user', username=user.username, page=pagination.prev_num) if pagination.has_prev else None
    return render_template('/user.html', user=user, posts=posts, pagination=pagination)

# 修改个人信息
@app.route('/edit_profile',methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('You profile has updated!!')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html',title='Edit Profile', form=form)

# 关注用户
@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('user {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('you cannot follow yourserlf')
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are follwing {}!'.format(username))
    return redirect(url_for('user', username=username))

# 取消关注
@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(username))
    return redirect(url_for('user', username=username))

# 发现页面
@app.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
    posts = pagination.items
    next_url = url_for('explore', page=pagination.next_num) if pagination.has_next else None
    prev_url = url_for('explore', page=pagination.prev_num) if pagination.has_prev else None
    return render_template('index.html', title='Explore Page', posts=posts, pagination=pagination)

# 密码重置路由
@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('请前往您的邮箱检查并打开链接进行密码重置')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html', title='reset password', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('密码重置成功')
        return redirect(url_for('login'))
    return render_template('reset_password.html', title = 'Reset Password', form=form)
