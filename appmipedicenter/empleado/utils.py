from flask_mail import Message
from appmipedicenter import mail
from appmipedicenter.models import Empleado

def mandar_mail_turno(email):
       emp = Empleado.query.filter_by(id= email.data).first()
       msg = Message('Pedido para obtener datos de cuenta', sender='mipedicenter@gmail.com', recipients=[email])
       msg.body = f''' Querido/a {emp.username}, Su contraseña para entrar al sistema MiPedicenter es:
              
       Att: Pedicenter.'''
       mail.send(msg)