import email
from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, SubmitField, IntegerField, DateField, PasswordField, BooleanField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from appmipedicenter.models import Empleado, Cliente

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

class ClienteForm(FlaskForm):
    dni = IntegerField('DNI', validators=[DataRequired()])
    username = StringField('Nombre Completo', validators=[DataRequired()])
    email = StringField('E-Mail', validators=[DataRequired(), Email()])
    fecha_nacimiento = DateField('Fecha Nacimiento YYYY-MM-DD', validators=[DataRequired()])
    telefono = IntegerField('Nro de Telefono (solo carácteres numéricos)', validators=[DataRequired()])
    submit = SubmitField('Crear')

    def validate_dni(self, dni):
        cliente = Cliente.query.filter_by(id_cliente = dni.data).first()
        if cliente:
            raise ValidationError("El DNI ya esta en uso")
    
    def validate_email(self, email):
        cliente = Cliente.query.filter_by(email = email.data).first()
        if cliente:
            raise ValidationError("El Email ya esta en uso")

    def validate_telefono(self, telefono):
        cliente = Cliente.query.filter_by(telefono = telefono.data).first()
        if cliente:
            raise ValidationError("El telefono ya esta en uso")

class ClienteUpdateForm(FlaskForm):
    dni = IntegerField('DNI', validators=[DataRequired()])
    username = StringField('Nombre Completo', validators=[DataRequired()])
    email = StringField('E-Mail', validators=[DataRequired(), Email()])
    fecha_nacimiento = DateField('Fecha Nacimiento YYYY-MM-DD', validators=[DataRequired()])
    telefono = IntegerField('Nro de Telefono (solo carácteres numéricos)', validators=[DataRequired()])
    submit = SubmitField('Modificar')

class AsignarTurno(FlaskForm):
    dni = IntegerField('DNI paciente', validators=[DataRequired()])
    id_hora = SelectField(u'Hora de Turno', choices=[('1', '10:00'), ('2', '10:30'), ('3', '11:00')
                                                    , ('4', '11:30'), ('5', '12:00'), ('6', '12:30')
                                                    , ('7', '13:00'), ('8', '13:30'), ('9', '14:00')
                                                    , ('10', '14:30'), ('11', '15:00'), ('12', '15:30')
                                                    , ('13', '16:00'), ('14', '16:30'), ('15', '17:00')
                                                    , ('16', '17:30'), ('17', '18:00'), ('18', '18:30')])
    listaPodologo = Empleado.query.filter_by(id_tipo = 1).all()
    listaPodologoSelect = []
    for i in range(0, len(listaPodologo)):
        listaPodologoSelect.append((listaPodologo[i].id, listaPodologo[i].username))
    id_podologo = SelectField(u'Seleccione Podologo', choices=listaPodologoSelect)
    date = DateField('Fecha', validators=[DataRequired()])
    submitUpdate = SubmitField('Guardar Turno')

    def validate_dni(self, dni):
        cliente = Cliente.query.filter_by(id_cliente = dni.data).first()
        if not cliente:
            raise ValidationError("El cliente no esta registrado.")