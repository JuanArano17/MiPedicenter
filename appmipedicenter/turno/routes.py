from http.client import REQUEST_HEADER_FIELDS_TOO_LARGE
from flask import render_template, url_for, flash, redirect, request, Blueprint
from appmipedicenter.models import *
from appmipedicenter.turno.forms import AsignarTurno
from appmipedicenter.turno.utils import mandar_mail_turno
from appmipedicenter.Plantilla import Plantilla
from appmipedicenter import db
from flask_login import current_user, login_required
from datetime import *

turno = Blueprint('turno', __name__)

@turno.route("/mi-calendario") #Incluye CRUD Turnos (envio mail), CURD Clientes y Disp Horario
@login_required
def mi_calendario():
        if request.method == "POST":
                date_str = request.get_data()
                return redirect(url_for("turno.plantilla_turnos", date_str = date_str))
        return render_template('mi_calendario.html', title="Calendario Turnos") 

@turno.route("/plantilla-turnos/<string:date_str>", methods=['GET', 'POST'])
@login_required
def plantilla_turnos(date_str):
        if current_user.is_authenticated:
                datePlant = date.fromisoformat(date_str)
                plantilla = Plantilla(datePlant)
                if (current_user.id_tipo == 1):     #Incluye CRUD Turnos, Disp Horario e Historias Clinicas
                        podologo = Empleado.query.filter_by(id = current_user.id).first()
                        plantilla.crear_matriz_podologo(podologo)
                        return render_template('plantilla_podologo.html', title="Calendario Vista Podologo", matriz=plantilla.matriz_podologo, plantilla = plantilla)
                elif (current_user.id_tipo == 2):
                        return render_template('plantilla_recep.html', title="Calendario Vista Recepcionista", plantilla=plantilla)
        else:
                return redirect(url_for('main.home'))

@turno.route("/plantilla-turnos/turno-disponible<string:date_str>/<int:i>/<int:j>", methods=['GET', 'POST'])
@login_required
def turno_disponible(date_str, j, i):
        if current_user.is_authenticated:
                datePlant = date.fromisoformat(date_str)
                plantilla = Plantilla(datePlant)
                if (current_user.id_tipo == 1): 
                        return redirect(url_for('main.home'))
                elif (current_user.id_tipo == 2):
                        form_crear_turno = AsignarTurno()
                        id_hora = j
                        id_empleado= plantilla.matriz[0][i].id
                        if form_crear_turno.validate_on_submit():
                                turno = Turno.query.filter_by(date = datePlant, id_empleado = id_empleado, id_hora = id_hora).first()
                                turno.id_cliente = form_crear_turno.dni.data
                                db.session.commit()
                                flash('Se ha asignado el turno con exito', 'success')
                                cliente = Cliente.query.filter_by(id_cliente = form_crear_turno.dni.data).first()
                                nombre_empleado = Empleado.query.filter_by(id = id_empleado).first().username
                                hora = Hora.query.filter_by(id_hora = id_hora).first().hora
                                mandar_mail_turno(cliente, date_str, hora, nombre_empleado)
                                return redirect(url_for("turno.plantilla_turnos", date_str = date_str))
                        return render_template('opciones_turno_disponible.html', title="Opciones para turno disponible", form_crear_turno=form_crear_turno, date_str=date_str, i=i, j=j)

@turno.route("/cambio-disponibilidad/<string:date_str>/<int:i>/<int:j>", methods=['GET', 'POST'])
@login_required
def cambio_disponibilidad(date_str, j, i):
        datePlant = date.fromisoformat(date_str)
        plantilla = Plantilla(datePlant)
        id_empleado = plantilla.matriz[0][i].id
        if current_user.is_authenticated:
                turno = Turno.query.filter_by(date = datePlant, id_empleado = id_empleado, id_hora = j).first()
                if turno.disponible:
                        turno.disponible = False
                else:
                        turno.disponible = True
                db.session.commit()
                return redirect(url_for("turno.plantilla_turnos", date_str = date_str))

@turno.route("/plantilla-turnos/gestion-eliminar-turno<string:date_str>/<int:i>/<int:j>", methods=['GET', 'POST'])
@login_required
def gestion_elimiar_turno(date_str, j, i):
        if current_user.is_authenticated:
                datePlant = date.fromisoformat(date_str)
                plantilla = Plantilla(datePlant)
                if (current_user.id_tipo == 2): 
                        return render_template('gestion_eliminar_turno.html', title="Gesstion de eliminacion de turnos", date_str = date_str, i=i, j=j)
                else:
                        return redirect(url_for('main.home'))

@turno.route("/plantilla-turnos/eliminar-turno<string:date_str>/<int:i>/<int:j>", methods=['GET', 'POST'])
@login_required
def eliminar_turno(date_str, j, i):
        if current_user.is_authenticated:
                datePlant = date.fromisoformat(date_str)
                plantilla = Plantilla(datePlant)
                if current_user.id_tipo == 2:
                        id_hora = j
                        id_empleado = plantilla.matriz[0][i].id
                        turno = Turno.query.filter_by(date = datePlant, id_empleado = id_empleado, id_hora = id_hora).first()
                        turno.id_cliente = None
                        db.session.commit()
                        return redirect(url_for("turno.plantilla_turnos", date_str = date_str))
                else:
                        return redirect(url_for('historiaclinica.historias_clinicas'))

@turno.route("/cambio-atendido/<string:date_str>/<int:i>/<int:j>", methods=['GET', 'POST'])
@login_required
def cambio_atendido(date_str, j, i):
        datePlant = date.fromisoformat(date_str)
        plantilla = Plantilla(datePlant)
        id_hora = j
        id_empleado = plantilla.matriz[0][i-1].id
        if current_user.is_authenticated:
                turno = Turno.query.filter_by(date = datePlant, id_empleado = id_empleado, id_hora = id_hora).first()
                if turno.atendido:
                        turno.atendido = False
                else:
                        turno.atendido = True
                db.session.commit()
                return redirect(url_for("turno.plantilla_turnos", date_str = date_str))