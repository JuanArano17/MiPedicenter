from http.client import REQUEST_HEADER_FIELDS_TOO_LARGE
from flask import render_template, url_for, flash, redirect, request, Blueprint
from appmipedicenter.models import Empleado, Historiaclinica, Cliente
from appmipedicenter.historiaclinica.forms import HistoriaClinicaForm, HistoriaClinicaForm, TablaHistoriaClinicaForm
from appmipedicenter import db
from flask_login import current_user, login_required
from datetime import *

historiaclinica = Blueprint('historiaclinica', __name__)

@historiaclinica.route("/historias-clinicas/<int:id_cliente>", methods=['GET', 'POST'])
@login_required
def historias_clinicas(id_cliente):
        cliente = Cliente.query.filter_by(id_cliente = id_cliente).first()
        historias_clinicas = Historiaclinica.query.filter_by(id_cliente = id_cliente).all()
        form = HistoriaClinicaForm() 
        if current_user.is_authenticated and current_user.id_tipo == 1:
                title_str = "Historial de "+ cliente.username 
                lista_podologos = Empleado.query.filter_by(id_tipo = 1).all()
                if form.validate_on_submit():
                        fecha_hoy = datetime.now()
                        historia = Historiaclinica(
                                datetime = fecha_hoy,
                                diagnostico = form.diagnostico.data,
                                diabetes = form.diabetes.data,
                                antecedentes = form.antecedentes.data,
                                onicopatias = form.onicopatias.data,
                                otros_datos = form.otros_datos.data,
                                id_empleado = current_user.id,
                                id_cliente = id_cliente
                        )
                        db.session.add(historia)
                        db.session.commit()
                        return redirect(url_for('historiaclinica.historias_clinicas', id_cliente=id_cliente))
                return render_template('historias_clinicas.html', title=title_str, cliente=cliente, historias_clinicas=historias_clinicas, form=form, lista_podologos = lista_podologos)
        return redirect(url_for('main.home'))

@historiaclinica.route("/historias-clinicas/eliminar/<int:id_historia>", methods=['GET', 'POST'])
@login_required
def eliminar_historia(id_historia, num):
        if current_user.is_authenticated:
                if current_user.id_tipo == 1: 
                        historia = Historiaclinica.query.filter_by(id_historia_clinica = id_historia).first()
                        id_cliente = historia.id_cliente
                        db.session.delete(historia)
                        db.session.commit()
                        flash('La historia clinica ha sido eliminada.', 'success')
                        if num==1:
                                return redirect(url_for('historiaclinica.historias_clinicas', id_cliente=id_cliente))
                        else:
                                return redirect(url_for('historiaclinica.tablaHC'))
                else:
                        return redirect(url_for('main.home'))
        else:
                return redirect(url_for('empleado.login'))

@historiaclinica.route("/historias-clinicas/editar/<int:id_historia>", methods=['GET', 'POST'])
@login_required
def editar_historia(id_historia, num):
        if current_user.is_authenticated:
                if current_user.id_tipo == 1: 
                        historia = Historiaclinica.query.filter_by(id_historia_clinica = id_historia).first()
                        id_cliente = historia.id_cliente
                        form = HistoriaClinicaForm()
                        if form.validate_on_submit():
                                historia.diagnostico = form.diagnostico.data
                                historia.diabetes = form.diabetes.data
                                historia.antecedentes = form.antecedentes.data
                                historia.onicopatias = form.onicopatias.data
                                historia.otros_datos = form.otros_datos.data
                                db.session.commit()
                                flash('Los datos de la historia clinica han sido actualizados.', 'success')
                                if num==1:
                                        return redirect(url_for('historiaclinica.historias_clinicas', id_cliente=id_cliente))
                                else:
                                        return redirect(url_for('historiaclinica.tablaHC'))
                        elif request.method=='GET':
                                form.diagnostico.data =  historia.diagnostico
                                form.diabetes.data = historia.diabetes
                                form.antecedentes.data = historia.antecedentes
                                form.onicopatias.data = historia.onicopatias
                                form.otros_datos.data  =  historia.otros_datos
                        return render_template('editar_historia_clinica.html', id_cliente=id_cliente, form=form)
                else:
                        return redirect(url_for('main.home'))
        else:
                return redirect(url_for('empleado.login'))

####SOFIA###
@historiaclinica.route("/tabla_historias_clinicas", methods=['GET', 'POST'])
@login_required
def tablaHC():
        if current_user.is_authenticated and current_user.id_tipo == 1:
                historiasclinicas = Historiaclinica.query.all()
                clientes = Cliente.query.all()
                podologos = Empleado.query.all()
                form = TablaHistoriaClinicaForm() 
                if form.validate_on_submit():
                        hc = Historiaclinica(
                                datetime = datetime.now(),
                                diagnostico = form.diagnostico.data,  
                                diabetes = form.diabetes.data,
                                antecedentes = form.antecedentes.data,
                                onicopatias = form.onicopatias.data,
                                otros_datos = form.otros_datos.data,
                                id_empleado = current_user.id,                                        
                                id_cliente = form.id_cliente.data
                        )
                        db.session.add(hc)
                        db.session.commit()
                        flash(f'La Historia Clinica ha sido creada con exito.', 'success')
                        return redirect(url_for('historiaclinica.tablaHC'))
                return render_template('tabla_historias_clinicas.html', title="Gestion de Historias Clinicas", historiasclinicas = historiasclinicas, podologos = podologos, clientes = clientes, form=form) 
        else:
                return redirect(url_for('empleado.login'))




