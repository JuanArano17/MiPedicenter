from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from appmipedicenter.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'empleado.login'
login_manager.login_message = 'Debes ingresarte para poder acceder a tu perfil.' 
login_manager.login_message_category = 'info'

mail = Mail()

def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from appmipedicenter.cliente.routes import cliente
    from appmipedicenter.empleado.routes import empleado
    from appmipedicenter.historiaclinica.routes import historiaclinica
    from appmipedicenter.turno.routes import turno
    from appmipedicenter.main.routes import main
    from appmipedicenter.errors.handlers import errors
    app.register_blueprint(cliente)
    app.register_blueprint(empleado)
    app.register_blueprint(historiaclinica)
    app.register_blueprint(turno)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app