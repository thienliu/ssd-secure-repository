# Import flask and template operators
from flask import Flask, render_template, redirect, url_for
from flask_bcrypt import Bcrypt

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

# Import a module / component using its blueprint handler variable (mod_auth)
from app.auth.controllers import auth as auth_module
from app.main.controllers import main as main_module

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.route('/')
def index():
    return redirect(url_for('main.home'))

# Register blueprint(s)
app.register_blueprint(auth_module)
app.register_blueprint(main_module)
# ..

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()