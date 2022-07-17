from http.client import REQUEST_HEADER_FIELDS_TOO_LARGE
from flask import render_template, url_for, flash, redirect, request, Blueprint
from appmipedicenter.models import Cliente, Historiaclinica, Turno
from appmipedicenter.cliente.forms import  ClienteForm, ClienteUpdateForm
from appmipedicenter import db
from flask_login import current_user, login_required
from datetime import *

cliente = Blueprint('cliente', __name__)

@cliente.route("/pacientes", methods=['GET', 'POST'])
@login_required
def pacientes():
        if current_user.is_authenticated:
                if current_user.id_tipo == 2: 
                        client_list = Cliente.query.all()
                        form = ClienteForm()
                        if form.validate_on_submit():
                                cliente = Cliente(
                                        id_cliente = form.dni.data,
                                        username = form.username.data,
                                        email = form.email.data,
                                        fecha_nacimiento = form.fecha_nacimiento.data,
                                        telefono = form.telefono.data
                                )
                                db.session.add(cliente)
                                db.session.commit()
                                flash(f'El cliente {form.username.data} ha sido ingresado/a con exito.', 'success')
                                return redirect(url_for('cliente.pacientes'))
                        return render_template('pacientes.html', title="Gestion de Pacientes", clientes = client_list, form=form) 
                else:
                        return redirect(url_for('main.home'))
        else:
                return redirect(url_for('empleado.login'))

@cliente.route("/pacientes/editar/<int:id_cliente>", methods=['GET', 'POST'])
@login_required
def editar_pacientes(id_cliente):
        if current_user.is_authenticated:
                if current_user.id_tipo == 2: 
                        cliente = Cliente.query.filter_by(id_cliente = id_cliente).first()
                        form = ClienteUpdateForm(cliente)
                        if form.validate_on_submit():
                                if cliente.id_cliente != form.dni.data:
                                        listaTurnosCliente = Turno.query.filter_by(id_cliente = cliente.id_cliente)
                                        for turno in listaTurnosCliente:
                                                turno.id_cliente = form.dni.data
                                cliente.id_cliente = form.dni.data
                                cliente.username = form.username.data
                                cliente.email = form.email.data
                                cliente.fecha_nacimiento = form.fecha_nacimiento.data
                                cliente.telefono = form.telefono.data
                                db.session.commit()
                                flash(f'Los datos de {form.username.data} han sido actualizados.', 'success')
                                return redirect(url_for('cliente.pacientes'))
                        elif request.method=='GET':
                                form.username.data = cliente.username
                                form.dni.data = cliente.id_cliente
                                form.email.data = cliente.email
                                form.telefono.data = cliente.telefono
                                form.fecha_nacimiento.data = cliente.fecha_nacimiento 
                        return render_template('editar_paciente.html', title="Edicion de Clientes", form=form)
                else:
                        return redirect(url_for('main.home'))
        else:
                return redirect(url_for('empleado.login'))

@cliente.route("/pacientes/eliminar/<int:id_cliente>", methods=['GET', 'POST'])
@login_required
def eliminar_pacientes(id_cliente):
        if current_user.is_authenticated:
                if current_user.id_tipo == 2: 
                        cliente = Cliente.query.filter_by(id_cliente = id_cliente).first()
                        lista_turnos_cliente = Turno.query.filter_by(id_cliente = cliente.id_cliente)
                        lista_historias_clinicas = Historiaclinica.query.filter_by(id_cliente = id_cliente)
                        for i in lista_turnos_cliente:
                                db.session.delete(i)
                        for i in lista_historias_clinicas:
                                db.session.delete(i)
                        db.session.delete(cliente)
                        db.session.commit()
                        flash(f'Los datos de {cliente.username} han sido borrados.', 'success')
                        return redirect(url_for('cliente.pacientes'))
                else:
                        return redirect(url_for('main.home'))
        else:
                return redirect(url_for('empleado.login'))