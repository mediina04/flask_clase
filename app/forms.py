from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

# Formulario para el inicio de sesión
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Contrasenya', validators=[DataRequired()])
    submit = SubmitField('Iniciar sessió')

# Formulario para el registro de usuario
class RegisterForm(FlaskForm):
    username = StringField('Nom d\'usuari', validators=[DataRequired(), Length(min=4, max=100)])
    password = PasswordField('Contrasenya', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirma la contrasenya', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrar-se')
