import os
from flask import Flask, request, render_template, flash, redirect, url_for, session, Blueprint
from tempfile import mkdtemp
from flask_mysqldb import MySQL
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from functools import wraps

app = Flask(__name__, instance_path=os.path.join(os.path.abspath(os.curdir), 'instance'), instance_relative_config=True, static_url_path="", static_folder="static")
app.config.from_pyfile('config.cfg')
app.config['SESSION_FILE_DIR'] = mkdtemp()
mysql=MySQL(app)
Session(app)

def execute_db(query,args=()):
    cur=mysql.connection.cursor()
    cur.execute(query,args)
    mysql.connection.commit()
    cur.close()
def query_db(query,args=(),one=False):
    cur=mysql.connection.cursor()
    result=cur.execute(query,args)
    if result>0:
        values=cur.fetchall()
        return values

# Importing Blueprints
from app.views.main import main

# Registering Blueprints
app.register_blueprint(main)
