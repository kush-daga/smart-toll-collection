from flask import Flask, request, render_template, flash, redirect, url_for, session, Blueprint
from passlib.hash import sha256_crypt as sha
from flask_session import Session;
from app import *
from app.views.ml.Main import main


main2 = Blueprint('main2', __name__)

@main2.route('/')
def index():
    a = main()
    return render_template("index.html", **locals())
@main2.route('/form')
def form():
    return render_template("form.html", **locals())
@main2.route('/generic')
def generic():
    return render_template("generic.html", **locals())    