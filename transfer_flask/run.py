from flask_paginate import Pagination, get_page_args
from flask import render_template, redirect, request, url_for, abort, session
from flask_login import (LoginManager, current_user, login_user,
                         logout_user, login_required, session_protected)
from .form import AddUserForm, LoginForm, AddTransForm, AddCurrencies
from datetime import datetime
from . import create_app, db, get_currency_date
from werkzeug.urls import url_parse
from flask_migrate import Migrate

app = create_app()
# app.send_static_file('base.css')

from .models import Users, Transaction, Balance, CurrencyConvert
login_manager = LoginManager(app)
login_manager.login_view = 'login'

migrate = Migrate(app, db)
db.create_all()


@app.route('/')
def index():
    users = Users.get_all()
    return render_template('users.html', users=users)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.get_email(form.email.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
    return render_template('signup_form.html', form=form)


@app.route('/users/<int:id>/transaction')
def show_transaction(id):
    trans = Transaction.get_by_user(id)
    user = Users.get_by_id(id)
    if trans is None:
        abort(404)
    return render_template('transaction.html', trans=trans, user=user)


@app.route('/transaction', methods=['GET', 'POST'])
@login_required
def create_transaction():
    user_loged = session['_user_id']

    form = AddTransForm()
    if form.validate_on_submit():
        destination = form.destination.data
        currency = form.currency.data
        amount = form.amount.data

        print("will try to transfer {} {} from {} to {}".format(amount, currency, id, destination))
        destiny = Users.get_email(destination)
        print("DESTINY:", destiny)
        if destiny is None:
            error = f'El email {destination} no existe.'
        else:
            user = Users.get_by_id(user_loged)
            print("now will transfer {} {} from {} to {}".format(amount, currency, user.email, destiny.email))
            trans = Transaction(user_id=user.id,
                                amount=amount,
                                currency=currency,
                                destination=destination)

            balance = Balance.get_by_user_id(user.id)

            receiver = Balance.get_by_user_id(Users.get_email(destination))

            if balance.currency != 'USD':
                transfer_amount = CurrencyConvert.translate(amount,
                                                            balance.currency,
                                                            currency)
            else:
                transfer_amount = balance.amount

            if balance.currency != currency:
                if currency != 'USD':
                    receiver_amount = CurrencyConvert.translate(amount,
                                                                currency,
                                                                receiver.currency)
            else:
                receiver_amount = transfer_amount

            if transfer_amount >= amount:
                balance.amount -= transfer_amount
                receiver.amount += receiver_amount

                trans.status = 'S'
            else:
                trans.status = 'IF'

            trans.save()
            balance.save()
            receiver.save()

            next_page = request.args.get('next', None)
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('show_transaction', id=user.id)
            return redirect(next_page)

    return render_template("transaction_form.html", form=form)


def get_pagina(milist, offset=0, per_page=20):
    return milist[offset:offset + per_page]


@app.route('/currencies', methods=['GET'])
def get_currencies():
    currencies = CurrencyConvert.get_all()
    total = len(currencies)
    print("Total de monedas:", total)
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')

    pagination_list = get_pagina(currencies, offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total)

    return render_template("currencies_list.html", currencies=pagination_list, page=page,
                           per_page=per_page, pagination=pagination)


@app.route("/currencies_add", methods=['GET', 'POST'])
def renew_currencies():

    form = AddCurrencies()
    print("form is AddCurrencies")
    if form.validate_on_submit():
        filename = form.filename.data
        print("validate file...", filename)
        if filename is None:
            error = f'El archivo {filename} no existe.'
            print(error)
        else:
            print("Validating currencies from file", filename)

            with open(filename) as ff:
                lines = ff.readlines()
                print("Total lines: ", len(lines))

                for line in lines:
                    print("*** line:", line)
                    values = line.split(',')
                    currency = values[3]

                    rate = get_currency_date(currency)

                    currency_rate = CurrencyConvert(state=line[0], currency=line[1],
                                                    symbol=line[2], iso_code=line[3],
                                                    fractional_unit=line[4], variance=rate)

                    currency_rate.save()

            next_page = request.args.get('next', None)
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('currencies')
            return redirect(next_page)

    return render_template("renew_currencies.html", form=form)


@app.route("/users", methods=['GET', 'POST'])
# @login_required
def user_form():
    form = AddUserForm()
    if form.validate_on_submit():
        name = form.name.data
        last_name = form.last_name.data
        email = form.email.data
        phone_number = form.phone_number.data
        msdi = form.msdi.data
        password = form.password.data
        balance = form.balance.data
        currency = form.currency.data
        is_admin = form.is_admin.data

        user = Users.get_email(email)
        if user is not None:
            error = f'El email {email} ya se encuentra registrado.'
        else:
            user = Users(name=name, last_name=last_name,
                         email=email, password=password,
                         msdi=msdi, phone_number=phone_number,
                         is_admin=is_admin)
            user.save()

            balance_user = Balance(user_id=user.id, amount=balance,
                                   currency=currency, last_modified=datetime.now())

            balance_user.save()

            next_page = request.args.get('next', None)
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)

    return render_template("user_form.html", form=form)


@app.route("/users/<int:id>/")
# @login_required
def users(id=None):
    return render_template("users.html", id=id)
    # return "User: {}.".format(id)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@login_manager.user_loader
def load_user(user_id):
    return Users.get_by_id(int(user_id))




