from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, SubmitField, IntegerField, DateField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from appmipedicenter.models import Empleado

class RegistrationForm(FlaskForm):
    username = StringField('Nombre Completo', validators=[DataRequired()])
    dni = IntegerField('DNI', validators=[DataRequired()])
    fecha_nacimiento = DateField('Fecha Nacimiento', validators=[DataRequired()])
    telefono = IntegerField('Nro de Telefono (solo carácteres numéricos)', validators=[DataRequired()])
    email = StringField('E-Mail', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar contraseña', validators=[DataRequired(), EqualTo('password')])
    id_tipo = SelectField(u'Tipo de cuenta', choices=[('1', 'Podologo'), ('2', 'Recepcionista')])
    submit = SubmitField('Registrarse')

    def validate_email(self, email):
        empleado = Empleado.query.filter_by(id= email.data).first()
        if empleado:
            raise ValidationError("El email ya esta en uso")

    def validate_dni(self, dni):
        empleado = Empleado.query.filter_by(dni = dni.data).first()
        if empleado:
            raise ValidationError("El DNI ya esta en uso")



class LoginForm(FlaskForm):
    email = StringField('E-Mail', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Acceder')


class UpdateAccountForm(FlaskForm):
    username = StringField('Nombre Completo', validators=[DataRequired()])
    dni = IntegerField('DNI', validators=[DataRequired()])
    fecha_nacimiento = DateField('Fecha Nacimiento YYYY-MM-DD', validators=[DataRequired()])
    telefono = IntegerField('Nro de Telefono (solo carácteres numéricos)', validators=[DataRequired()])
    submit = SubmitField('Actualizar')

    def validate_dni(self, dni):
        if dni.data != current_user.dni:
            empleado = Empleado.query.filter_by(dni = dni.data).first()
            if empleado:
                raise ValidationError("El DNI ya esta en uso")