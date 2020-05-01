from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length


class AddUserForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired(), Length(max=64)])
    last_name = StringField('Apellido', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    msdi = StringField('MSDI', validators=[DataRequired()])
    submit = SubmitField('Registrar')


class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
