# -*- coding: UTF-8 -*-
"""
  _author: Simon Qu
  _date: 20200101
  _version: 1.0.0
  _description: 配置数据库表对象
"""

from hashlib import md5
from datetime import datetime
from app import db, login, app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from time import time
import jwt

# 定义粉丝表，多对多关系
followers = db.Table('followers',
                     db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('followed_id', db.Integer, db.ForeignKey('user.id')))

class User(UserMixin, db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime,default=datetime.utcnow())
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    followed = db.relationship('User', secondary=followers,
                               primaryjoin=(followers.c.follower_id == id),
                               secondaryjoin=(followers.c.followed_id == id),
                               backref=db.backref('followers', lazy='dynamic'),
                               lazy='dynamic')
    # 设置密码加密
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # 验证用户密码
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # 生成用户头像
    def avator(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravator.com/avator/{}?d=identicon&s={}'.format(digest, size)

    # 关注用户
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    # 取消关注
    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    # 是否关注
    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    # 关注用户的评论
    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
            followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id= self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

    # 重置密码token生成
    def get_reset_password_token(self, expire_in=600):
        return jwt.encode(
            {'reset_password':self.id, 'exp':time()+expire_in}, app.config['SECRET_KEY'], algorithm='HS256'
        ).decode('utf-8')

    # 验证token
    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'], algorithm='HS256')['reset_password']
        except:
            return
        return User.query.get(id)

    def __repr__(self):
        return '<User {} >'.format(self.username)

class Post(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.INTEGER, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {} >'.format(self.body)

@login.user_loader
def load_loader(id):
    return User.query.get(int(id))
