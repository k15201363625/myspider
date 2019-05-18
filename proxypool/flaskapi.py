from flask import Flask,g
from proxypool.database import RedisClient
from proxypool.settings import API_HOST,API_PORT
app = Flask(__name__)

# 通过g查看全局
def get_conn():
    if not hasattr(g,'redisconn'):
        g.redisconn = RedisClient()
    return g.redisconn

@app.route('/')
def index():
    return '<h1>myproxy pool</h1>'

@app.route('/count')
def count():
    return str(get_conn().count())

@app.route('/all')
def getall():
    return str(get_conn().getall())

@app.route('/random')
def random():
    res = get_conn().random()
    if res:
        return res
    else:
        return 'sorry,proxy pool is empty'

@app.route('/query/<query_proxy>',methods=['GET'])
def query(query_proxy):
    return get_conn().exists(query_proxy)

if __name__ == '__main__':
    app.run(host=API_HOST,port=API_PORT)




