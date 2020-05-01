from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField, FloatField
from wtforms.validators import DataRequired, Length


class AddUserForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired(), Length(max=64)])
    last_name = StringField('Apellido', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    msdi = StringField('MSDI', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Registrar')


class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class AddTransForm(FlaskForm):
    origin = IntegerField('user_id', validators=[DataRequired()])
    name = StringField('name')
    destination = StringField('destination', validators=[DataRequired()])
    currency = StringField('currency', validators=[DataRequired()], default='MXN')
    amount = FloatField('amount', validators=[DataRequired()])
    submit = SubmitField('Agregar')

