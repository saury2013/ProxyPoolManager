# -*- coding: utf-8 -*-
__author__ = 'Allen'

from flask import Flask,g
from proxypool.db_connector import RedisClient

__all__ = ['app']

app = Flask(__name__)

def get_db_conn():
    if not hasattr(g,'redis'):
        g.redis = RedisClient()
    return g.redis

@app.route('/')
def index():
    return '<h2>Welcome to ProxyManger</h2>'

@app.route('/random')
def get_proxy():
    conn = get_db_conn()
    return conn.random()

@app.route('/count')
def get_counts():
    conn = get_db_conn()
    return str(conn.get_count())

if __name__ == '__main__':
    app.run()