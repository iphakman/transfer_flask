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
    phone_number = db.Column(db.String(10), nullable=False)
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
        return self.password == password

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


class CurrencyConvert(db.Model):

    __tablename__ = 'convertion'

    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String, nullable=False)
    currency = db.Column(db.String, nullable=False)
    symbol = db.Column(db.String, nullable=False)
    iso_code = db.Column(db.String(3))
    fractional_unit = db.Column(db.String, nullable=False)
    variance = db.Column(db.Float)

    @staticmethod
    def get_by_currency(currency):
        return Users.query.get(currency)

    @staticmethod
    def get_currency(cc):
        r = CurrencyConvert.query.filter(CurrencyConvert.iso_code == cc).first()
        return r.variance

    @staticmethod
    def translate(amount_m, from_currency, to_currency):
        final_amount = amount_m
        if from_currency != to_currency:
            usd = round(CurrencyConvert.get_currency(from_currency), 2)
            final_amount *= usd

            value = round(CurrencyConvert.get_currency(to_currency), 2)
            final_amount /= value

        return round(final_amount, 2)

    @staticmethod
    def get_all():
        return CurrencyConvert.query.all()


class Balance(db.Model):

    __tablename__ = 'user_balance'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id',
                        ondelete='CASCADE'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3))
    last_modified = db.Column(db.DateTime, nullable=False)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id',))

    def __repr__(self):
        return f"<user_id: {self.user_id}>\n" \
               f"<amount: {self.phone_number}>\n" \
               f"<currency: {self.currency}>\n"

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_user_id(id):
        return Balance.query.get(id)


class Transaction(db.Model):

    __tablename__ = 'transaction'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id',
                        ondelete='CASCADE'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='MXN')
    destination = db.Column(db.String, nullable=False)
    status = db.Column(db.String(2), default='P')

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
