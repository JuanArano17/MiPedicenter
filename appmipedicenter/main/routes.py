from asyncio.windows_events import NULL
from http.client import REQUEST_HEADER_FIELDS_TOO_LARGE
from flask import render_template, Blueprint

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
        return render_template('home.html')