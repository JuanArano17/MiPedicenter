from mailbox import NoSuchMailboxError
from sqlalchemy import ForeignKey
from appmipedicenter import db
from abc import ABC
from datetime import datetime

class Tipoempleado(db.Model):
        id_tipo = db.Column(db.Integer, primary_key=True)
        nombre = db.Column(db.String, nullable=False)
        descripcion = db.Column(db.String, nullable=True, default='')
        empleado = db.relationship('Empleado', backref='Tipo', lazy=True)
        def __repr__(self):
                return f'Tipo Empleado'

class Empleado(db.Model):
        id_empleado = db.Column(db.String, primary_key=True) # Es E-mail
        dni = db.Column(db.Integer, nullable=False)
        username = db.Column(db.String, nullable=False)
        fecha_nacimiento = db.Column(db.Date, nullable=False)
        telefono = db.Column(db.Integer, nullable=False)
        password = db.Column(db.String, nullable=False)
        id_tipo = db.Column(db.Integer, db.ForeignKey('tipoempleado.id_tipo'), nullable=False)
        historia_clinica = db.relationship('Historiaclinica', backref='Escritor', lazy=True)
        turno = db.relationship('Turno', backref='Podologo', lazy=True)
        def __repr__(self):
                return f'Empleado'



class Historiaclinica(db.Model):
        id_historia_clinica = db.Column(db.Integer, primary_key=True)
        datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
        diagnostico = db.Column(db.Text, nullable=False)
        diabetes = db.Column(db.Boolean, nullable = True)
        antecedentes = db.Column(db.String, nullable=True)
        onicopatias = db.Column(db.String, nullable=True)
        otros_datos = db.Column(db.Text, nullable=True)
        id_empleado = db.Column(db.Integer, db.ForeignKey('empleado.id_empleado'), nullable=False)
        id_cliente = db.Column(db.Integer, db.ForeignKey('cliente.id_cliente'), nullable=False)
        def __repr__(self):
                return f'Historia Clinica'

class Cliente(db.Model):
        id_cliente = db.Column(db.Integer, primary_key=True) # Es DNI
        username = db.Column(db.String, nullable=False)
        email = db.Column(db.String, unique=True, nullable=False)
        fecha_nacimiento = db.Column(db.Date, nullable=False)
        telefono = db.Column(db.Integer, unique=True, nullable=False)
        historia_clinica = db.relationship('Historiaclinica', backref='Paciente', lazy=True)
        turno = db.relationship('Turno', backref='Paciente', lazy=True)
        def __repr__(self):
                return f'Cliente'

class Hora(db.Model):
        id_hora = db.Column(db.Integer, primary_key=True) 
        hora = db.Column(db.String, nullable=False)
        turno = db.relationship('Turno', backref='Hora', lazy=True)
        def __repr__(self):
                return f'Hora'

class Turno(db.Model):
        id_horario = db.Column(db.Integer, primary_key=True) 
        date = db.Column(db.Date, nullable=False)
        disponible = db.Column(db.Boolean, nullable=False, default=True)
        atendido = db.Column(db.Boolean, nullable=False, default=False)
        id_hora = db.Column(db.Integer, db.ForeignKey('hora.id_hora'), nullable=False)
        id_empleado = db.Column(db.Integer, db.ForeignKey('empleado.id_empleado'), nullable=False)
        id_cliente = db.Column(db.Integer, db.ForeignKey('cliente.id_cliente'), nullable=True)
        def __repr__(self):
                return f'Turno'