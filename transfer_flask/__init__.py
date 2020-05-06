from flask import Flask
import flask_sqlalchemy
import requests
from bs4 import BeautifulSoup
from . import config

db = flask_sqlalchemy.SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_CONNECTION_URI
    app.config['SECRET_KEY'] = 'c467a56be94d50cc58967106467b34c40d857b32f1d6810b0a'
    app.config['SQLACLHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['DEBUG'] = True
    app.app_context().push()
    db.init_app(app)
    # this will create all tables based on model.py
    with app.app_context():
        db.create_all()
        return app


def get_currency_date(currencies):
    url_string = 'https://www.google.com/search?client=ubuntu&channel=fs&q='
    url_string += currencies
    url_string += '+to+USD&ie=utf-8&oe=utf-8'
    page = requests.get(url_string)

    result = set()
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')
        div = soup.find_all(class_='BNeawe iBp4i AP7Wnd')

        for val in div:
            result.add(val.text.split()[0])
        # BNeawe iBp4i AP7Wnd

    if len(result):
        return max(result)
    else:
        return None