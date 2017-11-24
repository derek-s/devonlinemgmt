# !/usr/bin/python
# -*- coding: UTF-8 -*-

from flask import (Flask, render_template, redirect, url_for, request, flash)
from flask_login import login_required, login_user, logout_user, current_user
from flask_bootstrap import Bootstrap

from forms import LoginForm
from ext import db, login_manager
from models import User

SECRET_KEY = '12efc6ca97aefb8e1f6a589c6f334a405bca977bc9cec023f193ee975379e153'

app = Flask(__name__)

app.secret_key = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:123a+-@192.168.10.105/devonlie"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bootstrap = Bootstrap(app)
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "login"

@app.route("/", methods=['GET', 'POST'])
@login_required
def hello():
    return "hello world Flask"

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username'], password=request.form['password']).first()
        if user:
            login_user(user)
            flash("logged in!")
            return redirect(url_for('hello'))
        else:
            flash("logged filed")
    form = LoginForm()
    return render_template('login.html', form=form)

@login_manager.user_loader
def load_user(id):
    return User.query.filter_by(id=int(id)).first()

if __name__ == '__main__':
    app.run(host='127.0.0.100', port=5000, debug=True)