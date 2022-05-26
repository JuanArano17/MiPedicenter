from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField, IntegerField, DateField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Nombre Completo', validators=[DataRequired()])
    dni = IntegerField('DNI', validators=[DataRequired()])
    fecha_nacimiento = DateField('Fecha Nacimiento YYYY-MM-DD', validators=[DataRequired()])
    telefono = IntegerField('Nro de Telefono (solo caraácteres numéricos)', validators=[DataRequired()])
    email = StringField('E-Mail', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar contraseña', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrarse')

class LoginForm(FlaskForm):
    email = StringField('E-Mail', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Registrarse')