# Import flask dependencies
from flask import ( 
    Blueprint, 
    request, 
    render_template, 
    flash, 
    g, 
    session, 
    redirect, 
    url_for 
)

# Import password /encryption helper tools
from flask_bcrypt import Bcrypt

# Import the database object from the main app module
from app import db

from app.auth.forms import LoginForm
from app.auth.models import User

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    return render_template("auth/login.html", form=form)