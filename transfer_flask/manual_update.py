from flask import Flask
import flask_sqlalchemy

user = 'tiernan'
password = 'password'
host = 'localhost'
database = 'transfer_money'
port = 5432
DATABASE_CONNECTION_URI = f'postgresql+psycopg2://{user}:{password}@localhost:{port}/{database}'

db = flask_sqlalchemy.SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_CONNECTION_URI
    app.config['SECRET_KEY'] = 'c467a56be94d50cc58967106467b34c40d857b32f1d6810b0a'
    app.config['SQLACLHEMY_TRACK_MODIFICATIONS'] = True
    app.app_context().push()
    db.init_app(app)
    # this will create all tables based on model.py
    print("create all on ", db)
    db.create_all()
    return app
