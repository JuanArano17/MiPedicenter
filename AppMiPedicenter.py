from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '4ecd725281820152a8d856062cbc77'

@app.route("/")
@app.route("/home")
def home():
        return render_template('home.html')

@app.route("/register", methods=['GET','POST'])
def register():
        form = RegistrationForm()
        if form.validate_on_submit():
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



@app.route("/podologo")
def podo():
        return render_template('podologo.html', title = "Podologo")

@app.route("/administrador")
def admin():
        return render_template('administrdor.html', title="Centro de accion del Administrador")

@app.route("/recepcionista")
def recep():
        return render_template('recepcionista.html', title="Centro de accion del Recepcionista")

@app.route("/recepcionista/calendario")
def calen_recep():
        return render_template('calen_recep.html', title="Calendario Vista Recepcionista")

@app.route("/podologo/calendario")
def calen_podo():
        return render_template('calen_podo.html', title="Calendario Vista Podologo")

@app.route("/podologo/historia-clinica")
def historiaClinica():
        return render_template('hist_clin.html', title="Historias Clinicas")

if __name__ == '__main__':
        app.run(debug=True)
