from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired

class HistoriaClinicaForm(FlaskForm):
    diagnostico = TextAreaField('Diagnostico General', validators=[DataRequired()])
    diabetes = BooleanField('¿Posee diabetes?')
    antecedentes = StringField('Antecedentes')
    onicopatias = StringField('Onicopatias')
    otros_datos = StringField('Otros datos')
    submit = SubmitField('Guardar')