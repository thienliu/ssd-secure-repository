import os

class Config(object):
    DEBUG = True
    TESTING = False
    DATABASE_NAME = "awesome_repo"

class DevelopmentConfig(Config):
    # Configure app's secret key to use sessions for authentication
    SECRET_KEY = os.urandom(24)

config = {
    'development': DevelopmentConfig,
    'testing': DevelopmentConfig,
    'production': DevelopmentConfig
}
