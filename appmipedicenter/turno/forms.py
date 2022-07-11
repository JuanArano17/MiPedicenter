from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField
from wtforms.validators import DataRequired, ValidationError
from appmipedicenter.models import Cliente

class AsignarTurno(FlaskForm):
    dni = IntegerField('DNI paciente', validators=[DataRequired()])
    '''id_hora = SelectField(u'Hora de Turno', choices=[('1', '10:00'), ('2', '10:30'), ('3', '11:00')
                                                    , ('4', '11:30'), ('5', '12:00'), ('6', '12:30')
                                                    , ('7', '13:00'), ('8', '13:30'), ('9', '14:00')
                                                    , ('10', '14:30'), ('11', '15:00'), ('12', '15:30')
                                                    , ('13', '16:00'), ('14', '16:30'), ('15', '17:00')
                                                    , ('16', '17:30'), ('17', '18:00'), ('18', '18:30')])
    listaPodologo = Empleado.query.filter_by(id_tipo = 1).all()
    listaPodologoSelect = []
    for i in range(0, len(listaPodologo)):
        listaPodologoSelect.append((listaPodologo[i].id, listaPodologo[i].username))
    id_podologo = SelectField(u'Seleccione Podologo', choices=listaPodologoSelect)'''
    submit = SubmitField('Guardar Turno')

    def validate_dni(self, dni):
        cliente = Cliente.query.filter_by(id_cliente = dni.data).first()
        if not bool(cliente):
            raise ValidationError("El cliente no esta registrado.")