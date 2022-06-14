from flask import render_template, url_for, flash, redirect
from appmipedicenter.models import *
from appmipedicenter.forms import RegistrationForm, LoginForm
from appmipedicenter import app, bcrypt, db

@app.route("/")
@app.route("/home")
def home():
        return render_template('home.html')

@app.route("/register", methods=['GET','POST'])
def register():
        form = RegistrationForm()
        if form.validate_on_submit():
                hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                Empleado(id_empleado=form.email.data,
                        dni=form.dni.data,
                        username=form.username.data, 
                        fecha_nacimiento=form.fecha_nacimiento.data,
                        telefono=form.telefono.data,
                        password=form.password.data,
                        id_tipo=form.id_tipo.data)
                flash(f'Cuenta creada con exito para {form.username.data}!', 'success')
                return redirect(url_for('home'))
        return render_template('register.html', title='Register', form=form)

@app.route("/login",  methods=['GET','POST'])
def login():
        form = LoginForm()
        if form.validate_on_submit():
                if form.email.data == 'juanarano17@gmail.com' and form.password.data == '123456':
                        flash('Te logueaste con exito', 'success')
                        return redirect(url_for('home'))
                else:
                        flash('Las credenciales no coinciden', 'danger')
        return render_template('login.html', title="Login", form=form)

@app.route("/mi-perfil-podologo")
def podo():
        return render_template('podologo.html', title = "Podologo")

@app.route("/mi-perfil-recepcionista")
def recep():
        return render_template('recepcionista.html', title="Centro de accion del Recepcionista")

@app.route("/calendario-recepcionista") #Incluye CRUD Turnos (envio mail), CURD Clientes y Disp Horario
def calen_recep():
        return render_template('calen_recep.html', title="Calendario Vista Recepcionista")

@app.route("/calendario-podologo")      #Incluye CRUD Turnos, Disp Horario e Historias Clinicas
def calen_podo():
        return render_template('calen_podo.html', title="Calendario Vista Podologo")
