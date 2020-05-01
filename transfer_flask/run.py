from flask import Flask, render_template, redirect, request, url_for, abort
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from form import AddUserForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from werkzeug.urls import url_parse
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = 'c467a56be94d50cc58967106467b34c40d857b32f1d6810b0a'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://tiernan:password@localhost:5432/transfer_money'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager(app)
login_manager.login_view = 'login'
db = SQLAlchemy(app)

from models import Users, Transaction

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
    return render_template('login_form.html', form=form)


@app.route('/transaction/<int:id>')
def show_transaction(id):
    trans = Transaction.get_by_user(id)
    if trans is None:
        abort(404)
    return render_template('transaction.html', trans=trans, id=id)


@app.route("/users/", methods=['GET', 'POST'])
# @login_required
def user_form():
    form = AddUserForm()
    if form.validate_on_submit():
        name = form.name.data
        last_name = form.last_name.data
        msdi = form.msdi.data

        next = request.args.get('next', None)
        if next:
            return redirect(next)
        return redirect(url_for('hello_world'))
    return render_template("user_form.html", form=form)


@app.route("/users/<int:id>/")
# @login_required
def users(id=None):
    return render_template("users.html", id=id)
    # return "User: {}.".format(id)


@login_manager.user_loader
def load_user(user_id):
    return Users.get_by_id(int(user_id))


@app.route('/signup/', methods=['GET', 'POST'])
def show_signup_form():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        name = form.name.data
        last_name = form.last_name.data
        email = form.email.data
        password = form.password.data
        user = Users.get_email(email)
        if user is not None:
            error = f'El email {email} ya se encuentra registrado.'
        else:
            user = Users(name=name, email=email)
            user.set_password(password)
            user.save()

            login_user(user, remember=True)
            next_page = request.args.get('next', None)
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
    return render_template('signup_form.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))










