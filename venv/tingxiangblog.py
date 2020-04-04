# -*- coding: UTF-8 -*-
"""
  _author: Simon Qu
  _date: 20200101
  _version: 1.0.0
  _description: 
"""

from app import app

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080, debug=True)

