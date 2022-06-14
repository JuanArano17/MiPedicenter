from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField, IntegerField, DateField, PasswordField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Nombre Completo', validators=[DataRequired()])
    dni = IntegerField('DNI', validators=[DataRequired()])
    fecha_nacimiento = DateField('Fecha Nacimiento YYYY-MM-DD', validators=[DataRequired()])
    telefono = IntegerField('Nro de Telefono (solo carácteres numéricos)', validators=[DataRequired()])
    email = StringField('E-Mail', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar contraseña', validators=[DataRequired(), EqualTo('password')])
    id_tipo = SelectField(u'Tipo de cuenta', choices=[('1', 'Podologo'), ('2', 'Recepcionista')])
    submit = SubmitField('Registrarse')

class LoginForm(FlaskForm):
    email = StringField('E-Mail', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Registrarse')
