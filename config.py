import os
import secrets
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Defines a base configuration for the app
class Config(object):
    DEBUG = True
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CSRF_ENABLED = True
    CSRF_SESSION_KEY = secrets.token_urlsafe(24)
    
# Session
PERMANENT_SESSION_LIFETIME = timedelta(minutes=120)

# Defines different environmental configuration for the app
# The purpose is to support different settings/databases
# to avoid the database records to be deleted accidentally
# Moreover, testing on development environment won't affect the production users
class DevelopmentConfig(Config):
    ENV='development'
    SECRET_KEY = os.getenv('SECRET_KEY_DEV', secrets.token_urlsafe(24))
    DATABASE_NAME = "awesome_repo_dev.db"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, DATABASE_NAME)
class TestingConfig(Config):
    ENV='development'
    SECRET_KEY = os.getenv('SECRET_KEY_TEST', secrets.token_urlsafe(24))
    DATABASE_NAME = "awesome_repo_test.db"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, DATABASE_NAME)
class ProductionConfig(Config):
    SECRET_KEY = os.getenv('SECRET_KEY_PROD', secrets.token_urlsafe(24))
    DATABASE_NAME = "awesome_repo_prod.db"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, DATABASE_NAME)

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}