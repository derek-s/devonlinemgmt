# !/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect
from flask_jsglue import JSGlue
from jinja2.ext import do
from jinja2 import Environment


from ext import login_manager, md5s
from models import *
from views.admin import adminbg
from views.ajaxquery import ajaxquery
from views.login import loginview
from views.index import indexview
from views.serach import serachview
from views.profile import profileview
from errorhandler import errorview

SECRET_KEY = '12efc6ca97aefb8e1f6a589c6f334a405bca977bc9cec023f193ee975379e153'

app = Flask(__name__, template_folder="templates")

# add Flask_URL in js code
jsglue = JSGlue(app)

app.register_blueprint(adminbg)
app.register_blueprint(ajaxquery)
app.register_blueprint(loginview)
app.register_blueprint(indexview)
app.register_blueprint(serachview)
app.register_blueprint(profileview)
app.register_blueprint(errorview)

app.secret_key = SECRET_KEY
app.config[
    'SQLALCHEMY_DATABASE_URI'] = "mysql://root:123a+-@192.168.10.105/devonlie"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Templates dev Testing Code
app.jinja_env.auto_reload = True

# add do ext
app.jinja_env.add_extension("jinja2.ext.do")

bootstrap = Bootstrap(app)
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "loginview.login"
login_manager.login_message = u"需要登录才可以查看页面"
CSRFProtect(app)

env = app.jinja_env
env.filters['md5s'] = md5s


if __name__ == '__main__':
    app.run(host='127.0.0.100', port=5000, debug=True)
