# Import flask and template operators
from flask import Flask, render_template, redirect, url_for
from flask_login import login_user, current_user, logout_user, login_required, UserMixin, LoginManager
from flask_bcrypt import Bcrypt
from config import config

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object(config['production'])

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

# Creates an instance of LoginManager
# which will provide user session management,
# handle the common tasks of logging in, logging out,
# and remembering user's session

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

app.app_context().push()

# Import a module / component using its blueprint handler variable (mod_auth)
from app.auth.controllers import auth as auth_module
from app.main.controllers import main as main_module
from app.admin.controllers import admin as admin_module
from app.document.controllers import document as document_module

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.route('/')
def index():
    return redirect(url_for('main.home'))

# Register blueprint(s)
app.register_blueprint(auth_module)
app.register_blueprint(main_module)
app.register_blueprint(admin_module)
app.register_blueprint(document_module)
# ..

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()