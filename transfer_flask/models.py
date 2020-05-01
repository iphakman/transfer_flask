from flask_login import UserMixin
from flask import url_for
from werkzeug.security import generate_password_hash, check_password_hash
from run import db
from sqlalchemy.exc import IntegrityError


class Users(UserMixin):

    __tablename__ = ''

    def __init__(self):
        self.id = db.Column(db.Integer, primary_key=True)
        self.name = db.Column(db.String(80), nullable=False)
        self.last_name = db.Column(db.String(80), nullable=False)
        self.password = db.Column(db.String(40), nullable=False)
        self.email = db.Column(db.String(256), nullable=False)
        self.msdi = db.Column(db.String(50), nullable=False)
        self.is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<User {self.email}>\n<ID {self.id}>"

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def get_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return Users.query.get(id)

    @staticmethod
    def get_email(email):
        return Users.query.filter_by(email=email).first()

    @staticmethod
    def get_all():
        return Users.query.all()


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id',
                        ondelete='CASCADE'), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    destination = db.Column(db.String, db.ForeignKey('Users.email'),
                            nullable=False)

    def __repr__(self):
        return f'<User {self.user_id}\n{self.id}>'

    def save(self):
        if not self.id:
            db.session.add(self)
        if not self.destination:
            Users.get_email(self.destination)

        saved = False
        count = 0
        while not saved:
            try:
                db.session.commit()
                saved = True
            except IntegrityError:
                count += 1

    def public_url(self):
        return url_for('show_trans', amount=self.amount)

    @staticmethod
    def get_by_id(id):
        return Transaction.query.filter_by(id=id).first()

    @staticmethod
    def get_all():
        return Transaction.query.all()
