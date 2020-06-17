# -*- coding: UTF-8 -*-
"""
  _author: Simon Qu
  _date: 20200101
  _version: 1.0.0
  _description:  邮件发送模块，用于密码重置等邮件发送
"""

from flask_mail import Message
from app import mail, app
from flask import render_template
from threading import Thread

def send_async_email(app, mail):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    # mail.send(msg)
    Thread(target=send_async_email, args=(app, mail)).start()

# 发在重置密码邮件
def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email(
        'TingxiangBlog 用户密码重置', app.config['ADMINS'][0], recipients=[user.email],
        text_body=render_template('email/reset_password.txt', user=user, token=token),
        html_body=render_template('email/reset_password.html', user=user, token=token)
    )

