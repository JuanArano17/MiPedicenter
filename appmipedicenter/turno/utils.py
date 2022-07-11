from flask_mail import Message
from appmipedicenter import mail
def mandar_mail_turno(cliente, date_str, hora, nombre_empleado):
       msg = Message('Confirmacion de turno Pedicenter', sender='mipedicenter@gmail.com', recipients=[cliente.email])
       msg.body = f''' Estimado/a {cliente.username}:

 Un turno podologico ha sido asignado exitosamente para el dia {date_str} a las {hora}hs con {nombre_empleado} en la sede: Arenales-1283-PB-Recoleta .
        
        Att: Pedicenter.'''
       mail.send(msg)