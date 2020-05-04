from flask import render_template, redirect, request, url_for, abort
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from .form import AddUserForm, LoginForm, AddTransForm
from datetime import datetime
from . import create_app, db
from werkzeug.urls import url_parse
from flask_migrate import Migrate

app = create_app()
# app.send_static_file('base.css')

from .models import Users, Transaction, Balance, CurrencyConvert
login_manager = LoginManager(app)
login_manager.login_view = 'login'

migrate = Migrate(app, db)


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


@app.route('/transaction/<int:id>', methods=['GET', 'POST'])
@login_required
def create_transaction(id):

    form = AddTransForm()
    if form.validate_on_submit():
        destination = form.destination.data
        currency = form.currency.data
        amount = form.amount.data
        destiny = Users.get_email(destination)
        if destiny is None:
            error = f'El email {destination} no existe.'
        else:
            user = Users.get_by_id(id)
            trans = Transaction(user_id=user.id,
                                amount=amount,
                                currency=currency,
                                destination=destination)

            balance = Balance.get_by_user_id(user.id)

            if balance.amount >= amount:
                balance.amount -= amount

                trans.status = 'S'
            else:
                trans.status = 'IF'

            trans.save()
            balance.save()

            next_page = request.args.get('next', None)
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('show_transaction', id=user.id)
            return redirect(next_page)

    return render_template("transaction_form.html", form=form)


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




