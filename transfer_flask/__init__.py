from flask import Flask
import flask_sqlalchemy

from . import config

db = flask_sqlalchemy.SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_CONNECTION_URI
    app.config['SECRET_KEY'] = 'c467a56be94d50cc58967106467b34c40d857b32f1d6810b0a'
    app.config['SQLACLHEMY_TRACK_MODIFICATIONS'] = False
    app.app_context().push()
    db.init_app(app)
    db.create_all()
    return app
