import os
import secrets
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
class Config(object):
    DEBUG = True
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CSRF_ENABLED = True
    CSRF_SESSION_KEY = secrets.token_urlsafe(24)
    
# Session
PERMANENT_SESSION_LIFETIME = timedelta(minutes=120)

class DevelopmentConfig(Config):
    ENV='development'
    SECRET_KEY = os.getenv('SECRET_KEY_DEV', secrets.token_urlsafe(24))
    DATABASE_NAME = "awesome_repo_dev.db"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, DATABASE_NAME)
    ADMIND_DASHBOARD_VISIBLE = True
class TestingConfig(Config):
    ENV='development'
    SECRET_KEY = os.getenv('SECRET_KEY_TEST', secrets.token_urlsafe(24))
    DATABASE_NAME = "awesome_repo_test.db"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, DATABASE_NAME)
    ADMIND_DASHBOARD_VISIBLE = True
class ProductionConfig(Config):
    SECRET_KEY = os.getenv('SECRET_KEY_PROD', secrets.token_urlsafe(24))
    DATABASE_NAME = "awesome_repo_prod.db"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, DATABASE_NAME)
    ADMIND_DASHBOARD_VISIBLE = False

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}