from flask import Flask, render_template, url_for
app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
        return render_template('home.html')

@app.route("/login")
def login():
        return render_template('login.html', title="LogIn")

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