import json
from flask import render_template, url_for, flash, redirect, request
from appmipedicenter.models import *
from appmipedicenter.forms import RegistrationForm, LoginForm, UpdateAccountForm
from Plantilla import Plantilla
from appmipedicenter import app, bcrypt, db
from flask_login import login_user, current_user, logout_user, login_required
from datetime import *

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
                        login_user(empleado, remember=form.remember)
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
        form = UpdateAccountForm()
        if form.validate_on_submit():
                current_user.username= form.username.data
                current_user.dni= form.dni.data
                current_user.id= form.email.data
                current_user.telefono= form.telefono.data
                current_user.fecha_nacimiento= form.fecha_nacimiento.data
                db.session.commit()
                flash('Los datos de tu cuenta han sido actualizados.', 'success')
                return redirect(url_for('mi_perfil'))
        elif request.method=='GET':
                form.username.data = current_user.username
                form.dni.data = current_user.dni
                form.email.data = current_user.id
                form.telefono.data = current_user.telefono
                form.fecha_nacimiento.data = current_user.fecha_nacimiento 
        return render_template('mi_perfil.html', title="MiPerfil", form=form)

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
        datePlant = date.fromisoformat(date_str)
        plantilla = Plantilla(datePlant)
        if (current_user.id_tipo == 1):     #Incluye CRUD Turnos, Disp Horario e Historias Clinicas
                return render_template('plantilla_podologo.html', title="Calendario Vista Podologo", plantilla=plantilla)
        elif (current_user.id_tipo == 2):
                return render_template('plantilla_recep.html', title="Calendario Vista Recepcionista", plantilla=plantilla) 
