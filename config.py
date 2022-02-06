import os
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
class Config(object):
    DEBUG = True
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CSRF_ENABLED = True
    CSRF_SESSION_KEY = os.urandom(24)
    
# Session
PERMANENT_SESSION_LIFETIME = timedelta(minutes=240)

class DevelopmentConfig(Config):
    SECRET_KEY = os.getenv('SECRET_KEY_DEV', os.urandom(24))
    DATABASE_NAME = "awesome_repo_dev.db"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, DATABASE_NAME)
    ADMIND_DASHBOARD_VISIBLE = True
class TestingConfig(Config):
    SECRET_KEY = os.getenv('SECRET_KEY_TEST', os.urandom(24))
    DATABASE_NAME = "awesome_repo_test.db"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, DATABASE_NAME)
    ADMIND_DASHBOARD_VISIBLE = True
class ProductionConfig(Config):
    SECRET_KEY = os.getenv('SECRET_KEY_PROD', os.urandom(24))
    DATABASE_NAME = "awesome_repo_prod.db"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, DATABASE_NAME)
    ADMIND_DASHBOARD_VISIBLE = False

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}