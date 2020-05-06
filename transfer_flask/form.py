from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, PasswordField,
                     IntegerField, FloatField, BooleanField,
                     FileField)
from wtforms.validators import DataRequired, Length


class AddUserForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired(), Length(max=64)])
    last_name = StringField('Apellido', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    phone_number = IntegerField('Phone', validators=[DataRequired()])
    msdi = StringField('MSDI', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    balance = FloatField('Balance', validators=[DataRequired()])
    currency = StringField('Currency', validators=[DataRequired()], default='MXN')
    is_admin = BooleanField('is_admin', default=False)
    submit = SubmitField('Registrar')


class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)
    submit = SubmitField('Login')


class AddTransForm(FlaskForm):
    destination = StringField('destination', validators=[DataRequired()])
    amount = FloatField('amount', validators=[DataRequired()])
    currency = StringField('currency', validators=[DataRequired()], default='MXN')
    submit = SubmitField('Agregar')


class AddCurrencies(FlaskForm):
    filename = FileField('File_name', validators=[DataRequired()])
    submit = SubmitField('Renovar')
