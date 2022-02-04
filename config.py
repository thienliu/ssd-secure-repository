import os
from datetime import timedelta

DEBUG = True
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# SQLAlchemy
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'awesome_repo.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

DATABASE_CONNECT_OPTIONS = {}

CSRF_ENABLED = True
CSRF_SESSION_KEY = os.urandom(24)
SECRET_KEY = os.urandom(24)

# Admin dashboard visibility
ADMIND_DASHBOARD_VISIBLE = True

# Session
PERMANENT_SESSION_LIFETIME = timedelta(minutes=240)