from http.client import REQUEST_HEADER_FIELDS_TOO_LARGE
from flask import render_template, url_for, flash, redirect, request, Blueprint
from appmipedicenter.models import Empleado, Tipoempleado, Turno
from appmipedicenter.empleado.forms import  RegistrationForm, LoginForm, UpdateAccountForm
from appmipedicenter import bcrypt, db
from flask_login import login_user, current_user, logout_user, login_required
from datetime import *

empleado = Blueprint('empleado', __name__)

@empleado.route("/register", methods=['GET','POST'])
def register():
        if current_user.is_authenticated:
                return redirect(url_for('main.home'))
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
                return redirect(url_for('main.home'))
        return render_template('register.html', title='Register', form=form)

@empleado.route("/login",  methods=['GET','POST'])
def login():
        if current_user.is_authenticated:
                return redirect(url_for('main.home'))
        form = LoginForm()
        if form.validate_on_submit():
                empleado = Empleado.query.filter_by(id = form.email.data).first()
                if empleado and bcrypt.check_password_hash(empleado.password, form.password.data):
                        login_user(empleado, remember=True)
                        next_page = request.args.get('next')
                        flash(f'{empleado.username}, has sido logeado con exito', 'success')
                        return redirect(next_page) if next_page else redirect (url_for('main.home'))
                else:
                        flash('Las credenciales no coinciden. Por favor verifica el Email y la contraseña', 'danger')
        return render_template('login.html', title="Login", form=form)

@empleado.route("/logout")
def logout():
        logout_user()
        return redirect(url_for('main.home'))

@empleado.route("/mi-perfil", methods=['GET','POST'])
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
                return redirect(url_for('empleado.mi_perfil'))
        elif request.method=='GET':
                form.username.data = current_user.username
                form.dni.data = current_user.dni
                form.telefono.data = current_user.telefono
                form.fecha_nacimiento.data = current_user.fecha_nacimiento 
        return render_template('mi_perfil.html', title="MiPerfil", form=form, cuenta_tipo = cuenta_tipo)


@empleado.route("/eliminar-cuenta/<string:id>", methods=['POST'])
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
        return redirect(url_for('main.home'))