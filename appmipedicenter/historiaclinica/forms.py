from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, ValidationError
from appmipedicenter.models import Cliente

class HistoriaClinicaForm(FlaskForm):
    diagnostico = TextAreaField('Diagnostico General', validators=[DataRequired()])
    diabetes = BooleanField('¿Posee diabetes?')
    antecedentes = StringField('Antecedentes')
    onicopatias = StringField('Onicopatias')
    otros_datos = StringField('Otros datos')
    submit = SubmitField('Guardar')

class TablaHistoriaClinicaForm(FlaskForm):
    diagnostico = TextAreaField('Diagnostico General', validators=[DataRequired()])
    diabetes = BooleanField('¿Posee diabetes?')
    antecedentes = StringField('Antecedentes')
    onicopatias = StringField('Onicopatias')
    otros_datos = StringField('Otros datos')
    id_cliente = IntegerField('DNI paciente',validators=[DataRequired()])
    submit = SubmitField('Guardar')

    def validate_id_cliente(self, id_cliente):
        cliente = Cliente.query.filter_by(id_cliente = id_cliente.data).first()
        if not bool(cliente):
            raise ValidationError("El cliente no esta registrado.")


