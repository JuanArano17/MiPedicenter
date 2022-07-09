from http.client import REQUEST_HEADER_FIELDS_TOO_LARGE
import json
from flask import render_template, url_for, flash, redirect, request
from appmipedicenter.models import *
from appmipedicenter.forms import RegistrationForm, LoginForm, UpdateAccountForm, ClienteForm, ClienteUpdateForm, AsignarTurno
from appmipedicenter.Plantilla import Plantilla
from appmipedicenter import app, bcrypt, db, mail
from flask_login import login_user, current_user, logout_user, login_required
from datetime import *
from flask_mail import Message

@app.route("/")
@app.route("/home")
def home():
        return render_template('home.html')

@app.route("/register", methods=['GET','POST'])
def register():
        if current_user.is_authenticated:
                return redirect(url_for('home'))
        form = RegistrationForm()
        if form.validate_on_submit():
                hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                empl = Empleado(id=form.email.data,
                        dni=form.dni.data,
                        username=form.username.data, 
                        fecha_nacimiento=form.fecha_nacimiento.data,
                        telefono=form.telefono.data,
                        password=hashed_password,
                        id_tipo=form.id_tipo.data)
                db.session.add(empl)
                db.session.commit()
                flash(f'{form.username.data}, tu cuenta ha sido creada con exito.', 'success')
                return redirect(url_for('home'))
        return render_template('register.html', title='Register', form=form)

@app.route("/login",  methods=['GET','POST'])
def login():
        if current_user.is_authenticated:
                return redirect(url_for('home'))
        form = LoginForm()
        if form.validate_on_submit():
                empleado = Empleado.query.filter_by(id = form.email.data).first()
                if empleado and bcrypt.check_password_hash(empleado.password, form.password.data):
                        login_user(empleado, remember=True)
                        next_page = request.args.get('next')
                        flash(f'{empleado.username}, has sido logeado con exito', 'success')
                        return redirect(next_page) if next_page else redirect (url_for('home'))
                else:
                        flash('Las credenciales no coinciden. Por favor verifica el Email y la contraseña', 'danger')
        return render_template('login.html', title="Login", form=form)

@app.route("/logout")
def logout():
        logout_user()
        return redirect(url_for('home'))

@app.route("/mi-perfil", methods=['GET','POST'])
@login_required
def mi_perfil():
        cuenta_tipo = Tipoempleado.query.filter_by(id_tipo = current_user.id_tipo).first()
        form = UpdateAccountForm()
        if form.validate_on_submit():
                current_user.username= form.username.data
                current_user.dni= form.dni.data
                current_user.telefono= form.telefono.data
                current_user.fecha_nacimiento= form.fecha_nacimiento.data
                db.session.commit()
                flash('Los datos de tu cuenta han sido actualizados.', 'success')
                return redirect(url_for('mi_perfil'))
        elif request.method=='GET':
                form.username.data = current_user.username
                form.dni.data = current_user.dni
                form.telefono.data = current_user.telefono
                form.fecha_nacimiento.data = current_user.fecha_nacimiento 
        return render_template('mi_perfil.html', title="MiPerfil", form=form, cuenta_tipo = cuenta_tipo)


@app.route("/eliminar-cuenta/<string:id>", methods=['POST'])
@login_required
def eliminar_cuenta(id):
        empleado = Empleado.query.get_or_404(id)
        if empleado != current_user:
                abort(403)
        listaTurnosEmpleado = Turno.query.filter_by(id_empleado = empleado.id)
        for i in listaTurnosEmpleado:
                db.session.delete(i)
        db.session.delete(empleado)
        db.session.commit()
        flash('Tu cuenta ha sido eliminada', 'success')
        logout_user()
        return redirect(url_for('home'))
        



@app.route("/mi-calendario") #Incluye CRUD Turnos (envio mail), CURD Clientes y Disp Horario
@login_required
def mi_calendario():
        if request.method == "POST":
                date_str = request.get_data()
                return redirect(url_for("plantilla_turnos", date_str = date_str))
        return render_template('mi_calendario.html', title="Calendario Turnos") 

@app.route("/plantilla-turnos/<string:date_str>", methods=['POST', 'GET'])
@login_required
def plantilla_turnos(date_str):
        if current_user.is_authenticated:
                datePlant = date.fromisoformat(date_str)
                plantilla = Plantilla(datePlant)
                if (current_user.id_tipo == 1):     #Incluye CRUD Turnos, Disp Horario e Historias Clinicas
                        return render_template('plantilla_podologo.html', title="Calendario Vista Podologo", plantilla=plantilla)
                elif (current_user.id_tipo == 2):
                        form_crear_turno = AsignarTurno()
                        if form_crear_turno.validate_on_submit():
                                form_crear_turno.date = datePlant
                                flash('Se ha asignado el turno con exito', 'success')
                                turno = Turno.query.filter_by(date = form_crear_turno.date, id_empleado = form_crear_turno.id_podologo.data, id_hora = form_crear_turno.id_hora.data).first()
                                turno.id_cliente = form_crear_turno.dni.data
                                db.session.commit()
                                return redirect(url_for("plantilla_turnos", date_str = date_str))
                        return render_template('plantilla_recep.html', title="Calendario Vista Recepcionista", plantilla=plantilla, form_crear_turno=form_crear_turno)
        else:
                return redirect(url_for('home'))

@app.route("/pacientes", methods=['GET', 'POST'])
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
                                return redirect(url_for('pacientes'))
                        return render_template('pacientes.html', title="Gestion de Pacientes", clientes = client_list, form=form) 
                else:
                        return redirect(url_for('home'))
        else:
                return redirect(url_for('login'))

@app.route("/pacientes/editar/<int:id_cliente>", methods=['GET', 'POST'])
@login_required
def editar_pacientes(id_cliente):
        if current_user.is_authenticated:
                if current_user.id_tipo == 2: 
                        cliente = Cliente.query.filter_by(id_cliente = id_cliente).first()
                        form = ClienteUpdateForm()
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
                                return redirect(url_for('pacientes'))
                        elif request.method=='GET':
                                form.username.data = cliente.username
                                form.dni.data = cliente.id_cliente
                                form.email.data = cliente.email
                                form.telefono.data = cliente.telefono
                                form.fecha_nacimiento.data = cliente.fecha_nacimiento 
                        return render_template('editar_paciente.html', title="Edicion de Clientes", form=form)
                else:
                        return redirect(url_for('home'))
        else:
                return redirect(url_for('login'))
                
@app.route("/pacientes/eliminar/<int:id_cliente>", methods=['GET', 'POST'])
@login_required
def eliminar_pacientes(id_cliente):
        if current_user.is_authenticated:
                if current_user.id_tipo == 2: 
                        cliente = Cliente.query.filter_by(id_cliente = id_cliente).first()
                        lista_turnos_cliente = Turno.query.filter_by(id_cliente = cliente.id_cliente)
                        for i in lista_turnos_cliente:
                                db.session.delete(i)
                        db.session.delete(cliente)
                        db.session.commit()
                        flash(f'Los datos de {cliente.username} han sido borrados.', 'success')
                        return redirect(url_for('pacientes'))
                else:
                        return redirect(url_for('home'))
        else:
                return redirect(url_for('login'))

def mandar_mail_turno(Cliente, Date):
        msg = Message('Confirmacion de turno Pedicenter', sender='mipedicenter@gmail.com', recipients=[Cliente.email])
        msg.body = f''' Un turno podologico ha sido asignado exitosamente para el dia {Date} en la sede Arenales 1283 PB.'''
        mail.send(msg)