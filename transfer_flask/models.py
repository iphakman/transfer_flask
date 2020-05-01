from flask_login import UserMixin
from flask import url_for
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from sqlalchemy.exc import IntegrityError


class Users(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    phone_number = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    msdi = db.Column(db.String(50), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<'id': {self.id}>\n'" \
               f"<phone_number': '{self.phone_number}'>\n" \
               f"<'name': {self.name}>\n"

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
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

    __tablename__ = 'transaction'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id',
                        ondelete='CASCADE'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='MXN')
    destination = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<User {self.user_id}\n{self.id}>'

    def save(self):
        if not self.id:
            db.session.add(self)
        if not self.destination:
            Users.get_email(self.destination)

        print("USER ID: ", self.user_id)
        print("EMAIL DESTINATARIO:", self.destination)

        saved = False
        count = 0
        while not saved:
            try:
                db.session.commit()
                print("Commit success!!!")
                saved = True
            except IntegrityError as e:
                print("Error de integridad: ", count, e)
                count += 1
        else:
            print("Datos a guardar: {} | {} | {} | {}".format(self.user_id,
                                                              self.amount,
                                                              self.currency,
                                                              self.destination))

    def public_url(self):
        return url_for('show_trans', amount=self.amount)

    @staticmethod
    def get_by_user(id):
        return Transaction.query.filter_by(user_id=id)

    @staticmethod
    def get_all():
        return Transaction.query.all()
