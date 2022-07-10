from asyncio.windows_events import NULL
from http.client import REQUEST_HEADER_FIELDS_TOO_LARGE
import json
from flask import render_template, url_for, flash, redirect, request
from appmipedicenter.models import *
from appmipedicenter.forms import HistoriaClinicaForm, RegistrationForm, LoginForm, UpdateAccountForm, ClienteForm, ClienteUpdateForm, AsignarTurno, HistoriaClinicaForm
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


@app.route("/plantilla-turnos/<string:date_str>", methods=['GET', 'POST'])
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
                return redirect(url_for('home'))

@app.route("/plantilla-turnos/turno-disponible<string:date_str>/<int:i>/<int:j>", methods=['GET', 'POST'])
@login_required
def turno_disponible(date_str, j, i):
        if current_user.is_authenticated:
                datePlant = date.fromisoformat(date_str)
                plantilla = Plantilla(datePlant)
                if (current_user.id_tipo == 1): 
                        return redirect(url_for('home'))
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
                                return redirect(url_for("plantilla_turnos", date_str = date_str))
                        return render_template('opciones_turno_disponible.html', title="Opciones para turno disponible", form_crear_turno=form_crear_turno, date_str=date_str, i=i, j=j)

@app.route("/cambio-disponibilidad/<string:date_str>/<int:i>/<int:j>", methods=['GET', 'POST'])
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
                return redirect(url_for("plantilla_turnos", date_str = date_str))

@app.route("/plantilla-turnos/gestion-eliminar-turno<string:date_str>/<int:i>/<int:j>", methods=['GET', 'POST'])
@login_required
def gestion_elimiar_turno(date_str, j, i):
        if current_user.is_authenticated:
                datePlant = date.fromisoformat(date_str)
                plantilla = Plantilla(datePlant)
                if (current_user.id_tipo == 2): 
                        return render_template('gestion_eliminar_turno.html', title="Gesstion de eliminacion de turnos", date_str = date_str, i=i, j=j)
                else:
                        return redirect(url_for('home'))

@app.route("/plantilla-turnos/eliminar-turno<string:date_str>/<int:i>/<int:j>", methods=['GET', 'POST'])
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
                        return redirect(url_for("plantilla_turnos", date_str = date_str))
                else:
                        return redirect(url_for('historias_clinicas'))

@app.route("/cambio-atendido/<string:date_str>/<int:i>/<int:j>", methods=['GET', 'POST'])
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
                return redirect(url_for("plantilla_turnos", date_str = date_str))

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

def mandar_mail_turno(cliente, date_str, hora, nombre_empleado):
        msg = Message('Confirmacion de turno Pedicenter', sender='mipedicenter@gmail.com', recipients=[cliente.email])
        msg.body = f''' Estimado/a {cliente.username}:

 Un turno podologico ha sido asignado exitosamente para el dia {date_str} a las {hora}hs con {nombre_empleado} en la sede: Arenales-1283-PB-Recoleta .
        
        Att: Pedicenter.'''
        mail.send(msg)

@app.route("/historias-clinicas/<int:id_cliente>", methods=['GET', 'POST'])
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
                        return redirect(url_for('historias_clinicas', id_cliente=id_cliente))
                return render_template('historias_clinicas.html', title=title_str, cliente=cliente, historias_clinicas=historias_clinicas, form=form, lista_podologos = lista_podologos)
        return redirect(url_for('home'))

@app.route("/historias-clinicas/eliminar/<int:id_historia>", methods=['GET', 'POST'])
@login_required
def eliminar_historia(id_historia):
        if current_user.is_authenticated:
                if current_user.id_tipo == 1: 
                        historia = Historiaclinica.query.filter_by(id_historia_clinica = id_historia).first()
                        id_cliente = historia.id_cliente
                        db.session.delete(historia)
                        db.session.commit()
                        flash('La historia clinica ha sido eliminada.', 'success')
                        return redirect(url_for('historias_clinicas', id_cliente=id_cliente))
                else:
                        return redirect(url_for('home'))
        else:
                return redirect(url_for('login'))

@app.route("/historias-clinicas/editar/<int:id_historia>", methods=['GET', 'POST'])
@login_required
def editar_historia(id_historia):
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
                                return redirect(url_for('historias_clinicas', id_cliente=id_cliente))
                        elif request.method=='GET':
                                form.diagnostico.data =  historia.diagnostico
                                form.diabetes.data = historia.diabetes
                                form.antecedentes.data = historia.antecedentes
                                form.onicopatias.data = historia.onicopatias
                                form.otros_datos.data  =  historia.otros_datos
                        return render_template('editar_historia_clinica.html', id_cliente=id_cliente, form=form)
                else:
                        return redirect(url_for('home'))
        else:
                return redirect(url_for('login'))