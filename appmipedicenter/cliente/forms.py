from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DateField
from wtforms.validators import DataRequired, Email, ValidationError
from appmipedicenter.models import Cliente

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
    def __init__(self, cliente):
        super().__init__()
        self.cliente = cliente

    dni = IntegerField('DNI', validators=[DataRequired()])
    username = StringField('Nombre Completo', validators=[DataRequired()])
    email = StringField('E-Mail', validators=[DataRequired(), Email()])
    fecha_nacimiento = DateField('Fecha Nacimiento YYYY-MM-DD', validators=[DataRequired()])
    telefono = IntegerField('Nro de Telefono (solo carácteres numéricos)', validators=[DataRequired()])
    submit = SubmitField('Modificar')

    # Error validators
    def validate_dni(self, dni):
        if self.cliente.id_cliente != dni.data:
            clien = Cliente.query.filter_by(id_cliente = dni.data).first()
            if clien:
                raise ValidationError("El DNI ya esta en uso")
    
    def validate_email(self, email):
        if self.cliente.email != email.data:
            clien = Cliente.query.filter_by(email = email.data).first()
            if clien:
                raise ValidationError("El Email ya esta en uso")

    def validate_telefono(self, telefono):
        if self.cliente.telefono != telefono.data:
            clien = Cliente.query.filter_by(telefono = telefono.data).first()
            if clien:
                raise ValidationError("El telefono ya esta en uso")