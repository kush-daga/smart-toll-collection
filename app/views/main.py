from flask import Flask, request, render_template, flash, redirect, url_for, session, Blueprint
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt as sha
from flask_session import Session;
from app import *
import requests
import bs4

main = Blueprint('main', __name__)

@main.route('/test')
def test():
    res = requests.get('http://tweeplers.com/hashtags/?cc=IN')
    soup = bs4.BeautifulSoup(res.text,'lxml')
    new = soup.find_all( class_='wordwrap')
    titles=[]
    hashes=[]
    urls=[]

    for tag in new:
        res2 = requests.get('https://www.bing.com/news/search?q=india'+tag.text[1:]+'&FORM=HDRSC6')
        soup2 = bs4.BeautifulSoup(res2.text, 'lxml')
        new2 = soup2.find_all(class_="title")
        for ans in new2:
            titles.append(ans.text)
            hashes.append(tag.text)
            url =ans.get('href')
            urls.append(url)
    
    all = zip(titles,hashes,urls)
    

    return render_template("test1.html", **locals())

@main.route('/')
def index():
    return render_template("index.html", **locals())